"""Verify the approved AC-2 extension without changing the original 87 contracts."""
import argparse
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from verify_ac1_baseline import REPO, self_test as common_self_test, test_id, verify

MANIFEST = REPO / "docs/evidence/ac2/expected-tests.json"
BASE_MANIFEST = REPO / "docs/evidence/ac1/expected-tests.json"
PHASE_COUNTS = {"passed": 88, "stub_failure": 2, "skipped": 5}
NEW_FILE = "tests/test_s1_validation.py"
NEW_TEST_IDS = {
    f"{NEW_FILE}::{name}" for name in (
        "test_ac2_rejects_unstorable_description[nul]",
        "test_ac2_rejects_unstorable_description[unpaired-high]",
        "test_ac2_rejects_unstorable_description[unpaired-low]",
        "test_ac2_invalid_description_precedes_category",
        "test_ac2_accepts_supplementary_unicode",
        "test_ac2_identity_precedes_unstorable_description",
        "test_ac2_membership_precedes_unstorable_description",
        "test_ac2_length_precedes_unstorable_description",
    )
}


def manifest_errors(manifest, base, base_hash):
    errors = []
    if manifest["ac1_manifest_sha256"] != base_hash:
        errors.append("Protected AC-1 manifest hash changed")
    if set(manifest["new_test_ids"]) != NEW_TEST_IDS or len(manifest["new_test_ids"]) != 8:
        errors.append("New-case list differs from the eight approved AC-2 IDs")
    if set(manifest["tests"]) != set(base["tests"]) | NEW_TEST_IDS:
        errors.append("Manifest must contain all original tests and only the eight approved additions")
    for node_id, rule in base["tests"].items():
        if manifest["tests"].get(node_id) != rule:
            errors.append(f"Original test expectation changed: {node_id}")
    for node_id in NEW_TEST_IDS:
        if manifest["tests"].get(node_id) != {"outcome": "passed"}:
            errors.append(f"Approved new test must pass: {node_id}")
    if set(manifest["test_file_sha256"]) != set(base["test_file_sha256"]) | {NEW_FILE}:
        errors.append("Test-file inventory differs from the approved extension")
    for path, digest in base["test_file_sha256"].items():
        if manifest["test_file_sha256"].get(path) != digest:
            errors.append(f"Original test-file hash changed: {path}")
    return errors


def verify_phase(root, manifest, base, base_hash):
    return manifest_errors(manifest, base, base_hash) + verify(
        root, manifest, phase_counts=PHASE_COUNTS,
    )


def self_test(manifest, base, base_hash):
    # Shared verification still covers missing original tests, errors and bad outcomes.
    output = io.StringIO()
    with redirect_stdout(output):
        common_self_test(manifest, phase_counts=PHASE_COUNTS)
    common = json.loads(output.getvalue())
    valid = ET.Element("testsuites")
    suite = ET.SubElement(valid, "testsuite")
    for node_id, rule in manifest["tests"].items():
        path, name = node_id.split("::", 1)
        case = ET.SubElement(suite, "testcase", classname=path[:-3].replace("/", "."), name=name)
        if rule["outcome"] == "stub_failure":
            ET.SubElement(case, "failure", message=rule["message_prefix"] + "\n + response is 501")
        elif rule["outcome"] == "skipped":
            ET.SubElement(case, "skipped", message=rule["reason"])
    if verify_phase(valid, manifest, base, base_hash):
        raise ValueError("AC-2 self-test valid control was rejected")
    altered = deepcopy(valid)
    case = next(c for c in altered[0] if test_id(c) in NEW_TEST_IDS)
    altered[0].remove(case)
    if not verify_phase(altered, manifest, base, base_hash):
        raise ValueError("AC-2 verifier accepted a missing new test")
    rejected = ["missing new test"]
    mutations = {}
    bad = deepcopy(manifest)
    bad["tests"][next(iter(base["tests"]))] = {"outcome": "skipped", "reason": "unauthorized"}
    mutations["changed original expectation"] = bad
    bad = deepcopy(manifest)
    bad["test_file_sha256"][next(iter(base["test_file_sha256"]))] = "0" * 64
    mutations["changed original file hash"] = bad
    bad = deepcopy(manifest)
    bad["ac1_manifest_sha256"] = "0" * 64
    mutations["changed original manifest hash"] = bad
    bad = deepcopy(manifest)
    bad["tests"]["tests/unapproved.py::test_extra"] = {"outcome": "passed"}
    mutations["unapproved additional test"] = bad
    bad = deepcopy(manifest)
    bad["test_file_sha256"][NEW_FILE] = "0" * 64
    mutations["changed new test-file hash"] = bad
    bad = deepcopy(manifest)
    bad["tests"][sorted(NEW_TEST_IDS)[0]] = {"outcome": "skipped", "reason": "unauthorized"}
    mutations["new test not required to pass"] = bad
    for label, bad in mutations.items():
        if not verify_phase(valid, bad, base, base_hash):
            raise ValueError(f"AC-2 verifier accepted defect: {label}")
        rejected.append(label)
    print(json.dumps({"common_gate": common, "ac2_valid_control": "accepted",
                      "ac2_extension_rejected_defects": rejected}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--junit", type=Path, default=REPO / "artifacts/pytest.xml")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(MANIFEST.read_text())
        base_bytes = BASE_MANIFEST.read_bytes()
        base, base_hash = json.loads(base_bytes), hashlib.sha256(base_bytes).hexdigest()
        if args.self_test:
            self_test(manifest, base, base_hash)
            return 0
        errors = verify_phase(ET.parse(args.junit).getroot(), manifest, base, base_hash)
        if errors:
            print("AC-2 PHASE REJECTED:\n" + "\n".join(errors), file=sys.stderr)
            return 1
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        print(f"AC-2 PHASE REJECTED: {exc}", file=sys.stderr)
        return 1
    print("AC-2 PHASE VERIFIED: 88 passed; AC-4/AC-6 remain 501 failures; 5 exact S-6 skips. Full S-1 is incomplete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
