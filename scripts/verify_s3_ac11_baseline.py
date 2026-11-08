"""Exact additive AC11 gate: 200 passes, zero failures/errors, five original skips."""
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
from verify_s3_ac12_baseline import manifest_errors as ac12_manifest_errors

MANIFEST = REPO / "docs/evidence/s3-ac11/expected-tests.json"
AC12_MANIFEST = REPO / "docs/evidence/s3-ac12/expected-tests.json"
S1_MANIFEST = REPO / "docs/evidence/ac4/expected-tests.json"
AC2_MANIFEST = REPO / "docs/evidence/ac2/expected-tests.json"
AC1_MANIFEST = REPO / "docs/evidence/ac1/expected-tests.json"
AC12_SHA256 = "d98bb241fa86b1968c3496a781ca3ffd41f3f4c9f01a57cba714b1591e9ac9c2"
NEW_FILE = "tests/test_s3_selected_requests.py"
# Frozen in the actual tests-first commit, before selected-community code existed.
NEW_TEST_SHA256 = "ca65fe6833b940901e51025b6f6a93b1550ecdbe8faba17199d2e8e3eaf55d38"
TESTS_FIRST_COMMIT = "359f9e6a8a8633d95ac5fbc22d8746a5f9f529d6"
PHASE_COUNTS = {"passed": 200, "skipped": 5}
NEW_TEST_IDS = set(['tests/test_s3_selected_requests.py::test_ac11_manager_reads_only_selected_community',
 'tests/test_s3_selected_requests.py::test_ac11_manager_reads_all_residents_in_selected_community',
 'tests/test_s3_selected_requests.py::test_ac11_assigned_empty_community_returns_empty_array',
 'tests/test_s3_selected_requests.py::test_ac11_switch_has_no_remembered_context',
 'tests/test_s3_selected_requests.py::test_ac11_interleaved_managers_stay_isolated',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[missing]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[empty]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[zero]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[negative]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[leading-zero]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[plus]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[decimal]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[text]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[space]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[unicode-digits]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[unknown]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[outside-db-range]',
 'tests/test_s3_selected_requests.py::test_ac11_reject_invalid_caller[overlong]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[zero]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[negative]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[leading-zero]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[plus]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[decimal]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[text]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[space]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[unicode-digits]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[outside-db-range]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[overlong]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[nonexistent]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[unassigned]',
 'tests/test_s3_selected_requests.py::test_ac11_unavailable_community_is_indistinguishable[max-valid-absent]',
 'tests/test_s3_selected_requests.py::test_ac11_identity_precedes_invalid_path[missing]',
 'tests/test_s3_selected_requests.py::test_ac11_identity_precedes_invalid_path[unknown]',
 'tests/test_s3_selected_requests.py::test_ac11_identity_precedes_invalid_path[malformed]',
 'tests/test_s3_selected_requests.py::test_ac11_nonmanager_cannot_read[resident]',
 'tests/test_s3_selected_requests.py::test_ac11_nonmanager_cannot_read[board_member]',
 'tests/test_s3_selected_requests.py::test_ac11_nonmanager_cannot_read[admin]',
 'tests/test_s3_selected_requests.py::test_ac11_known_unassigned_caller_denied',
 'tests/test_s3_selected_requests.py::test_ac11_mixed_roles_do_not_grant_manager_access',
 'tests/test_s3_selected_requests.py::test_ac11_committed_removal_denies_later_read',
 'tests/test_s3_selected_requests.py::test_ac11_committed_role_change_denies_later_read[resident]',
 'tests/test_s3_selected_requests.py::test_ac11_committed_role_change_denies_later_read[board_member]',
 'tests/test_s3_selected_requests.py::test_ac11_committed_role_change_denies_later_read[admin]',
 'tests/test_s3_selected_requests.py::test_ac11_new_assignment_authorizes_next_read',
 'tests/test_s3_selected_requests.py::test_ac11_unit_link_does_not_change_authority',
 'tests/test_s3_selected_requests.py::test_ac11_public_fields_order_status_and_utc',
 'tests/test_s3_selected_requests.py::test_ac11_reads_preserve_application_tables',
 'tests/test_s3_selected_requests.py::test_ac11_resident_routes_remain_self_only',
 'tests/test_s3_selected_requests.py::test_ac11_membership_stable_through_validation[delete]',
 'tests/test_s3_selected_requests.py::test_ac11_membership_stable_through_validation[role-change]',
 'tests/test_s3_selected_requests.py::test_ac11_validation_failure_releases_transaction',
 'tests/test_s3_selected_requests.py::test_ac11_database_failure_is_not_authorization_denial'])


def manifest_errors(manifest, ac12, s1, ac2, ac1, ac12_hash, s1_hash, ac2_hash, ac1_hash):
    errors = ac12_manifest_errors(ac12, s1, ac2, ac1, s1_hash, ac2_hash, ac1_hash)
    if ac12_hash != AC12_SHA256 or manifest.get("source_ac12_manifest_sha256") != AC12_SHA256:
        errors.append("Original AC12 manifest must match the approved frozen hash")
    if manifest.get("tests_first_commit") != TESTS_FIRST_COMMIT:
        errors.append("Tests-first commit differs from the recorded baseline")
    new_ids = manifest.get("new_test_ids", [])
    if set(new_ids) != NEW_TEST_IDS or len(new_ids) != 52:
        errors.append("Exactly the 52 approved AC11 IDs are required")
    expected = {**ac12["tests"], **{n: {"outcome": "passed"} for n in NEW_TEST_IDS}}
    if manifest.get("tests") != expected:
        errors.append("Expectations must be unchanged original153 plus52 required passes")
    expected_hashes = {**ac12["test_file_sha256"], NEW_FILE: NEW_TEST_SHA256}
    if manifest.get("test_file_sha256") != expected_hashes:
        errors.append("Test hash inventory must preserve original files and frozen AC11 file")
    return errors


def verify_phase(root, manifest, ac12, s1, ac2, ac1, ac12_hash, s1_hash, ac2_hash, ac1_hash, *, repo=REPO):
    errors = manifest_errors(manifest, ac12, s1, ac2, ac1, ac12_hash, s1_hash, ac2_hash, ac1_hash)
    if errors:
        return errors
    errors = verify(root, manifest, repo=repo, phase_counts=PHASE_COUNTS)
    if root.findall(".//failure"):
        errors.append("No case or suite failures permitted")
    return errors


def self_test(manifest, ac12, s1, ac2, ac1, ac12_hash, s1_hash, ac2_hash, ac1_hash):
    valid = ET.Element("testsuites")
    suite = ET.SubElement(valid, "testsuite")
    for node_id, rule in manifest["tests"].items():
        path, name = node_id.split("::", 1)
        case = ET.SubElement(suite, "testcase", classname=path[:-3].replace("/", "."), name=name)
        if rule["outcome"] == "skipped":
            ET.SubElement(case, "skipped", message=rule["reason"])

    def check(report, candidate=manifest, *, repo=REPO, source_hash=ac12_hash):
        return verify_phase(report, candidate, ac12, s1, ac2, ac1, source_hash, s1_hash, ac2_hash, ac1_hash, repo=repo)

    if check(valid):
        raise ValueError("AC11 gate rejected valid control")
    reports = {}
    for label, node_id in (("missing original test", sorted(ac12["tests"])[0]),
                           ("missing AC11 test", sorted(NEW_TEST_IDS)[0])):
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
            raise ValueError(f"AC11 gate accepted defect: {label}")

    manifests = {}
    for label, key in (("changed source hash", "source_ac12_manifest_sha256"),
                       ("changed tests-first commit", "tests_first_commit")):
        bad = deepcopy(manifest)
        bad[key] = "0" * 64
        manifests[label] = bad
    for label, path in (("changed old test hash", sorted(ac12["test_file_sha256"])[0]),
                        ("changed new test hash", NEW_FILE)):
        bad = deepcopy(manifest)
        bad["test_file_sha256"][path] = "0" * 64
        manifests[label] = bad
    for label, path in (("missing old hash", sorted(ac12["test_file_sha256"])[0]),
                        ("missing new hash", NEW_FILE)):
        bad = deepcopy(manifest)
        bad["test_file_sha256"].pop(path)
        manifests[label] = bad
    for label, node_id in (("changed old expectation", sorted(ac12["tests"])[0]),
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
            raise ValueError(f"AC11 gate accepted defect: {label}")
    if not check(valid, source_hash="0" * 64):
        raise ValueError("AC11 gate accepted altered on-disk source manifest hash")
    # Exercise actual file-integrity checks against a disposable copy, not repo files.
    with TemporaryDirectory() as directory:
        scratch = Path(directory)
        for name in manifest["test_file_sha256"]:
            destination = scratch / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, destination)
        (scratch / NEW_FILE).write_text("# changed frozen contract\n")
        if not check(valid, repo=scratch):
            raise ValueError("AC11 gate accepted changed on-disk test file")
        (scratch / NEW_FILE).unlink()
        if not check(valid, repo=scratch):
            raise ValueError("AC11 gate accepted missing on-disk test file")
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
        ac12_bytes, s1_bytes, ac2_bytes, ac1_bytes = (p.read_bytes() for p in (AC12_MANIFEST, S1_MANIFEST, AC2_MANIFEST, AC1_MANIFEST))
        inputs = (manifest, json.loads(ac12_bytes), json.loads(s1_bytes), json.loads(ac2_bytes), json.loads(ac1_bytes),
                  *(hashlib.sha256(b).hexdigest() for b in (ac12_bytes, s1_bytes, ac2_bytes, ac1_bytes)))
        if args.self_test:
            self_test(*inputs)
            return 0
        errors = verify_phase(ET.parse(args.junit).getroot(), *inputs)
        if errors:
            print("S3 AC11 PHASE REJECTED:\n" + "\n".join(errors), file=sys.stderr)
            return 1
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        print(f"S3 AC11 PHASE REJECTED: {exc}", file=sys.stderr)
        return 1
    print("S3 AC11 PHASE VERIFIED: 200 passed; zero failures/errors; 5 exact S6 skips. Human review remains separate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
