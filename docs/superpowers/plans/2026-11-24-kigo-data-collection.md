# Kigo Data Collection — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-time data kit for Kigo, an English app for kids aged 6–10. It covers English curriculum and teaching methods, plus Vietnamese folktales, history before 1945 and culture. Every item carries its source and a license label, and the kit is ready to upload to Google Drive.

**Architecture:** A small Python package (`kigo_collect`) handles the mechanical work: polite fetching with a raw cache, parsing the Cambridge wordlist, the MediaWiki and OpenAlex clients, the entry file format, validation, building the index and syncing the owner's review back. Claude, working inside Claude Code, writes the content: method cards, retellings and summaries. It writes them through the same entry format, and the validator gates them.

**Tech Stack:** Python 3.13 (installed), `requests`, `pypdf`, `PyYAML`, `pytest`. Git 2.48 (installed). The project folder is not a git repo yet.

**Spec:** `docs/superpowers/specs/2026-11-24-kigo-data-collection-design.md`

## Global Constraints

- License labels are exactly `usable` (🟢), `reference` (🟡) and `excluded` (🔴).
- Every entry's front matter has these fields: `id, title, category, tags_method, tags_topic, age_range, cefr_level, license_label, license_detail, source_url, retrieved_at, reviewed`. Vietnam entries also have `type: legend | history`.
- Public content only. Respect robots.txt, never bypass logins or bot blocks, and never scrape Google Trends.
- The HTTP User-Agent is the generic `kigo-collect/0.1 (research script)`. It contains no personal details.
- Khan Academy content is never copied. Only a description of its design approach goes in.
- Wikipedia (CC BY-SA) counts as `reference`, so content taken from it is always rewritten.
- The Cambridge word list (word, part of speech, level, topic) can be used directly. Do not copy example sentences, pictures, document layout or exam papers.
- History covers only the period **before 1945** and follows the mainstream Vietnamese historical account. Every name, year and event in a history entry must have a cited source link.
- Retellings may simplify the source but never invent. Any added detail is wrapped in `[thêm]…[/thêm]` and listed in `added_details`.
- Retellings for kids: a 3–5 sentence summary plus a read-aloud version of about 3 minutes (400–500 words), split into scenes, in Vietnamese.
- Do the core set first and make every field complete: the whole Cambridge list, 10–15 methods and about 30 of the best-known stories. Then expand to the full estimate: 60–100 stories, 30–50 history items, 30–50 culture topics and 50–100 papers.
- Output root: `kigo-data/`. `index.csv` is written as UTF-8 with BOM, so Google Sheets and Excel display Vietnamese correctly.
- No Claude API and no Google API.

## Review Focus

1. **Vietnamese text in `index.csv` opened in Excel or Google Sheets** → the diacritics display correctly. Test: `test_index_csv_has_bom_and_vietnamese` (Task 3).
2. **Vietnamese titles turned into file names on Windows** (`Sơn Tinh – Thủy Tinh`, `đ`, `?`, `:`) → an ASCII slug that is a valid Windows file name and has no collisions. Tests: `test_slugify_vietnamese`, `test_slug_collision_gets_suffix` (Task 2).
3. **Owner edits the CSV badly** (an unknown `id`, a label like `green`, an empty row) → the bad rows are reported and skipped, and no Markdown file is changed for those rows. Test: `test_sync_rejects_bad_rows_without_touching_files` (Task 3).
4. **Re-running a fetch after a network error or partway through** → pages already cached are not downloaded again, and a failed request is retried and then reported, not fatal for the whole batch. Tests: `test_fetch_uses_cache`, `test_fetch_retries_then_raises` (Task 4).
5. **A history entry with no source, or a retelling with an unmarked addition** → the validator fails it. Tests: `test_history_requires_source`, `test_added_details_must_match_markers` (Task 2).

---

## File Structure

```
kid-go/
  pyproject.toml                      # package + deps + pytest config
  tools/kigo_collect/
    __init__.py
    entry.py        # Entry dataclass, slugify, read/write Markdown+YAML, validate()
    licenses.py     # classify_license()
    index.py        # build_index(), sync_review()
    fetch.py        # polite cached HTTP get
    cambridge.py    # parse wordlist PDF text → rows
    mediawiki.py    # vi.wikipedia / vi.wikisource client
    openalex.py     # open-access paper search
    cli.py          # `python -m kigo_collect <cmd>`
    __main__.py
  tests/            # one test_*.py per module, fixtures in tests/fixtures/
  kigo-data/        # output (layout in spec §7)
    content-lists/  # chosen topic lists (Task 7)
```

---

### Task 1: Project scaffold and git

**Files:**
- Create: `pyproject.toml`, `.gitignore`, `tools/kigo_collect/__init__.py`, `tests/test_smoke.py`

**Interfaces:**
- Produces: an importable package `kigo_collect` (src path `tools/`), and `pytest` running from the repo root.

- [ ] **Step 1:** Run `git init`, then create a `.gitignore` containing `__pycache__/`, `.venv/`, `kigo-data/raw/` and `.pytest_cache/`. The raw cache stays local, and the processed output is committed.
- [ ] **Step 2:** Write `pyproject.toml` with dependencies `requests`, `pypdf`, `PyYAML`, dev dependency `pytest`, and `[tool.pytest.ini_options] pythonpath = ["tools"]`.
- [ ] **Step 3:** Write `tests/test_smoke.py::test_import`, which does `import kigo_collect`.
- [ ] **Step 4:** Run `python -m venv .venv; .venv\Scripts\pip install -e .[dev]; .venv\Scripts\pytest -q`. Expected: 1 passed.
- [ ] **Step 5:** Commit the spec, the plan and the scaffold: `chore: scaffold kigo_collect`.

### Task 2: Entry format and validator

**Files:**
- Create: `tools/kigo_collect/entry.py`, `tests/test_entry.py`

**Interfaces:**
- Produces:
  - `REQUIRED_FIELDS: tuple[str, ...]` holds the 12 fields from Global Constraints.
  - `LABELS = ("usable", "reference", "excluded")`
  - `@dataclass Entry(meta: dict, body: str)`
  - `slugify(text: str) -> str` strips diacritics, maps `đ/Đ`→`d`, lowercases, joins words with `-` and keeps only `[a-z0-9-]`.
  - `unique_path(dir: Path, slug: str) -> Path` appends `-2`, `-3` and so on if the file exists.
  - `write_entry(path: Path, entry: Entry) -> None` and `read_entry(path: Path) -> Entry` store a `---` YAML block followed by a Markdown body, in UTF-8.
  - `validate(entry: Entry) -> list[str]` returns a list of error messages, empty if the entry is valid.
- `source_url` is a **list** of URLs, because one entry may draw on several sources.

- [ ] **Step 1: Write the failing tests**
  - `test_slugify_vietnamese`: `slugify("Sơn Tinh – Thủy Tinh") == "son-tinh-thuy-tinh"`, `slugify("Đền Hùng?") == "den-hung"`
  - `test_slug_collision_gets_suffix`: in a temp folder that already has `tam-cam.md`, `unique_path(...)` returns `tam-cam-2.md`
  - `test_roundtrip`: `write_entry` then `read_entry` returns equal meta and body, Vietnamese text included
  - `test_missing_field_reported`: meta without `license_label` → the errors include `"missing field: license_label"`
  - `test_bad_label_reported`: `license_label: "green"` → the errors include `"bad license_label: green"`
  - `test_history_requires_source`: `category: "vietnam/history"` with `source_url: []` → the errors include `"history entry needs source_url"`
  - `test_vietnam_requires_type`: `category` starts with `vietnam/` and `type` is not one of `legend` or `history` → error
  - `test_added_details_must_match_markers`: the body has `[thêm]Gióng nói: "..."[/thêm]` but `added_details: []` → error `"unlisted [thêm] markers: 1"`
- [ ] **Step 2:** Run `pytest tests/test_entry.py -v`. Expected: FAIL (ImportError).
- [ ] **Step 3:** Implement `entry.py` with the signatures above. Use `unicodedata.normalize("NFD")` for slugify, and `yaml.safe_dump(allow_unicode=True, sort_keys=False)`.
- [ ] **Step 4:** Run `pytest tests/test_entry.py -v`. Expected: all pass.
- [ ] **Step 5:** Commit: `feat: entry format and validator`.

### Task 3: License classifier, index and review sync

**Files:**
- Create: `tools/kigo_collect/licenses.py`, `tools/kigo_collect/index.py`, `tests/test_licenses.py`, `tests/test_index.py`

**Interfaces:**
- Consumes: `read_entry`, `write_entry`, `REQUIRED_FIELDS`, `LABELS` (Task 2)
- Produces:
  - `classify_license(raw: str | None, *, ideas_only: bool = False) -> tuple[str, str]` returns `(label, detail)`.
  - `build_index(root: Path) -> int` walks `root/**/*.md` (skipping `raw/`), writes `root/index.csv` in `utf-8-sig` with one column per required field plus `type` and `path`, and returns the row count. List fields are joined with `; `.
  - `sync_review(root: Path, csv_path: Path) -> SyncReport` copies only `reviewed` and `license_label` from the CSV into each file's front matter. `SyncReport(updated: int, errors: list[str])`.

- [ ] **Step 1: Write the failing tests**
  - `test_cc_by_usable`: `classify_license("cc-by")[0] == "usable"`; the same holds for `"cc0"`, `"public-domain"` and `"OGL"`
  - `test_cc_by_sa_reference`: `"cc-by-sa"` → `"reference"`
  - `test_nc_excluded`: `"cc-by-nc-sa"` → `"excluded"`
  - `test_unknown_excluded`: `None` → `"excluded"`
  - `test_nc_ideas_only_reference`: `classify_license("cc-by-nc", ideas_only=True)[0] == "reference"`. This is for research summaries, which take only the conclusions. *(Claude's call, applying the spec §4 meaning of 🟡.)*
  - `test_index_csv_has_bom_and_vietnamese`: given 2 entries, one titled `"Tấm Cám"`, the file bytes start with `b"\xef\xbb\xbf"`, `"Tấm Cám"` decodes correctly, and the function returns 2
  - `test_sync_updates_reviewed`: in the CSV, `reviewed=true` and `license_label=excluded` for one id → that file's meta is updated, and its body is byte-identical
  - `test_sync_rejects_bad_rows_without_touching_files`: the rows are an unknown id, `license_label=green` and an empty row → `report.errors` has 3 entries, `report.updated == 0`, and the file mtimes are unchanged
- [ ] **Step 2:** Run `pytest tests/test_licenses.py tests/test_index.py -v`. Expected: FAIL.
- [ ] **Step 3:** Implement both modules. `classify_license` normalises the input to lowercase and checks NC before SA before BY.
- [ ] **Step 4:** Run the same command. Expected: all pass.
- [ ] **Step 5:** Commit: `feat: license labels, index.csv, review sync`.

### Task 4: Polite cached fetcher

**Files:**
- Create: `tools/kigo_collect/fetch.py`, `tests/test_fetch.py`

**Interfaces:**
- Produces: `fetch(url: str, *, cache_dir: Path, params: dict | None = None, retries: int = 3, delay: float = 1.0) -> FetchResult`, where `FetchResult(url: str, path: Path, from_cache: bool, retrieved_at: str)`. The cache key is the sha1 of the URL plus its sorted params. A `<key>.meta.json` file next to the cached body stores the url and retrieved_at. A robots.txt check uses `urllib.robotparser`, and a URL that robots.txt disallows raises `FetchBlocked`. After the retries run out it raises `FetchFailed`. The session is injectable for tests: `session: requests.Session | None = None`.

- [ ] **Step 1: Write the failing tests** (they use a fake session object, no network)
  - `test_fetch_uses_cache`: the second call returns `from_cache=True`, and the fake session saw exactly 1 GET
  - `test_fetch_retries_then_raises`: a session that always raises `ConnectionError` → `FetchFailed` after 3 attempts (`delay=0`)
  - `test_robots_disallow_blocks`: robots text `Disallow: /` → `FetchBlocked`
  - `test_user_agent_generic`: the GET headers have `User-Agent == "kigo-collect/0.1 (research script)"`
- [ ] **Step 2:** Run `pytest tests/test_fetch.py -v`. Expected: FAIL.
- [ ] **Step 3:** Implement `fetch.py`.
- [ ] **Step 4:** Run the same command. Expected: all pass.
- [ ] **Step 5:** Commit: `feat: polite cached fetch`.

### Task 5: Source clients — Cambridge, MediaWiki, OpenAlex

**Files:**
- Create: `tools/kigo_collect/cambridge.py`, `mediawiki.py`, `openalex.py`, `tests/test_cambridge.py`, `tests/test_mediawiki.py`, `tests/test_openalex.py`, `tests/fixtures/` (a small text sample of the wordlist and saved JSON responses)

**Interfaces:**
- Consumes: `fetch` (Task 4), `classify_license` (Task 3)
- Produces:
  - `parse_wordlist_text(text: str, level: str) -> list[WordRow]`, where `WordRow(word: str, pos: str, level: str, topic: str | None)` and `level` is one of `"starters" | "movers" | "flyers"`. `extract_pdf_text(pdf: Path) -> str` uses pypdf.
  - `get_page(site: str, title: str, *, cache_dir: Path) -> WikiPage`, where `site` is one of `"vi.wikipedia" | "vi.wikisource"` and `WikiPage(title, url, text, categories: list[str], license_raw: str)`. It uses `action=query&prop=extracts|categories&explaintext=1&format=json`. `license_raw` is `"cc-by-sa"` for Wikipedia. For Wikisource it is `"public-domain"` when a category contains `"phạm vi công cộng"` or `"PD"` (case-insensitive), and otherwise `None`.
  - `search_works(query: str, *, cache_dir: Path, per_page: int = 25) -> list[Paper]`, where `Paper(title, year, doi, url, license_raw, abstract)`. It filters with `is_oa:true`. The abstract is rebuilt from `abstract_inverted_index`.

- [ ] **Step 1: Write the failing tests** against the fixtures
  - `test_parse_wordlist_basic`: the lines `"apple (n)\nafter (prep)\nask (v)"` → 3 rows, the first being `("apple","n","starters",None)`
  - `test_parse_wordlist_skips_headers_and_page_numbers`: lines like `"Pre A1 Starters"` or `"12"` are not counted as words
  - `test_parse_wordlist_multiword`: `"ice cream (n)"` → word `"ice cream"`
  - `test_wikipedia_license_reference`: page fixture → `classify_license(page.license_raw)[0] == "reference"`
  - `test_wikisource_pd_category`: a fixture with the category `"Thể loại:Tác phẩm phạm vi công cộng"` → `license_raw == "public-domain"`
  - `test_openalex_abstract_rebuilt`: inverted index `{"Phonics":[0],"works":[1]}` → `"Phonics works"`
- [ ] **Step 2:** Run `pytest tests/test_cambridge.py tests/test_mediawiki.py tests/test_openalex.py -v`. Expected: FAIL.
- [ ] **Step 3:** Implement the three modules.
- [ ] **Step 4:** Run the same command. Expected: all pass.
- [ ] **Step 5:** Commit: `feat: cambridge, mediawiki, openalex clients`.

### Task 6: CLI

**Files:**
- Create: `tools/kigo_collect/cli.py`, `tools/kigo_collect/__main__.py`, `tests/test_cli.py`

**Interfaces:**
- Consumes: everything above.
- Produces the commands for `python -m kigo_collect` (default `--root kigo-data`):
  - `wordlist --pdf <path> --level <starters|movers|flyers>` writes `english/curriculum/vocabulary.csv` (columns `word,pos,level,topic`, utf-8-sig) and merges levels without duplicate `(word,pos,level)` rows.
  - `wiki --site <...> --title <...>` and `wiki --site <...> --titles-file <txt>` cache raw pages under `raw/wiki/` and print the title, url and license label for each.
  - `papers --query <...>` caches results under `raw/openalex/` and prints a summary table.
  - `check` runs `validate` on every entry and exits with code 1 if any errors are found, printing `path: message`.
  - `index` runs `build_index` and prints the count.
  - `sync-review --csv <path>` runs `sync_review` and prints the report.
- [ ] **Step 1:** Write the tests: `test_check_exit_code` (one invalid entry → exit 1), `test_wordlist_merges_levels` (2 runs → no duplicate rows), and `test_index_command_counts`.
- [ ] **Step 2:** Run `pytest tests/test_cli.py -v`. Expected: FAIL.
- [ ] **Step 3:** Implement with `argparse`.
- [ ] **Step 4:** Run `pytest -q`. Expected: the whole suite passes.
- [ ] **Step 5:** Commit: `feat: kigo_collect CLI`.

---

**From here on, the tasks are content work by Claude.** Each one is gated the same way: `python -m kigo_collect check` exits 0, the counts match, and the work is committed. Claude writes the files with the Write tool, using the entry format from Task 2.

### Task 7: Content lists — what to collect

**Files:**
- Create: `kigo-data/content-lists/{methods,folktales,history,culture,research-queries}.txt` (one item per line, the core-set items marked `*`)

- [ ] **Step 1:** Write the lists. methods has 10–15 items (phonics, TPR, storytelling, songs/chants, CLIL, spaced repetition, gamification, task-based learning, picture-word/flashcards, dialogic reading, mastery learning, ...). folktales has 60–100 titles, chosen by checking which ones exist on vi.wikipedia or vi.wikisource. history has 30–50 people or events before 1945, each with its year. culture has 30–50 topics, including 12 con giáp. research-queries has about 15 OpenAlex queries.
- [ ] **Step 2:** Check that each folktale and history title resolves with `python -m kigo_collect wiki --site vi.wikipedia --titles-file ...`. Drop any that don't resolve, or replace them with a title that does.
- [ ] **Step 3:** Commit: `data: content lists`.

### Task 8: English curriculum (core)

**Files:**
- Create: `kigo-data/english/curriculum/vocabulary.csv`, `vocabulary.md` (an entry with the usage note from the spec), `cefr-young-learners.md`, `phonics-letters-and-sounds.md`

- [ ] **Step 1:** Download the official Cambridge Young Learners wordlist PDF(s) from cambridgeenglish.org into `kigo-data/raw/cambridge/`, and run `wordlist` once per level.
- [ ] **Step 2:** Verify that the row count per level is plausible (about 1,400–1,500 in total). Spot-check 20 random rows against the PDF.
- [ ] **Step 3:** Write the CEFR and phonics entries. Check the actual license of Letters and Sounds on the gov.uk page and record it in `license_detail`. Label it `usable` only if the page says OGL.
- [ ] **Step 4:** Run `check`, then commit: `data: english curriculum`.

### Task 9: Method cards and research (core)

**Files:**
- Create: `kigo-data/english/methods/<slug>.md` (one per method), `kigo-data/english/research/<slug>.md`, `kigo-data/english/design-references/khan-academy-kids.md`

- [ ] **Step 1:** Run `papers` for each line of research-queries. Pick 50–100 reviews or meta-analyses, and write a summary entry for each paper (label from `classify_license(..., ideas_only=True)`).
- [ ] **Step 2:** Write one method card per method. Each card has these sections: *Mô tả*, *Độ tuổi phù hợp*, *Bằng chứng nghiên cứu* (linking the research entries by id), *Áp dụng vào video/bài học*, *Ví dụ hoạt động* and *Nguồn*. Set `tags_method` to the method's slug.
- [ ] **Step 3:** Write the Khan Academy / Khan Academy Kids design note, describing the approach only, with label `reference`.
- [ ] **Step 4:** Run `check`, then commit: `data: methods and research`.

### Task 10: Vietnamese folktales

**Files:**
- Create: `kigo-data/vietnam/folktales/<slug>.md`

- [ ] **Step 1:** Do the core-set (`*`) stories first. For each one, fetch the sources and write the entry. It needs `type: legend`, and the body has these sections in order: *Tóm tắt* (3–5 câu), *Nhân vật*, *Bài học*, *Kể cho bé* (400–500 words, split into `### Cảnh 1..n`), *Từ tiếng Anh liên quan* (linking to words in vocabulary.csv where possible) and *Lưu ý độ tuổi* (frightening or violent details, and how they were softened).
- [ ] **Step 2:** Fact-check pass for each story. Compare the retelling with the fetched source, wrap anything that isn't in the source in `[thêm]`, and list it in `added_details`.
- [ ] **Step 3:** Run `check` and commit the core set. Then repeat steps 1–2 for the rest of the list, committing every 10 or so.

### Task 11: Vietnamese history (before 1945)

**Files:**
- Create: `kigo-data/vietnam/history/<slug>.md`

- [ ] **Step 1:** For each item, write the entry with `type: history` (or `legend` for figures such as the Hùng Vương origin story). Every name, year and event in the body carries an inline footnote link to a `source_url` item. Include *Tóm tắt*, *Kể cho bé* and *Lưu ý độ tuổi* as in Task 10.
- [ ] **Step 2:** Fact-check pass. Any sentence without a source is either removed or marked `[thêm]`. Append the open doubts to `kigo-data/vietnam/history/_can-kiem-tra.md`, a list for a history teacher to review.
- [ ] **Step 3:** Run `check`, then commit: `data: vietnam history`.

### Task 12: Vietnamese culture, trends and handover

**Files:**
- Create: `kigo-data/vietnam/culture/<slug>.md`, `kigo-data/english/trends/apps.md`, `kigo-data/README.md` (how to use and review the kit)

- [ ] **Step 1:** Write the culture entries in the same shape as the folktales, with `type: history` for practices with documented origins and `type: legend` for origin myths. 12 con giáp gets one entry per animal.
- [ ] **Step 2:** Write `trends/apps.md`, a feature analysis of about 10 kids' English apps popular in Vietnam and worldwide (from their public store pages). If the owner has put Google Trends exports in `raw/trends/`, summarise them too. Otherwise note that this part was skipped.
- [ ] **Step 3:** Run `index` and then `check`. Expected: exit 0, and the count matches the number of entry files.
- [ ] **Step 4:** Write `kigo-data/README.md`, covering the folder layout, what each label means, how to review in Sheets, and how to run `sync-review`. Note for Drive: no Google Drive for desktop mount was found on this machine (only the C: and D: drives), so upload `kigo-data/` by hand, or install Drive for desktop and copy the folder in.
- [ ] **Step 5:** Commit: `data: culture, trends, index, README`.
