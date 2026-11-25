# Codex Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give Codex everything it needs, inside the repo, to finish the rest of the Kigo data collection while Claude only spot-checks.

**Architecture:** Two Markdown files, no code. `kigo-data/PROGRESS.md` tells Codex what is done and what is next (Claude's own ledger is git-ignored, so Codex cannot see it). `AGENTS.md` at the repo root, which Codex reads automatically, holds the rules, the entry format, the batch routine and the stop conditions. The existing `kigo_collect` package does fetching and validation and is not changed.

**Tech Stack:** Markdown; `python -m kigo_collect check` and `pytest` for the existing gates; git.

**Spec:** `docs/superpowers/specs/2026-11-25-codex-handoff-design.md` (the original data plan is `docs/superpowers/plans/2026-11-24-kigo-data-collection.md`, Tasks 10–12).

## Global Constraints

- History covers only the period before 1945; every name, year and event has a source link inside the entry; doubts go to `kigo-data/vietnam/history/_can-kiem-tra.md`.
- Default license label is `reference`; never `usable` unless the page states a license that allows commercial use (CC0, CC BY, public domain, OGL).
- Codex works on branch `feature/data-collection-tools`, never touches `main`, commits every ~10 entries, and does not push.
- Fetch pages only through `kigo_collect.fetch` (polite, cached, robots.txt); needs network access, which the owner must enable.
- The existing 39 folktale entries and Tasks 1–9 are not redone.
- Ruling made during execution: the package CLI `wiki` command prints only title, url and label, so Codex could not read sources. Added a standalone `tools/read_source.py` (not part of `kigo_collect`; no automated test; run by hand on a wiki page, a plain URL and a missing page) and pointed AGENTS.md at it.
- Output language of entries: Vietnamese. The 12 required front-matter fields and `type: legend | history` for `vietnam/` entries come from the data plan's Global Constraints.

## Review Focus

1. **Codex labels Wikipedia or a commercial page `usable`** → AGENTS.md says the default is `reference` and lists what counts as `usable`. Pinned by Task 2, Step 3 (grep).
2. **Codex invents a detail to fill a gap** → AGENTS.md says no source, no sentence; additions only in `[thêm]…[/thêm]` plus `added_details`; never pad. Pinned by Task 2, Step 3.
3. **Codex cannot tell what is done and redoes or skips entries** → PROGRESS.md lists every finished folktale slug and the next batch. Pinned by Task 1, Step 2.
4. **No network access in Codex's sandbox** → AGENTS.md says stop and report; never write from memory. Pinned by Task 2, Step 3.
5. **Codex pushes, switches branch, or edits `tools/`** → AGENTS.md forbids it. Pinned by Task 2, Step 3.

---

### Task 1: `kigo-data/PROGRESS.md`

**Files:**
- Create: `kigo-data/PROGRESS.md`

**Interfaces:**
- Consumes: `kigo-data/vietnam/folktales/*.md` (39 files), `kigo-data/content-lists/{folktales,history,culture}.txt`.
- Produces: the file AGENTS.md (Task 2) tells Codex to read first and update at the end of every batch.

- [ ] **Step 1: Write `kigo-data/PROGRESS.md` in Vietnamese** with these sections, in order: *Cách dùng* (read first; update and commit together with each batch); *Folktales – đã xong* (all 39 slugs, one per line, split into "bộ lõi" 29 and "ngoài lõi đợt 8" 10; the slug is the file name without `.md`); *Folktales – đợt kế tiếp* (the next 10 titles in order from `folktales.txt`, starting at `Quan án xử kiện`); *Folktales – còn lại sau đó* (count, and the 3 reference books last); *History* (not started; start with the `*` lines of `history.txt`); *Culture, apps, index, README* (not started; order from the data plan Task 12); *Nhật ký kiểm của Claude* (an empty table: đợt, ngày, mục đã kiểm, kết quả, ghi chú).
- [ ] **Step 2: Verify every existing folktale file is listed**

Run: `for f in kigo-data/vietnam/folktales/*.md; do s=$(basename "$f" .md); grep -q "$s" kigo-data/PROGRESS.md || echo "MISSING $s"; done`
Expected: no output.
- [ ] **Step 3: Verify the next batch matches the list**

Run: `sed -n '43,52p' kigo-data/content-lists/folktales.txt`
Expected: the same 10 titles, in the same order, as *đợt kế tiếp*: `Quan án xử kiện`, `Hồn Trương Ba, da hàng thịt`, `Ngưu Lang Chức Nữ`, `Dã tràng`, `Lý Ông Trọng`, `Thuồng luồng`, `Rồng Việt Nam`, `Liễu Hạnh Công chúa`, `Tứ bất tử`, `Bà Mụ`.

### Task 2: `AGENTS.md`

**Files:**
- Create: `AGENTS.md` (repo root)

**Interfaces:**
- Consumes: `kigo-data/PROGRESS.md` (Task 1); the entry format and rules in the data plan; three example entries `kigo-data/vietnam/folktales/{ba-giai,tu-thuc,thuan-thien-kiem}.md`.
- Produces: the instructions Codex follows. Claude's spot-check in the spec reads the same rules.

- [ ] **Step 1: Write `AGENTS.md` in Vietnamese** (short, bullet style) with these sections in order:
  1. *Mục tiêu* – what Kigo is (English app, Vietnamese kids 6–10, corgi mascot Kigo, 12 zodiac animals) and what this kit is for, in 3 lines.
  2. *Việc cần làm* – the remaining work and its order: rest of `folktales.txt`, then `history.txt` (core `*` first), then Task 12 (culture, `trends/apps.md`, `index`, `README`), with the data plan path and Tasks 10–12 as the detailed brief. Read `kigo-data/PROGRESS.md` first.
  3. *Định dạng một mục* – the 12 required front-matter fields, `type`, `added_details`, a front-matter template copied from `thuan-thien-kiem.md`, the body sections in order (*Tóm tắt, Nhân vật, Bài học, Kể cho bé, Từ tiếng Anh liên quan, Lưu ý độ tuổi, Nguồn*), and the three example files.
  4. *Quy tắc nội dung* – each as one bullet: new words, never copy a source sentence or dialogue; 400–500 words in *Kể cho bé* when the source is rich enough, otherwise shorter and never padded; no source, no sentence; any addition is `[thêm]…[/thêm]` plus `added_details` (empty list `[]` when none); variants only when attributed to their source; soften violence, nudity, people-as-property and stigmatising words by omission or rewording and say so in *Lưu ý độ tuổi*; list every place the sources contradict each other and do not resolve it by guessing; English words from Cambridge Starters/Movers/Flyers (`kigo-data/english/curriculum/vocabulary.csv`), others marked as outside the list; no first-person "mình" in entries; history only before 1945 with an inline source link after every name, year and event, doubts in `_can-kiem-tra.md`.
  5. *Giấy phép* – `reference` by default; `usable` only for CC0, CC BY, public domain, OGL as stated on the page; Wikipedia is CC BY-SA so `reference`; commercial or unknown-author pages `reference`; write the reason in `license_detail`.
  6. *Quy trình một đợt* – pick the next ~10 items from PROGRESS.md; fetch each source with `python -m kigo_collect wiki --site vi.wikipedia --title "..."` (or `kigo_collect.fetch.fetch` for other pages); write the entries; run `python -m kigo_collect check` (expect `0 problem(s)`) and `python -m pytest -q`; update PROGRESS.md; `git add` and commit with the message style `data: <what> batch N` (no Claude co-author line, since Codex wrote it); stop and tell the owner the batch is ready for Claude's check.
  7. *Dừng và hỏi* – stop and ask the owner when: the network is blocked or a page cannot be opened (never write from memory); a source is too thin to retell; content is sensitive for children; the license is unclear; `check` fails in a way you cannot fix by editing entries.
  8. *Không được làm* – push, switch or merge branches, touch `main`; edit `tools/` or `tests/`; redo finished entries; change a license label to `usable` without the page saying so; commit `kigo-data/raw/`.
  9. *Claude sẽ kiểm* – one paragraph: Claude opens the `source_url` pages of sampled entries and compares every name, year and detail, so list every page used in `source_url` and say in *Nguồn* which part came from which page.
- [ ] **Step 2: Check the existing gates still pass**

Run: `python -m kigo_collect check` and `python -m pytest -q`
Expected: `0 problem(s)` and all tests pass (no code changed).
- [ ] **Step 3: Verify the five Review Focus rules are present**

Run: `grep -c -E "reference|usable" AGENTS.md; grep -c "không bịa\|no source\|Không có nguồn" AGENTS.md; grep -c "\[thêm\]" AGENTS.md; grep -c -i "mạng" AGENTS.md; grep -c -i "không push\|không được.*push" AGENTS.md; grep -c "tools/" AGENTS.md`
Expected: every count is at least 1.
- [ ] **Step 4: Verify the three example files exist**

Run: `ls kigo-data/vietnam/folktales/ba-giai.md kigo-data/vietnam/folktales/tu-thuc.md kigo-data/vietnam/folktales/thuan-thien-kiem.md`
Expected: all three listed.
- [ ] **Step 5: Commit the spec, plan and both files**

```bash
git add AGENTS.md kigo-data/PROGRESS.md docs/superpowers/specs/2026-11-25-codex-handoff-design.md docs/superpowers/plans/2026-11-25-codex-handoff.md
git commit -m "docs: hand-off to Codex (AGENTS.md, PROGRESS.md, design, plan)"
```
Expected: one commit; `git status --short` shows only the untracked `kigo-data/index.csv`.
