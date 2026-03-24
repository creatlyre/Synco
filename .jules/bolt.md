## 2024-05-24 - Pre-compile regex for performance
**Learning:** Instantiating and compiling regular expressions inside tight loops or frequently called functions adds significant, unnecessary CPU overhead.
**Action:** When a static set of string patterns is used repeatedly (like locale keywords in NLP), compile them to `re.Pattern` objects during class initialization or at the module level.

## 2024-05-23 - [Precompute Monthly Overview Variables]
**Learning:** In hot loops such as calculating monthly budget overviews, fetching repeated values from a dictionary using `get()` and constantly evaluating defaults within the loop creates measurable processing overhead (especially when multiplied by many users or years).
**Action:** When a loop iterates over fixed bounds (e.g., months 1-12), use a pre-allocated array of corresponding size and pre-compute repetitive math operations. In Python, list indexing combined with ahead-of-time calculations is substantially faster than inline dictionary lookups and conditional default evaluations.

## 2024-05-25 - [Pre-normalize Static Keywords / Resolve N+1 Queries]
**Learning:** Performing data normalization (like stripping diacritics via `unicodedata.normalize`) on static reference maps during hot loop categorization is very CPU intensive. In addition, fetching reference data inside a loop (N+1 query) degrades batch operation performance.
**Action:** When categorizing items or expenses against a static set of keywords, pre-normalize the static reference map at module initialization time (or map creation). When processing a batch of items, fetch reference mappings (e.g. `sections` and `overrides`) before the loop and pass them through to helper functions.