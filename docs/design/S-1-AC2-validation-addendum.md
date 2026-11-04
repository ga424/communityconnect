# S-1 AC-2 validation addendum — approved November 4, 2026

Authority: Gustavo's explicit approval of [AC-2 packet v1](../plans/AC-2-approval.md), recorded in [the actual prompt](../../prompts/2026-11-04-ac2-approval.txt). This adds the missing text-representability rule to S-1 D2 while preserving the original design and all original acceptance criteria. No wider S-1 or teammate approval is implied.

After caller, path/membership and exact JSON/body-shape validation:

1. Strip description with Python `str.strip()`; empty returns 422 `{"detail":"Description is required"}`.
2. Check Python `len()` against `MAX_DESCRIPTION_CHARS`; oversized returns 422 `{"detail":"Description is too long"}`.
3. A nonempty, in-limit description must contain Unicode scalar values and exclude U+0000. Reject NUL or unpaired surrogate code points with 422 `{"detail":"Invalid request body"}` before any insert. Do not sanitize, replace, truncate or store escaped substitutes.
4. Check the existing exact case-sensitive category allow-list; mismatch returns 422 `{"detail":"Unknown category"}`.

An unsupported description therefore precedes an unknown category; an oversized description precedes unsupported-text rejection. Valid accented text and supplementary Unicode, including correctly decoded surrogate pairs representing emoji, remain valid. All rejections preserve the entire request table and the resident's list, including seeded existing rows. Successful creation still persists exactly one request and returns the existing public fields.

The guard validates description text before the database call. Database outages, schema errors and unrelated persistence failures must not be caught and misreported as input validation errors. Existing transaction rollback and access rules are unchanged. No new category policy, endpoint, schema, dependency, authentication or provider behavior is introduced.
