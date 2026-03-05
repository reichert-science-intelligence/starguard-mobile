#!/usr/bin/env python3
"""
fix_mobile_generate.py — Add Claude AI Generate button to Mobile HEDIS Gap panel

Patches:
1. hedis_gap_ui.py — add "🤖 Generate Recommendation" button before gap_claude_rec textarea
2. app.py — add JS handler for loading + set-rec
3. app.py — add generate server handler that calls Claude

Run from starguard-mobile/Artifacts/app dir:
    python fix_mobile_generate.py
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ─── 1. hedis_gap_ui.py: textarea + button ───────────────────────────────────
HEDIS_GAP_UI_OLD = '''            ui.input_text_area(
                "gap_claude_rec", "Claude AI Recommendation",
                placeholder="Paste Claude-generated care gap recommendation...",
                rows=3
            ),'''

HEDIS_GAP_UI_NEW = '''            ui.div(
                ui.input_action_button(
                    "btn_generate_gap_rec",
                    "🤖 Generate Recommendation",
                    class_="btn btn-outline-primary btn-sm mb-2",
                    style="background:#4A3E8F; color:#fff; border-color:#D4AF37;"
                ),
                class_="gap-generate-row"
            ),
            ui.input_text_area(
                "gap_claude_rec", "Claude AI Recommendation",
                placeholder="Fill gap details above, click 🤖 Generate — or paste manually.",
                rows=3
            ),'''

# ─── 2. app.py: JS handler — insert after cloud_status_css() ───────────────────
JS_ANCHOR = "        cloud_status_css(),\n        ui.tags.style(\"\"\""
JS_INSERT = '''        cloud_status_css(),
        ui.tags.script("""
            (function(){
                if (typeof Shiny !== 'undefined') {
                    Shiny.addCustomMessageHandler('gap_show_loading', function(msg) {
                        var ta = document.getElementById('gap_claude_rec') || document.querySelector('textarea[id$="gap_claude_rec"]');
                        if (ta) ta.value = '⏳ Claude is generating...';
                    });
                    Shiny.addCustomMessageHandler('gap_set_rec', function(msg) {
                        var v = (msg && msg.value) || msg || '';
                        var ta = document.getElementById('gap_claude_rec') || document.querySelector('textarea[id$="gap_claude_rec"]');
                        if (ta) ta.value = v;
                        try { Shiny.setInputValue('gap_claude_rec', v); } catch(e) {}
                    });
                }
            })();
        """),
        ui.tags.style("""'''

# ─── 3. app.py: generate server handler ─────────────────────────────────────
SERVER_ANCHOR = '''    @reactive.effect
    @reactive.event(input.btn_push_gap)
    def _push_gap():
        if input.page_nav() != "hedisgaps":
            return'''

SERVER_INSERT = '''
    @reactive.effect
    @reactive.event(input.btn_generate_gap_rec)
    def _generate_gap_rec():
        if input.page_nav() != "hedisgaps":
            return
        session.send_custom_message("gap_show_loading", {})
        try:
            import anthropic
            client = anthropic.Anthropic()
            member_id = input.gap_member_id() or "N/A"
            member_name = input.gap_member_name() or "N/A"
            measure_code = input.gap_measure_code() or "N/A"
            intervention = input.gap_intervention() or "Outreach"
            star_impact = input.gap_star_impact() or 3
            prompt = f"""Generate a concise care gap recommendation (2-4 sentences) for:
Member: {member_id} — {member_name}
HEDIS Measure: {measure_code}
Intervention: {intervention}
Star Impact: {star_impact}

Write a practical, actionable recommendation for closing this gap. Return only the text, no preamble."""
            resp = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            rec = resp.content[0].text.strip() if resp.content else ""
            ui.update_text_area("gap_claude_rec", value=rec)
        except Exception as e:
            err_msg = str(e)
            if "ANTHROPIC" in err_msg.upper() or "api_key" in err_msg.lower():
                err_msg = "ANTHROPIC_API_KEY not set. Add to .env or Space secrets."
            ui.update_text_area("gap_claude_rec", value=f"Error: {err_msg}")

    @reactive.effect
    @reactive.event(input.btn_push_gap)
    def _push_gap():
        if input.page_nav() != "hedisgaps":
            return'''


def main():
    print("Applying Mobile Generate patches...")

    # 1. hedis_gap_ui.py
    ui_path = BASE / "hedis_gap_ui.py"
    if not ui_path.exists():
        print("[FAIL] hedis_gap_ui.py not found")
        return
    ui_text = ui_path.read_text(encoding="utf-8")
    if HEDIS_GAP_UI_NEW.strip() in ui_text:
        print("[OK] gap_claude_rec + button: already patched")
    elif HEDIS_GAP_UI_OLD.strip() in ui_text:
        ui_text = ui_text.replace(HEDIS_GAP_UI_OLD, HEDIS_GAP_UI_NEW)
        ui_path.write_text(ui_text, encoding="utf-8")
        print("[OK] gap_claude_rec + button: patched")
    else:
        print("[WARN] gap_claude_rec textarea not found — manual edit needed")

    # 2. app.py — JS handler
    app_path = BASE / "app.py"
    if not app_path.exists():
        print("[FAIL] app.py not found")
        return
    app_text = app_path.read_text(encoding="utf-8")

    if "gap_show_loading" in app_text and "gap_set_rec" in app_text:
        print("[OK] JS handler: already patched")
    elif JS_ANCHOR in app_text:
        app_text = app_text.replace(JS_ANCHOR, JS_INSERT, 1)
        app_path.write_text(app_text, encoding="utf-8")
        print("[OK] JS handler: patched")
    else:
        print("[WARN] JS anchor not found (cloud_status_css + ui.tags.style)")

    # 3. app.py — generate server handler
    if "def _generate_gap_rec():" in app_text:
        print("[OK] generate server handler: already patched")
    elif SERVER_ANCHOR.strip() in app_text:
        app_text = app_text.replace(SERVER_ANCHOR, SERVER_INSERT)
        app_path.write_text(app_text, encoding="utf-8")
        print("[OK] generate server handler: inserted")
    else:
        print("[WARN] server anchor not found (@reactive.event(input.btn_push_gap) def _push_gap)")

    print("\nDone. Restart: shiny run app.py --port 8090 --reload")


if __name__ == "__main__":
    main()
