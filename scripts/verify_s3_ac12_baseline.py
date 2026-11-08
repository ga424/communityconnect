"""Exact additive AC12 gate: 148 passes, zero failures/errors, five original skips."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET

from verify_ac1_baseline import REPO, test_id, verify
from verify_s1_baseline import manifest_errors as s1_manifest_errors

MANIFEST = REPO / "docs/evidence/s3-ac12/expected-tests.json"
S1_MANIFEST = REPO / "docs/evidence/ac4/expected-tests.json"
AC2_MANIFEST = REPO / "docs/evidence/ac2/expected-tests.json"
AC1_MANIFEST = REPO / "docs/evidence/ac1/expected-tests.json"
S1_SHA256 = "ce748625dc00f3c13cebc8f14af4af2163c0b11ebd14fedf413693056acaa644"
NEW_FILE = "tests/test_s3_community_options.py"
# Frozen in the actual tests-first commit, before the endpoint was added.
NEW_TEST_SHA256 = "b9455f1fa62b2ec439956be42dc972d31e8e5fae52117980c770d615bb70ca3d"
TESTS_FIRST_COMMIT = "5b5a1d6bf775774b58d89e206363919b3cb739bd"
PHASE_COUNTS = {"passed": 148, "skipped": 5}
NEW_TEST_IDS = {
    f"{NEW_FILE}::test_ac12_{name}"
    for name in (
        "manager_lists_only_assigned_communities", "options_multiple_assignments_sorted",
        "known_user_without_assignments",
        *(f"nonmanager_roles_have_no_options[{role}]" for role in ("resident", "board_member", "admin")),
        *(f"reject_invalid_caller[{case}]" for case in (
            "missing", "empty", "zero", "negative", "leading-zero", "plus", "decimal",
            "text", "space", "unicode-digits", "unknown", "outside-db-range", "overlong",
        )),
        "mixed_roles_offer_only_manager_assignments", "deleted_assignment_disappears",
        *(f"role_change_removes_option[{role}]" for role in ("resident", "board_member", "admin")),
        "added_assignment_appears_without_restart", "reads_leave_database_unchanged",
        "manager_does_not_gain_resident_access", "manager_unit_link_does_not_change_authority",
    )
}


def manifest_errors(manifest, s1, ac2, ac1, s1_hash, ac2_hash, ac1_hash):
    errors = s1_manifest_errors(s1, ac2, ac1, ac2_hash, ac1_hash)
    if s1_hash != S1_SHA256 or manifest.get("source_s1_manifest_sha256") != S1_SHA256:
        errors.append("Original S1 manifest must match the approved frozen hash")
    if manifest.get("tests_first_commit") != TESTS_FIRST_COMMIT:
        errors.append("Tests-first commit differs from the recorded baseline")
    new_ids = manifest.get("new_test_ids", [])
    if set(new_ids) != NEW_TEST_IDS or len(new_ids) != 28:
        errors.append("Exactly the 28 approved AC12 IDs are required")
    expected = {**s1["tests"], **{n: {"outcome": "passed"} for n in NEW_TEST_IDS}}
    if manifest.get("tests") != expected:
        errors.append("Expectations must be unchanged original125 plus28 required passes")
    expected_hashes = {**s1["test_file_sha256"], NEW_FILE: NEW_TEST_SHA256}
    if manifest.get("test_file_sha256") != expected_hashes:
        errors.append("Test hash inventory must preserve original files and frozen AC12 file")
    return errors


def verify_phase(root, manifest, s1, ac2, ac1, s1_hash, ac2_hash, ac1_hash, *, repo=REPO):
    errors = manifest_errors(manifest, s1, ac2, ac1, s1_hash, ac2_hash, ac1_hash)
    if errors:
        return errors
    errors = verify(root, manifest, repo=repo, phase_counts=PHASE_COUNTS)
    if root.findall(".//failure"):
        errors.append("No case or suite failures permitted")
    return errors


def self_test(manifest, s1, ac2, ac1, s1_hash, ac2_hash, ac1_hash):
    valid = ET.Element("testsuites")
    suite = ET.SubElement(valid, "testsuite")
    for node_id, rule in manifest["tests"].items():
        path, name = node_id.split("::", 1)
        case = ET.SubElement(suite, "testcase", classname=path[:-3].replace("/", "."), name=name)
        if rule["outcome"] == "skipped":
            ET.SubElement(case, "skipped", message=rule["reason"])

    def check(report, candidate=manifest, *, repo=REPO, source_hash=s1_hash):
        return verify_phase(report, candidate, s1, ac2, ac1, source_hash, ac2_hash, ac1_hash, repo=repo)

    if check(valid):
        raise ValueError("AC12 gate rejected valid control")
    reports = {}
    for label, node_id in (("missing original test", sorted(s1["tests"])[0]),
                           ("missing AC12 test", sorted(NEW_TEST_IDS)[0])):
        bad = deepcopy(valid)
        bad[0].remove(next(c for c in bad[0] if test_id(c) == node_id))
        reports[label] = bad
    bad = deepcopy(valid)
    bad[0].append(deepcopy(bad[0][0]))
    reports["duplicate test"] = bad
    bad = deepcopy(valid)
    ET.SubElement(bad[0], "testcase", classname="tests.extra", name="test_extra")
    reports["unexpected test"] = bad
    for label, tag, in_case in (
        ("case error", "error", True), ("suite error", "error", False),
        ("case failure", "failure", True), ("suite failure", "failure", False),
        ("extra skip", "skipped", True),
    ):
        bad = deepcopy(valid)
        ET.SubElement(bad[0][0] if in_case else bad[0], tag, message=label)
        reports[label] = bad
    bad = deepcopy(valid)
    bad.find(".//skipped").set("message", "changed reason")
    reports["changed S6 skip reason"] = bad
    bad = deepcopy(valid)
    skipped = next(c for c in bad[0] if c.find("skipped") is not None)
    skipped.remove(skipped.find("skipped"))
    reports["unexpected S6 pass"] = bad
    for label, report in reports.items():
        if not check(report):
            raise ValueError(f"AC12 gate accepted defect: {label}")

    manifests = {}
    for label, key in (("changed source hash", "source_s1_manifest_sha256"),
                       ("changed tests-first commit", "tests_first_commit")):
        bad = deepcopy(manifest)
        bad[key] = "0" * 64
        manifests[label] = bad
    for label, path in (("changed old test hash", sorted(s1["test_file_sha256"])[0]),
                        ("changed new test hash", NEW_FILE)):
        bad = deepcopy(manifest)
        bad["test_file_sha256"][path] = "0" * 64
        manifests[label] = bad
    for label, path in (("missing old hash", sorted(s1["test_file_sha256"])[0]),
                        ("missing new hash", NEW_FILE)):
        bad = deepcopy(manifest)
        bad["test_file_sha256"].pop(path)
        manifests[label] = bad
    for label, node_id in (("changed old expectation", sorted(s1["tests"])[0]),
                           ("weakened new expectation", sorted(NEW_TEST_IDS)[0])):
        bad = deepcopy(manifest)
        bad["tests"][node_id] = {"outcome": "skipped", "reason": "unapproved"}
        manifests[label] = bad
    bad = deepcopy(manifest)
    bad["new_test_ids"][0] = "tests/unapproved.py::test_extra"
    manifests["changed approved ID list"] = bad
    bad = deepcopy(manifest)
    bad["tests"]["tests/unapproved.py::test_extra"] = {"outcome": "passed"}
    manifests["extra expectation"] = bad
    for label, candidate in manifests.items():
        if not check(valid, candidate):
            raise ValueError(f"AC12 gate accepted defect: {label}")
    if not check(valid, source_hash="0" * 64):
        raise ValueError("AC12 gate accepted altered on-disk source manifest hash")
    # Exercise actual file-integrity checks against a disposable copy, not repo files.
    with TemporaryDirectory() as directory:
        scratch = Path(directory)
        for name in manifest["test_file_sha256"]:
            destination = scratch / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, destination)
        (scratch / NEW_FILE).write_text("# changed frozen contract\n")
        if not check(valid, repo=scratch):
            raise ValueError("AC12 gate accepted changed on-disk test file")
        (scratch / NEW_FILE).unlink()
        if not check(valid, repo=scratch):
            raise ValueError("AC12 gate accepted missing on-disk test file")
    print(json.dumps({"valid_control": "accepted", "rejected_reports": list(reports),
                      "rejected_manifests": list(manifests),
                      "rejected_disk_defects": ["altered source manifest", "changed test file", "missing test file"]}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--junit", type=Path, default=REPO / "artifacts/pytest.xml")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(MANIFEST.read_text())
        s1_bytes, ac2_bytes, ac1_bytes = (p.read_bytes() for p in (S1_MANIFEST, AC2_MANIFEST, AC1_MANIFEST))
        inputs = (manifest, json.loads(s1_bytes), json.loads(ac2_bytes), json.loads(ac1_bytes),
                  *(hashlib.sha256(b).hexdigest() for b in (s1_bytes, ac2_bytes, ac1_bytes)))
        if args.self_test:
            self_test(*inputs)
            return 0
        errors = verify_phase(ET.parse(args.junit).getroot(), *inputs)
        if errors:
            print("S3 AC12 PHASE REJECTED:\n" + "\n".join(errors), file=sys.stderr)
            return 1
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        print(f"S3 AC12 PHASE REJECTED: {exc}", file=sys.stderr)
        return 1
    print("S3 AC12 PHASE VERIFIED: 148 passed; zero failures/errors; 5 exact S6 skips. Human review remains separate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
