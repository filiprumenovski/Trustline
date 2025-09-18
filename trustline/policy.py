import pandas as pd

def _get_nudge_level(prob: float) -> str:
    if prob < 0.30: return "encourage"
    elif 0.30 <= prob < 0.60: return "redirect"
    else: return "alert"

def _calculate_suggested_cap(expected_spend: float) -> int:
    return int(round(max(20, min(60, 0.33 * expected_spend))))

def generate_nudge(prob: float, top_category: str, expected_spend_total: float, window_start: pd.Timestamp) -> dict:
    level, cap = _get_nudge_level(prob), _calculate_suggested_cap(expected_spend_total)
    start_time, end_time = window_start, window_start + pd.Timedelta(hours=3)
    start_str, end_str = f"{start_time.strftime('%-I%p').lower()}", f"{end_time.strftime('%-I%p').lower()}"
    window_str, json_window_str = f"{start_str}-{end_str}", f"{start_time.strftime('%a %H:%M')}-{end_time.strftime('%H:%M')}"

    message = ""
    if level == "encourage": message = f"On track! Your buffer is growing. Keep this pace {window_str}."
    elif level == "redirect": message = f"Heads up: {top_category.capitalize()} spending can spike {window_str}. Skip one and bank ."
    elif level == "alert": message = f"High risk {window_str}: {top_category.capitalize()} could push you off target. Cap at  to stay steady."

    return {"window": json_window_str, "prob": round(prob, 2), "top_category": top_category, "expected_spend": round(expected_spend_total, 2), "suggested_cap": cap, "level": level, "message": message}
