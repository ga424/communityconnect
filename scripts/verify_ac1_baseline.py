"""Fail-closed gate for the approved AC-1 phase, not full S-1 completion."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "docs/evidence/ac1/expected-tests.json"
PHASE_COUNTS = {"passed": 80, "stub_failure": 2, "skipped": 5}


def test_id(case):
    return case.get("classname", "").replace(".", "/") + ".py::" + case.get("name", "")


def verify(root, manifest, repo=REPO, *, phase_counts=None):
    counts = PHASE_COUNTS if phase_counts is None else phase_counts
    expected = manifest["tests"]
    errors = []
    if dict(Counter(item["outcome"] for item in expected.values())) != counts:
        label = "/".join(str(counts[key]) for key in ("passed", "stub_failure", "skipped"))
        errors.append(f"Manifest does not describe the approved {label} phase")
    cases = root.findall(".//testcase")
    observed = Counter(test_id(case) for case in cases)
    for missing in sorted(expected.keys() - observed.keys()):
        errors.append(f"Missing required test: {missing}")
    for extra in sorted(observed.keys() - expected.keys()):
        errors.append(f"Unexpected test: {extra}")
    for node_id, count in observed.items():
        if count != 1:
            errors.append(f"Duplicate test: {node_id}")
    if root.findall(".//error"):
        errors.append("Collection/setup/runtime error is not a deferred stub failure")
    for case in cases:
        node_id = test_id(case)
        if node_id not in expected:
            continue
        rule = expected[node_id]
        failures, skips = case.findall("failure"), case.findall("skipped")
        outcome = rule["outcome"]
        if outcome == "passed":
            if failures or skips:
                errors.append(f"Required pass failed or skipped: {node_id}")
        elif outcome == "stub_failure":
            if len(failures) != 1 or skips or not failures[0].get("message", "").startswith(
                rule["message_prefix"] + "\n"
            ):
                errors.append(f"Expected exact 501 assertion failure: {node_id}")
        elif outcome == "skipped":
            if failures or len(skips) != 1 or skips[0].get("message") != rule["reason"]:
                errors.append(f"Expected unchanged S-6 skip reason: {node_id}")
        else:
            errors.append(f"Unknown manifest outcome: {outcome}")
    for name, expected_hash in manifest["test_file_sha256"].items():
        path = repo / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            errors.append(f"Protected test file differs from red baseline: {name}")
    return errors


def self_test(manifest, *, phase_counts=None):
    # Construct a known-valid report, then prove each distinct defect is rejected.
    valid = ET.Element("testsuites")
    suite = ET.SubElement(valid, "testsuite")
    for node_id, rule in manifest["tests"].items():
        path, name = node_id.split("::", 1)
        case = ET.SubElement(suite, "testcase", classname=path[:-3].replace("/", "."), name=name)
        if rule["outcome"] == "stub_failure":
            ET.SubElement(case, "failure", message=rule["message_prefix"] + "\n + response is 501")
        elif rule["outcome"] == "skipped":
            ET.SubElement(case, "skipped", message=rule["reason"])
    if verify(valid, manifest, phase_counts=phase_counts):
        raise ValueError("Verifier self-test valid control was rejected")
    mutations = {}
    altered = deepcopy(valid)
    altered[0].remove(altered[0][0])
    mutations["missing required test"] = altered
    altered = deepcopy(valid)
    altered[0].append(deepcopy(altered[0][0]))
    mutations["duplicate test"] = altered
    altered = deepcopy(valid)
    ET.SubElement(altered[0], "testcase", classname="tests.extra", name="test_extra")
    mutations["unexpected test"] = altered
    altered = deepcopy(valid)
    ET.SubElement(altered[0][0], "error", message="setup failed")
    mutations["setup error"] = altered
    altered = deepcopy(valid)
    ET.SubElement(altered[0], "error", message="collection failed")
    mutations["collection error"] = altered
    altered = deepcopy(valid)
    ET.SubElement(altered[0][0], "failure", message="assert 500 == 200")
    mutations["unexpected failure"] = altered
    altered = deepcopy(valid)
    ET.SubElement(altered[0][0], "skipped", message="unauthorized skip")
    mutations["extra skip"] = altered
    altered = deepcopy(valid)
    altered.find(".//skipped").set("message", "changed reason")
    mutations["changed skip reason"] = altered
    altered = deepcopy(valid)
    altered.find(".//failure").set("message", "assert 500 == 404")
    mutations["non-stub deferred failure"] = altered
    altered = deepcopy(valid)
    stub = next(c for c in altered[0] if c.find("failure") is not None)
    stub.remove(stub.find("failure"))
    mutations["unexpected deferred pass"] = altered
    for label, root in mutations.items():
        if not verify(root, manifest, phase_counts=phase_counts):
            raise ValueError(f"Verifier accepted defect: {label}")
    bad_manifest = deepcopy(manifest)
    first_file = next(iter(bad_manifest["test_file_sha256"]))
    bad_manifest["test_file_sha256"][first_file] = "0" * 64
    if not any("Protected test file" in e for e in verify(valid, bad_manifest, phase_counts=phase_counts)):
        raise ValueError("Verifier accepted a test-file hash mismatch")
    print(json.dumps({"valid_control": "accepted", "rejected_defects": [*mutations, "test-file hash mismatch"]}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--junit", type=Path, default=REPO / "artifacts/pytest.xml")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(MANIFEST.read_text())
        if args.self_test:
            self_test(manifest)
            return 0
        errors = verify(ET.parse(args.junit).getroot(), manifest)
        if errors:
            print("AC-1 PHASE REJECTED:\n" + "\n".join(errors), file=sys.stderr)
            return 1
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        print(f"AC-1 PHASE REJECTED: {exc}", file=sys.stderr)
        return 1
    print("AC-1 PHASE VERIFIED: 80 passed; AC-4/AC-6 remain 501 failures; 5 exact S-6 skips. Full S-1 is incomplete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
