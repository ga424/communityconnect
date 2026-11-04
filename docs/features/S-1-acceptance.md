# S-1 acceptance baseline

Draft requirements copied from COMC-9 on November 3, 2026. Human review remains pending.

Lead: Kundan    
Reviewer: Gustavo    
Scope: Milestone 1

## Source and current state

[Revised Milestone 1 review document attached to COMC-4](https://gkms.atlassian.net/browse/COMC-4), CS690_Milestone1_CommunityConnect_Review_v2.docx, November 3, 2026. This supersedes the October 27 planning scope; the earlier attachments remain historical.

Document drafted and quality-checked; human acceptance and repository execution are not established by this Jira update. Four interviews are real per Gustavo; preserve their supplied notes and corrected participation.

## Remaining work

As a resident, I want to submit a maintenance request and see its current status in the portal, so that I do not have to email or visit the office to ask for updates.

Trace: E-1, E-2, E-12; A-1, A-6

### AC-1

Given seeded resident R1 has a unit in Mountain Ridge and Plumbing is an allowed category, When R1 posts “Kitchen sink leaks” to its requests endpoint, Then the API returns 201 with that description, status Open and the injected current UTC time, and the request appears in R1’s list.    
Trace: E-1, E-2, E-12

### AC-2

Given R1 is authorized, When R1 posts an empty or whitespace-only description, Then the API returns 422 with “Description is required” and R1’s list is unchanged.    
Trace: E-1, E-12

### AC-3

Given R1 has a request in Mountain Ridge and R2 is a resident of Pine Hollow, When R2 lists Pine Hollow requests, Then the response excludes R1’s request.    
Trace: E-12; A-6

### AC-4

Given R2 is authorized only in Pine Hollow, When R2 fetches R1’s request by ID, Then the API returns 404 with “Not found” and no request details.    
Trace: E-12; A-6

### AC-5

Given R3 is another resident in Mountain Ridge, When R3 lists its requests, Then R1’s request is absent.    
Trace: E-12; A-6

### AC-6

Given a test fixture sets R1’s request to In progress, When R1 fetches it, Then the API returns status In progress.    
Trace: E-2, E-12

Planned tests:

* AC-1: tests/test_s1_requests.py::test_ac1_resident_submits_request_shown_as_open
* AC-2: tests/test_s1_requests.py::test_ac2_blank_description_rejected_and_list_unchanged
* AC-3: tests/test_s1_requests.py::test_ac3_other_community_resident_does_not_see_request
* AC-4: tests/test_s1_requests.py::test_ac4_other_community_direct_id_returns_not_found
* AC-5: tests/test_s1_requests.py::test_ac5_neighbor_in_same_community_does_not_see_request
* AC-6: tests/test_s1_requests.py::test_ac6_resident_sees_in_progress_status

Build only this local API slice in M1 after both test baselines and plan approval. Synthetic X-User-Id is local harness only; no production authentication claim.

## Acceptance criteria

* Given the reviewed design and trace, when this story is assessed, then every listed AC maps to its planned test and its build/unbuilt scope is explicit.

## Completion evidence

Approved design, real tests and scoped implementation evidence; never close an unbuilt story as implemented.

Close only with linked artifacts and actual reviewer/check results. Use actual dates and SHAs; retain unresolved questions rather than inventing answers.
