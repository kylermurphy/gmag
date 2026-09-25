# CLAUDE.md — gmag

Instructions for Claude Code **and** claude.ai/code (cloud) sessions working in this repo.
Both read this file. Edit it in dev-hub (`repos/gmag/CLAUDE.md`), not
here: this copy is replaced from the master at the start of each task.

## What this is
Data I/O for ground-based magnetometer arrays (CARISMA, CANOPUS, IMAGE, THEMIS and
others), loading into pandas DataFrames. Mature (since 2019, v2.0.2). Also includes an
`efield` module for deriving ground-induced electric fields from magnetometer data.

## Environment & install
- Python **>= 3.10**.
- Legacy `setup.py` build (no pyproject yet — task **GMAG-1**).
- Install: `pip install -e .`  (deps: pandas, numpy, wget, requests, cdflib, chardet)
- Data locations are set via a `gmagrc` file (see `gmagrc_example`) — it defines local
  download/cache directories and the HTTP source URLs per array.

## Commands
- Tests: none yet — task **GMAG-3** (mock the HTTP fetch; don't hit the network in tests).
- CI: none yet — task **GMAG-2**.

## Layout (`gmag/`)
- `arrays/` — per-array loaders (carisma, canopus, image, themis)
- `efield.py` — ground-induced E-field derivation (task **GMAG-5**: confirm tested/documented)
- `config.py`, `utils.py`, `Stations/` (yearly station parameter files)

## Conventions & gotchas
- Coordinate rotation: geographic (XYZ) → geomagnetic (HDZ) uses station declinations
  from the yearly `Stations/` files. THEMIS-loaded data is generally already geomagnetic
  and is not rotated.
- THEMIS module loads many non-THEMIS arrays — preserve the per-array acknowledg/attribution
  metadata returned with the data.
- `wget` is an unusual library dependency (task **GMAG-4**: consider `requests` streaming).

## Learnings

Durable facts from past tasks, promoted from `log/<ID>.md` by `mark-done` (max ~15).

_None yet._

## Task protocol (dev-hub tasks)

Tasks come from **dev-hub** (`kylermurphy/dev-hub`). Its `CLAUDE.md` → **Task protocol** is the
full, authoritative version; this is the summary. Each task is self-contained: start from its
board row alone.

- **Branch** `task/<ID>-<slug>` off the default branch; never commit to `main`.
- **First commit:** sync this file from its dev-hub master
  (`repos/gmag/CLAUDE.md`). Edit instructions in the master, never here.
- **Plan** saved to dev-hub `log/<ID>.md` before heavy work (`plan-task <ID>`); a `plan <ID>`
  dry run saves nothing. **Draft PR** following dev-hub's `templates/PULL_REQUEST_TEMPLATE.md`
  (not copied here): ID, what, why, how tested, DoD check.
- **Bookkeeping** (`log/<ID>.md`, `TASK_LOG.md` row, board Status → `WIP`) goes straight to
  dev-hub `main`. In a branch-restricted session it goes to the designated branch with an
  open PR instead (say so in chat; never merge it yourself). Only `mark-done <ID>` sets `Done`.
- **Stop states:** `Blocked` (fill `## Blocked / open questions`) or `Usage-stopped`; keep
  `Next step` current and resume with `pickup-task <ID>`.
- **Batches** (`multi-task`, or `plan-task` with several IDs): one branch
  `task/<ID>+<ID>+…-<slug>` and one PR for up to 5 simple tasks; each keeps its own log, and
  commits are prefixed with their ID. A `Blocked` task is dropped from the batch; the rest
  ship. Rules: dev-hub `CLAUDE.md` → Batches.
- **Learnings:** mark lasting findings as `Learning:` lines in the log; `mark-done` promotes
  them into `## Learnings` above (via the master).
- **Subagents:** delegate only broad/mechanical work to cheaper models, per dev-hub
  `CLAUDE.md` → Subagents; the main session does all commits and pushes.
- No test suite yet; verify by import + a manual check until GMAG-3 lands.
- Definition of done = the task's row on dev-hub `TASK_BOARD.md`.

## Task board
This repo's backlog IDs use the **`GMAG-`** prefix.
