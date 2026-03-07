"""
Phase 2 unit tests — StarGuard Mobile
21 tests: banner/HITL UI, launch contract (Artifacts.app.app:app),
relative import prefix, HEDIS measure list integrity.
No live DB/API calls.
"""
import json
import os
import tempfile

import pandas as pd
import pytest


# ── Gap suppression CRUD ───────────────────────────────────────────────────

@pytest.fixture
def gap_suppression_temp(monkeypatch):
    """Use temp file for gap suppressions."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    monkeypatch.setenv("GAP_SUPPRESSION_FILE", path)
    yield path
    try:
        os.unlink(path)
    except OSError:
        pass


def test_get_gap_suppressions_empty(gap_suppression_temp):
    """get_gap_suppressions returns [] when file empty."""
    import sys
    sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")))
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    assert hedis_gap_trail.get_gap_suppressions() == []


def test_add_gap_suppression_success(gap_suppression_temp):
    """add_gap_suppression adds rule and returns success."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    r = hedis_gap_trail.add_gap_suppression("GAP-M1", "Test")
    assert r["success"] is True
    assert r["gap_id"] == "GAP-M1"


def test_remove_gap_suppression_success(gap_suppression_temp):
    """remove_gap_suppression removes rule."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    hedis_gap_trail.add_gap_suppression("GAP-M2", "Test")
    r = hedis_gap_trail.remove_gap_suppression("GAP-M2")
    assert r["success"] is True
    assert hedis_gap_trail.get_gap_suppressions() == []


# ── Suppression banner UI ───────────────────────────────────────────────────

def test_suppression_banner_base_css_returns_tag():
    """suppression_banner_base_css returns Tag."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from suppression_banner import suppression_banner_base_css
    assert suppression_banner_base_css() is not None


def test_suppression_banner_gap_returns_tag():
    """suppression_banner(app_type=gap) returns Tag."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from suppression_banner import suppression_banner
    assert suppression_banner(app_type="gap") is not None


# ── HITL Admin View UI ──────────────────────────────────────────────────────

def test_hitl_admin_css_returns_tag():
    """hitl_admin_css returns Tag."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from hitl_admin_view import hitl_admin_css
    assert hitl_admin_css() is not None


def test_hitl_admin_panel_returns_tag():
    """hitl_admin_panel returns Tag."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from hitl_admin_view import hitl_admin_panel
    assert hitl_admin_panel(app_type="gap") is not None


# ── Launch contract (app module) ────────────────────────────────────────────

def test_app_module_exists():
    """Artifacts.app.app module can be imported."""
    import sys
    repo_root = os.path.join(os.path.dirname(__file__), "..")
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from Artifacts.app import app as app_mod
    assert app_mod is not None


def test_app_has_app_object():
    """app module exposes 'app' object (Shiny App)."""
    import sys
    repo_root = os.path.join(os.path.dirname(__file__), "..")
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from Artifacts.app.app import app
    assert app is not None
    assert hasattr(app, "ui") or hasattr(app, "_ui")


# ── Port / config (documentation) ───────────────────────────────────────────

def test_mobile_port_8000_or_8090():
    """Mobile typically uses port 8000 or 8090 (Dockerfile)."""
    dockerfile_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "Dockerfile")
    if os.path.exists(dockerfile_path):
        with open(dockerfile_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "8000" in content or "8090" in content or "EXPOSE" in content
    else:
        pytest.skip("Dockerfile not found")


# ── Relative import prefix (Artifacts.app) ───────────────────────────────────

def test_artifacts_app_has_hedis_gap_trail():
    """Artifacts.app can import hedis_gap_trail."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    import hedis_gap_trail
    assert hasattr(hedis_gap_trail, "HEDIS_MEASURES")
    assert hasattr(hedis_gap_trail, "get_gap_suppressions")


def test_artifacts_app_has_suppression_banner():
    """Artifacts.app can import suppression_banner."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    import suppression_banner
    assert hasattr(suppression_banner, "suppression_banner")


def test_artifacts_app_has_hitl_admin_view():
    """Artifacts.app can import hitl_admin_view."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    import hitl_admin_view
    assert hasattr(hitl_admin_view, "hitl_admin_panel")


# ── HEDIS measure list integrity ─────────────────────────────────────────────

def test_hedis_measures_has_cbp():
    """HEDIS_MEASURES contains CBP."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from hedis_gap_trail import HEDIS_MEASURES
    assert "CBP" in HEDIS_MEASURES


def test_hedis_measures_has_gsd():
    """HEDIS_MEASURES contains GSD."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from hedis_gap_trail import HEDIS_MEASURES
    assert "GSD" in HEDIS_MEASURES


def test_hedis_measures_count():
    """HEDIS_MEASURES has at least 10 measures."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from hedis_gap_trail import HEDIS_MEASURES
    assert len(HEDIS_MEASURES) >= 10


def test_hedis_columns_integrity():
    """HEDIS_COLUMNS has gap_id, measure_code, gap_status."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from hedis_gap_trail import HEDIS_COLUMNS
    assert "gap_id" in HEDIS_COLUMNS
    assert "measure_code" in HEDIS_COLUMNS
    assert "gap_status" in HEDIS_COLUMNS


def test_apply_gap_suppression_filter_empty(gap_suppression_temp):
    """apply_gap_suppression_filter returns empty df unchanged."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    import hedis_gap_trail
    hedis_gap_trail._SUPPRESSION_FILE = gap_suppression_temp
    hedis_gap_trail._GAP_SUPPRESSIONS_CACHE = None
    df = pd.DataFrame()
    out = hedis_gap_trail.apply_gap_suppression_filter(df)
    assert out.empty


def test_cloud_status_badge_available():
    """cloud_status_badge / starguard_mobile_badge can be imported."""
    import sys
    app_path = os.path.join(os.path.dirname(__file__), "..", "Artifacts", "app")
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    from cloud_status_badge import starguard_mobile_badge
    assert starguard_mobile_badge(mode="strip") is not None
