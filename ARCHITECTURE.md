# StarGuard Mobile — Architecture

## Purpose

StarGuard Mobile is the mobile-optimized edition of the StarGuard Medicare Advantage Intelligence Platform. Purpose-built for clinical operations staff and field-based quality coordinators, it delivers HEDIS gap analysis, HCC risk stratification, Star Rating forecasting, and AI-powered insights in a responsive, touch-optimized interface. Phase 2 adds gap suppression, suppression banner, HITL Admin View, and hardening artifacts.

---

## Component Map (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      StarGuard Mobile (Shiny App)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Artifacts/app/app.py (main)                                                 │
│    ├── hedis_gap_trail.py ──────► Google Sheets + Supabase                   │
│    │   └── .gap_suppressions.json (Phase 2)                                 │
│    ├── hedis_gap_ui.py                                                       │
│    ├── cloud_status_badge.py                                                 │
│    ├── suppression_banner.py (Phase 2)                                        │
│    ├── hitl_admin_view.py (Phase 2)                                           │
│    ├── star_rating_cache.py, star_rating_cache_ui.py                         │
│    ├── intervention_optimizer.py                                              │
│    ├── pages/ (star_predictor, hedis_analyzer, ai_validation, etc.)         │
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
| `pages/` | Executive dashboard, star predictor, HEDIS analyzer, etc. |
| `utils/theme_config.py` | Mobile theme, CSS, meta |

---

## Data Flow

```
User → Hamburger Nav → Shiny UI → Server Handlers
         │
         ├──► hedis_gap_trail.push_hedis_gap() → Google Sheets + Supabase
         ├──► hedis_gap_trail.fetch_hedis_gaps() → DataFrame (suppression filter)
         ├──► get_gap_suppressions() → .gap_suppressions.json
         ├──► add/remove_gap_suppression() → JSON CRUD
         ├──► navigateTo() → Shiny.setInputValue('page_nav', page, {priority:'event'})
         └──► star_rating_cache, pages → forecasts, analytics
```

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

## Phase 2 Hardening Checklist

- [x] pyproject.toml (build, ruff, mypy, pytest)
- [x] Type hints (hedis_gap_trail, cloud_status_badge, suppression_banner, hitl_admin_view)
- [x] Unit tests (tests/test_starguard_mobile.py)
- [x] CI workflow (.github/workflows/ci.yml)
- [x] ARCHITECTURE.md

---

## Phase 3 Forward Reference

**starguard-core** — Shared library for StarGuard Desktop and Mobile. Extracts HEDIS_MEASURES, ROI calculators, and compound framework. Mobile will consume starguard-core alongside its pages/ and utils/ structure. Deferred until Phase 2 gate closes.
