# StarGuard Mobile — Architecture

## Purpose

StarGuard Mobile is the mobile-optimized edition of the StarGuard Medicare Advantage Intelligence Platform. Purpose-built for clinical operations staff and field-based quality coordinators, it delivers HEDIS gap analysis, HCC risk stratification, Star Rating forecasting, and AI-powered insights in a responsive, touch-optimized interface. Primary use case: point-of-care gap alerts, real-time member targeting, and AI insights in the field. Phase 2 adds gap suppression, suppression banner, HITL Admin View, and hardening artifacts.

---

## Design Decisions

**starguard-core** — Shared library introduced to consolidate HEDIS gap logic across Desktop and Mobile. Single source of truth for gap CRUD and measure definitions. Mobile adopts typed `MemberRecord` for consistent gap handling.

---

## Component Map (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      StarGuard Mobile (Shiny App)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Artifacts/app/app.py (main)                                                 │
│    ├── starguard_core.hedis.gap_trail ──► Google Sheets + Supabase          │
│    │   logic/ hedis_gap_trail.py deleted                                     │
│    │   └── .gap_suppressions.json (Phase 2)                                  │
│    ├── hedis_gap_ui.py                                                       │
│    ├── cloud_status_badge.py                                                 │
│    ├── suppression_banner.py (Phase 2)                                       │
│    ├── hitl_admin_view.py (Phase 2)                                          │
│    ├── star_rating_cache.py, star_rating_cache_ui.py                         │
│    ├── intervention_optimizer.py                                             │
│    ├── pages/ (star_predictor, hedis_analyzer, ai_validation, etc.)          │
│    └── utils/theme_config.py                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Module Reference

| Module | Role |
|--------|------|
| `Artifacts/app/app.py` | Main Shiny UI + server, hamburger nav |
| `hedis_gap_trail.py` | HEDIS gap CRUD, Google Sheets, Supabase, Phase 2 gap suppression |
| `hedis_gap_ui.py` | HEDIS gap panel UI |
| `cloud_status_badge.py` | Cloud services badge (starguard_mobile_badge) |
| `suppression_banner.py` | Phase 2 gap suppression banner |
| `hitl_admin_view.py` | Phase 2 HITL Admin View (gap suppressions) |
| `star_rating_cache.py` | Star rating forecast cache |
| `star_rating_cache_ui.py` | Star cache panel UI |
| `intervention_optimizer.py` | Intervention optimizer |
| `pages/` | Executive dashboard, star predictor, HEDIS analyzer, ai_validation, etc. |
| `utils/theme_config.py` | Mobile theme, CSS, meta, iOS Safari overrides |

---

## Data Flow

```
User → Hamburger Nav → Shiny UI → Server Handlers
         │
         ├──► starguard_core.hedis.gap_trail.push_hedis_gap() → Google Sheets + Supabase
         ├──► starguard_core.hedis.gap_trail.fetch_hedis_gaps() → DataFrame (suppression filter)
         ├──► get_gap_suppressions() → .gap_suppressions.json
         ├──► add/remove_gap_suppression() → JSON CRUD
         ├──► navigateTo() → Shiny.setInputValue('page_nav', page, {priority:'event'})
         └──► star_rating_cache, pages → forecasts, analytics
```

---

## Supabase Schema

| Table | Purpose |
|------|---------|
| `hedis_gap_trail` | Parallel write from hedis_gap_trail.py; mirrors Google Sheets HEDIS gap records |

Primary persistence: Google Sheets. Supabase used for parallel write when `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set. Same schema as StarGuard Desktop — shared tables.

---

## Deployment Topology

| Environment | Host | Port | Entry |
|-------------|------|------|-------|
| Local | localhost | 8000 | `shiny run Artifacts.app.app:app` |
| HuggingFace Spaces | rreichert/starguardai | 8000 | Docker, PYTHONPATH=Artifacts/app |
| Docker | python:3.11-slim | 8000 | `shiny run Artifacts.app.app:app` |

---

## Dependency Graph

```
Artifacts.app.app
  ├── shiny, shinyswatch
  ├── hedis_gap_trail, hedis_gap_ui
  ├── cloud_status_badge, suppression_banner, hitl_admin_view
  ├── star_rating_cache, star_rating_cache_ui
  ├── intervention_optimizer
  ├── pages/* (star_predictor, hedis_analyzer, ai_validation, etc.)
  ├── utils.theme_config
  ├── pandas, plotly
  └── gspread, supabase, google-auth
```

---

## Configuration

| Variable | Purpose |
|----------|---------|
| `GSHEETS_CREDS_JSON` | Google Sheets credentials (HF Secret) |
| `HEDIS_SHEET_ID` | Sheet name (default: StarGuard_HEDIS_Gap_Tracker) |
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Supabase parallel write |
| `GAP_SUPPRESSION_FILE` | Phase 2 gap suppression JSON path |
| `ANTHROPIC_API_KEY` | Claude API |
| `PYTHONPATH` | Set to Artifacts/app for Docker |

---

## 4. starguard-core Import Chain

| starguard_core module | Replaces |
|----------------------|----------|
| `starguard_core.hedis.gap_trail` | `hedis_gap_trail.py` |

**Install:** `pip install starguard-core` (or `pip install -e path/to/starguard-core` for local dev)

**Usage:**
```python
from starguard_core.hedis.gap_trail import push_hedis_gap, fetch_hedis_gaps
```

---

## Supabase Schema

| Table | Purpose |
|-------|---------|
| `hedis_gap_trail` | Parallel write from starguard_core.hedis.gap_trail (HEDIS gap records) |

Google Sheets is source of truth; Supabase receives fire-and-forget parallel writes when `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set. Shared schema with StarGuard Desktop.

---

## Phase 2 Hardening Checklist

- [x] pyproject.toml (build, ruff, mypy, pytest)
- [x] Type hints (hedis_gap_trail, cloud_status_badge, suppression_banner, hitl_admin_view)
- [x] Unit tests (tests/test_starguard_mobile.py) — 19 tests — 19 tests
- [x] CI workflow (.github/workflows/ci.yml) — strict mode
- [x] ARCHITECTURE.md
- [x] starguard-core import chain

---

## Phase 3 Complete

**starguard-core** — Shared library integrated. Mobile consumes `starguard_core.hedis.gap_trail` with typed `MemberRecord`. `hedis_gap_trail.py` deleted.

---

## Rollback Procedure

**Revert → push → auto-redeploy.** No manual HuggingFace intervention needed in the normal case.

1. `git revert <commit>` (or `git revert HEAD` for last commit)
2. `git push origin main`
3. CI runs tests; deploy job syncs to HuggingFace Space
4. Space rebuilds from updated repo

If deploy fails, add `HF_TOKEN` secret (Settings → Secrets) with write access to the Space. One token covers all three repos.

---

## Rollback Procedure

If a bad deploy reaches production:

1. **Revert** the commit: `git revert HEAD --no-edit`
2. **Push** to main: `git push origin main`
3. **Auto-redeploy** — GitHub Actions deploy job runs on push; HuggingFace Space rebuilds from the reverted commit.

No manual HuggingFace intervention needed in the normal case.

---

*Phase 3 Complete*
