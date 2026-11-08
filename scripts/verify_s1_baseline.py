"""Exact gate for approved AC-4/AC-6: 120 passes and five unchanged S-6 skips."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from verify_ac1_baseline import REPO, test_id, verify
from verify_ac2_baseline import manifest_errors as ac2_manifest_errors

MANIFEST = REPO / "docs/evidence/ac4/expected-tests.json"
AC1_MANIFEST = REPO / "docs/evidence/ac1/expected-tests.json"
AC2_MANIFEST = REPO / "docs/evidence/ac2/expected-tests.json"
NEW_FILE = "tests/test_s1_details.py"
# Frozen at the actual tests-first commit fb8db8046e3458a14d4c9edf04f019d3fcf7332e.
NEW_TEST_SHA256 = "e5449fa0885fc7e3c8bd14b552fc56a4775ac705effecb695a710bf5fdd60ce5"
# The unchanged shared verifier compares Counter dictionaries, which omit zero
# outcomes. Manifest validation below guarantees this exact no-failure phase
# before calling it; historical verifier defaults remain untouched.
PHASE_COUNTS = {"passed": 120, "skipped": 5}
PROMOTED_IDS = {
    "tests/test_s1_requests.py::test_ac4_other_community_direct_id_returns_not_found",
    "tests/test_s1_requests.py::test_ac6_resident_sees_in_progress_status",
}
NEW_TEST_IDS = {
    f"{NEW_FILE}::test_ac4_details_{name}"
    for name in (
        "identity_precedes_path", "membership_elsewhere_does_not_authorize",
        "owner_in_two_communities",
        *(f"reject_invalid_caller[{case}]" for case in (
            "missing", "empty", "zero", "negative", "leading-zero", "plus",
            "decimal", "text", "space", "unknown", "outside-db-range",
        )),
        *(f"reject_unavailable_id[{case}]" for case in (
            "zero", "negative", "leading-zero", "text", "unicode-digits",
            "decimal", "unknown", "outside-db-range",
        )),
        *(f"reject_nonresident_owner[{role}]" for role in ("board_member", "manager", "admin")),
        "reject_other_submitter[same-community]", "reject_other_submitter[same-unit]",
        "returns_persisted_status[open]", "returns_persisted_status[in-progress]",
        "returns_persisted_status[resolved]",
    )
}


def manifest_errors(manifest, ac2, ac1, ac2_hash, ac1_hash):
    errors = ac2_manifest_errors(ac2, ac1, ac1_hash)
    if manifest["ac1_manifest_sha256"] != ac1_hash:
        errors.append("Protected AC-1 manifest hash changed")
    if manifest["ac2_manifest_sha256"] != ac2_hash:
        errors.append("Protected AC-2 manifest hash changed")
    if set(manifest["new_test_ids"]) != NEW_TEST_IDS or len(manifest["new_test_ids"]) != 30:
        errors.append("New-case list must equal the 30 approved AC-4 IDs")
    if set(manifest["promoted_test_ids"]) != PROMOTED_IDS or len(manifest["promoted_test_ids"]) != 2:
        errors.append("Only the original AC-4 and AC-6 cases may be promoted")
    if set(manifest["tests"]) != set(ac2["tests"]) | NEW_TEST_IDS:
        errors.append("Test inventory must preserve the original 95 plus exactly 30 additions")
    for node_id, rule in ac2["tests"].items():
        expected = {"outcome": "passed"} if node_id in PROMOTED_IDS else rule
        if manifest["tests"].get(node_id) != expected:
            errors.append(f"Original expectation differs from approved promotion: {node_id}")
    for node_id in NEW_TEST_IDS:
        if manifest["tests"].get(node_id) != {"outcome": "passed"}:
            errors.append(f"New contract must pass: {node_id}")
    if set(manifest["test_file_sha256"]) != set(ac2["test_file_sha256"]) | {NEW_FILE}:
        errors.append("Test-file inventory differs from approved extension")
    if manifest["test_file_sha256"].get(NEW_FILE) != NEW_TEST_SHA256:
        errors.append("New contract hash differs from the tests-first baseline")
    for path, digest in ac2["test_file_sha256"].items():
        if manifest["test_file_sha256"].get(path) != digest:
            errors.append(f"Original test-file hash changed: {path}")
    return errors


def verify_phase(root, manifest, ac2, ac1, ac2_hash, ac1_hash):
    errors = manifest_errors(manifest, ac2, ac1, ac2_hash, ac1_hash)
    if errors:
        return errors
    errors = verify(root, manifest, phase_counts=PHASE_COUNTS)
    if root.findall(".//failure"):
        errors.append("No failures are permitted in the approved S-1 phase")
    return errors


def self_test(manifest, ac2, ac1, ac2_hash, ac1_hash):
    valid = ET.Element("testsuites")
    suite = ET.SubElement(valid, "testsuite")
    for node_id, rule in manifest["tests"].items():
        path, name = node_id.split("::", 1)
        case = ET.SubElement(suite, "testcase", classname=path[:-3].replace("/", "."), name=name)
        if rule["outcome"] == "skipped":
            ET.SubElement(case, "skipped", message=rule["reason"])

    def check(report, candidate=manifest):
        return verify_phase(report, candidate, ac2, ac1, ac2_hash, ac1_hash)

    if check(valid):
        raise ValueError("S-1 gate rejected valid control")
    reports = {}
    for label, node_id in (
        ("missing original test", sorted(set(ac2["tests"]) - PROMOTED_IDS)[0]),
        ("missing new test", sorted(NEW_TEST_IDS)[0]),
        ("missing promoted test", sorted(PROMOTED_IDS)[0]),
    ):
        altered = deepcopy(valid)
        altered[0].remove(next(c for c in altered[0] if test_id(c) == node_id))
        reports[label] = altered
    altered = deepcopy(valid)
    altered[0].append(deepcopy(altered[0][0]))
    reports["duplicate test"] = altered
    altered = deepcopy(valid)
    ET.SubElement(altered[0], "testcase", classname="tests.extra", name="test_extra")
    reports["unexpected test"] = altered
    for label, element, parent in (
        ("setup error", "error", "case"),
        ("collection error", "error", "suite"),
        ("failing case", "failure", "case"),
        ("suite failure", "failure", "suite"),
        ("extra skip", "skipped", "case"),
    ):
        altered = deepcopy(valid)
        ET.SubElement(altered[0][0] if parent == "case" else altered[0], element, message=label)
        reports[label] = altered
    altered = deepcopy(valid)
    altered.find(".//skipped").set("message", "changed reason")
    reports["changed skip reason"] = altered
    altered = deepcopy(valid)
    skipped = next(c for c in altered[0] if c.find("skipped") is not None)
    skipped.remove(skipped.find("skipped"))
    reports["unexpected S-6 pass"] = altered
    altered = deepcopy(valid)
    promoted = next(c for c in altered[0] if test_id(c) in PROMOTED_IDS)
    ET.SubElement(promoted, "failure", message="assert 501 == 200")
    reports["promoted case still stubbed"] = altered
    for label, report in reports.items():
        if not check(report):
            raise ValueError(f"S-1 gate accepted defect: {label}")

    manifests = {}
    for label, key in (("changed AC-1 manifest hash", "ac1_manifest_sha256"),
                       ("changed AC-2 manifest hash", "ac2_manifest_sha256")):
        bad = deepcopy(manifest)
        bad[key] = "0" * 64
        manifests[label] = bad
    for label, path in (("changed original file hash", sorted(ac2["test_file_sha256"])[0]),
                        ("changed new file hash", NEW_FILE)):
        bad = deepcopy(manifest)
        bad["test_file_sha256"][path] = "0" * 64
        manifests[label] = bad
    for label, node_id in (("changed original expectation", sorted(set(ac2["tests"]) - PROMOTED_IDS)[0]),
                           ("weakened new expectation", sorted(NEW_TEST_IDS)[0]),
                           ("weakened promoted expectation", sorted(PROMOTED_IDS)[0])):
        bad = deepcopy(manifest)
        bad["tests"][node_id] = {"outcome": "skipped", "reason": "unapproved"}
        manifests[label] = bad
    bad = deepcopy(manifest)
    bad["tests"]["tests/unapproved.py::test_extra"] = {"outcome": "passed"}
    manifests["unapproved additional test"] = bad
    bad = deepcopy(manifest)
    bad["new_test_ids"][0] = "tests/unapproved.py::test_extra"
    manifests["changed approved case list"] = bad
    bad = deepcopy(manifest)
    bad["promoted_test_ids"] = []
    manifests["changed promotion list"] = bad
    bad = deepcopy(manifest)
    bad["test_file_sha256"].pop(NEW_FILE)
    manifests["missing new file hash"] = bad
    for label, candidate in manifests.items():
        if not check(valid, candidate):
            raise ValueError(f"S-1 gate accepted defect: {label}")
    print(json.dumps({"valid_control": "accepted", "rejected_reports": list(reports),
                      "rejected_manifests": list(manifests)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--junit", type=Path, default=REPO / "artifacts/pytest.xml")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(MANIFEST.read_text())
        ac2_bytes, ac1_bytes = AC2_MANIFEST.read_bytes(), AC1_MANIFEST.read_bytes()
        inputs = (manifest, json.loads(ac2_bytes), json.loads(ac1_bytes),
                  hashlib.sha256(ac2_bytes).hexdigest(), hashlib.sha256(ac1_bytes).hexdigest())
        if args.self_test:
            self_test(*inputs)
            return 0
        errors = verify_phase(ET.parse(args.junit).getroot(), *inputs)
        if errors:
            print("S-1 PHASE REJECTED:\n" + "\n".join(errors), file=sys.stderr)
            return 1
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        print(f"S-1 PHASE REJECTED: {exc}", file=sys.stderr)
        return 1
    print("S-1 PHASE VERIFIED: 120 passed; zero failures; 5 exact S-6 skips. Human review remains required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
