# ============================================================
# Climate Risk India — Multi-Hazard Real Estate Risk Analyser
# ============================================================
# Covers: Drought, Flood, Heatwave, Cyclone, Landslide
# Cities: 32 Indian cities
# Years:  2015–2023
#
# HOW TO RUN:
# CLI:  python3 main.py
#       (Install first: pip3 install colorama pandas)
# ============================================================

import os, sys, pandas as pd

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system(f"{sys.executable} -m pip install colorama -q")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

# ── Data paths ────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "data", "outputs")

composite  = pd.read_csv(os.path.join(OUT, "composite_risk_scores.csv"))
drought_df = pd.read_csv(os.path.join(OUT, "drought_risk_scores.csv"))
flood_df   = pd.read_csv(os.path.join(OUT, "flood_risk_scores.csv"))
heat_df    = pd.read_csv(os.path.join(OUT, "heatwave_risk_scores.csv"))
cyclone_df = pd.read_csv(os.path.join(OUT, "cyclone_risk_scores.csv"))
slide_df   = pd.read_csv(os.path.join(OUT, "landslide_risk_scores.csv"))

# Normalise keys
for df in [composite, drought_df, flood_df, heat_df, cyclone_df, slide_df]:
    df["_key"] = df["city"].str.strip().str.lower()

CITIES     = sorted(composite["city"].unique())
YEARS      = sorted(composite["year"].unique())
MIN_Y, MAX_Y = YEARS[0], YEARS[-1]

HAZARDS = [
    ("drought_risk_score",   "🌵", "Drought  "),
    ("flood_risk_score",     "🌊", "Flood    "),
    ("heatwave_risk_score",  "🌡️ ", "Heatwave "),
    ("cyclone_risk_score",   "🌀", "Cyclone  "),
    ("landslide_risk_score", "⛰️ ", "Landslide"),
]

# ── Helpers ───────────────────────────────────────────────────
def cat_from_score(score):
    if score <= 25:   return "LOW"
    elif score <= 50: return "MEDIUM"
    elif score <= 75: return "HIGH"
    else:             return "VERY HIGH"

def clr(category):
    c = str(category).upper()
    if c == "VERY HIGH": return Fore.RED
    if c == "HIGH":      return Fore.YELLOW
    if c == "MEDIUM":    return Fore.CYAN
    return Fore.GREEN

def emoji(category):
    c = str(category).upper()
    if c == "VERY HIGH": return "🔴"
    if c == "HIGH":      return "🟠"
    if c == "MEDIUM":    return "🟡"
    return "🟢"

def bar(score, width=24):
    filled = int(round(min(max(score, 0), 100) / 100 * width))
    return f"[{'█' * filled}{'░' * (width - filled)}] {int(round(score)):3d}"

def get_row(city_key, year):
    """Return composite row as dict, or None."""
    r = composite[(composite["_key"] == city_key) & (composite["year"] == year)]
    return r.iloc[0] if not r.empty else None

def get_prob(df, city_key, year, prob_col):
    r = df[(df["_key"] == city_key) & (df["year"] == year)]
    if r.empty or prob_col not in r.columns: return None
    v = r.iloc[0][prob_col]
    return float(v) if pd.notna(v) else None

def get_recommendation(composite_score, scores):
    cat = cat_from_score(composite_score)
    dominant = max(scores, key=scores.get)
    dom_name = dominant.replace("_risk_score","").title()
    base = {
        "LOW":       "LOW RISK — Standard loan processing applicable.",
        "MEDIUM":    "MEDIUM RISK — Annual climate review clause recommended.",
        "HIGH":      "HIGH RISK — Climate risk insurance clause required before loan approval.",
        "VERY HIGH": "VERY HIGH RISK — Independent climate assessment mandatory before approval.",
    }[cat]
    if scores[dominant] > 0:
        note = f"Primary concern: {dom_name} exposure ({scores[dominant]:.1f}/100) requires attention."
    else:
        note = "All individual hazard scores are low."
    return cat, base, note

def divider(char="━", width=68):
    print(Fore.WHITE + Style.BRIGHT + char * width)

def resolve_city(user_input):
    """Accept number (1-32) or name (case-insensitive). Returns city name or None."""
    s = user_input.strip()
    if s.isdigit():
        idx = int(s) - 1
        if 0 <= idx < len(CITIES):
            return CITIES[idx]
        return None
    match = [c for c in CITIES if c.lower() == s.lower()]
    return match[0] if match else None

# ── Display: numbered city list ───────────────────────────────
def show_city_list():
    print(Fore.WHITE + "\n  Available cities:")
    cols = 4
    for i, city in enumerate(CITIES):
        num = f"{i+1:2d}. {city:<14s}"
        print(Fore.CYAN + f"  {num}", end="")
        if (i + 1) % cols == 0:
            print()
    print()

# ── Display: single city + year ───────────────────────────────
def show_profile(city_name, year):
    key = city_name.lower()
    row = get_row(key, year)
    if row is None:
        print(Fore.RED + f"\n  No data for {city_name} in {year}.")
        return

    scores = {h[0]: float(row.get(h[0], 0) or 0) for h in HAZARDS}
    comp_score = float(row["composite_score"])
    comp_cat   = str(row["composite_category"])
    cat, rec_base, rec_note = get_recommendation(comp_score, scores)

    print()
    divider()
    print(Fore.WHITE + Style.BRIGHT + f"  RISK PROFILE: {city_name} — {year}")
    divider()

    # Individual hazard scores
    print(Fore.WHITE + "\n  ── INDIVIDUAL HAZARD SCORES ──────────────────────────────────")
    for col, ico, label in HAZARDS:
        sc   = scores[col]
        cat_h = cat_from_score(sc)
        c     = clr(cat_h)
        print(f"  {ico} {label}  :  {c}{sc:5.1f} / 100   [ {cat_h:<9s}]{Fore.WHITE}")

    # Composite
    print(Fore.WHITE + "\n  ── COMPOSITE SCORE ───────────────────────────────────────────")
    c = clr(comp_cat)
    print(f"  OVERALL RISK SCORE    :  {c}{Style.BRIGHT}{comp_score:.1f} / 100")
    print(f"  RISK CATEGORY         :  {c}{emoji(comp_cat)} {comp_cat}")

    # Visual bars
    print(Fore.WHITE + "\n  ── VISUAL RISK METER ─────────────────────────────────────────")
    for col, _ico, label in HAZARDS:
        sc = scores[col]
        c  = clr(cat_from_score(sc))
        print(f"  {label}  {c}{bar(sc)}{Fore.WHITE}")
    c = clr(comp_cat)
    print(f"  COMPOSITE  {c}{bar(comp_score)}{Fore.WHITE}")

    # Recommendation
    print(Fore.WHITE + "\n  ── BANK / INSURER RECOMMENDATION ────────────────────────────")
    c = clr(cat)
    print(f"  {c}{emoji(cat)} {rec_base}")
    print(f"  {Fore.WHITE}{rec_note}")

    print()
    divider()

# ── Display: all years for a city ────────────────────────────
def show_history(city_name):
    key  = city_name.lower()
    rows = composite[composite["_key"] == key].sort_values("year")
    if rows.empty:
        print(Fore.RED + f"\n  No data for {city_name}.")
        return

    print(Fore.WHITE + Style.BRIGHT + f"\n  RISK HISTORY: {city_name} ({MIN_Y}–{MAX_Y})")
    hdr = f"  ┌──────┬──────────┬───────┬──────────┬─────────┬───────────┬───────────┬───────────┐"
    sep = f"  ├──────┼──────────┼───────┼──────────┼─────────┼───────────┼───────────┼───────────┤"
    ftr = f"  └──────┴──────────┴───────┴──────────┴─────────┴───────────┴───────────┴───────────┘"
    print(hdr)
    print(f"  │ Year │ Drought  │ Flood │ Heatwave │ Cyclone │ Landslide │ Composite │ Category  │")
    print(sep)

    best_row, worst_row = None, None
    best_sc, worst_sc = 999, -1

    for _, r in rows.iterrows():
        yr  = int(r["year"])
        d   = float(r.get("drought_risk_score",  0) or 0)
        fl  = float(r.get("flood_risk_score",    0) or 0)
        h   = float(r.get("heatwave_risk_score", 0) or 0)
        cy  = float(r.get("cyclone_risk_score",  0) or 0)
        ls  = float(r.get("landslide_risk_score",0) or 0)
        co  = float(r["composite_score"])
        cat = str(r["composite_category"])
        c   = clr(cat)
        print(f"  │ {yr} │ {c}{d:>6.1f}{Fore.WHITE}   │{c}{fl:>5.1f}{Fore.WHITE}  │ {c}{h:>6.1f}{Fore.WHITE}   │ {c}{cy:>5.1f}{Fore.WHITE}   │ {c}{ls:>7.1f}{Fore.WHITE}   │ {c}{co:>7.1f}{Fore.WHITE}   │ {c}{cat:<9s}{Fore.WHITE} │")
        if co < best_sc:  best_sc,  best_row  = co, r
        if co > worst_sc: worst_sc, worst_row = co, r

    print(ftr)
    if worst_row is not None:
        c = clr(worst_row["composite_category"])
        print(f"  Worst year: {int(worst_row['year'])}  ({c}{worst_row['composite_score']:.1f} — {worst_row['composite_category']}{Fore.WHITE})")
    if best_row is not None:
        c = clr(best_row["composite_category"])
        print(f"  Best year:  {int(best_row['year'])}  ({c}{best_row['composite_score']:.1f} — {best_row['composite_category']}{Fore.WHITE})")
    print()

# ── Display: compare two cities ───────────────────────────────
def show_compare(city1, year, city2):
    row1 = get_row(city1.lower(), year)
    row2 = get_row(city2.lower(), year)
    if row1 is None or row2 is None:
        print(Fore.RED + "\n  No data for one or both cities.")
        return

    print(Fore.WHITE + Style.BRIGHT + f"\n  COMPARISON: {city1} vs {city2} — {year}")
    print(f"  {'Metric':<20s}  {'':>2s}{city1:<18s}  {'':>2s}{city2}")
    print("  " + "─" * 60)

    for col, ico, label in HAZARDS:
        s1 = float(row1.get(col, 0) or 0)
        s2 = float(row2.get(col, 0) or 0)
        c1, c2 = clr(cat_from_score(s1)), clr(cat_from_score(s2))
        print(f"  {ico} {label:<14s}  {c1}{s1:6.1f}{Fore.WHITE}              {c2}{s2:6.1f}{Fore.WHITE}")

    cs1, cs2 = float(row1["composite_score"]), float(row2["composite_score"])
    cat1, cat2 = str(row1["composite_category"]), str(row2["composite_category"])
    c1, c2 = clr(cat1), clr(cat2)
    print("  " + "─" * 60)
    print(f"  {'COMPOSITE':<20s}  {c1}{cs1:6.1f} {emoji(cat1)} {cat1:<9s}{Fore.WHITE}  {c2}{cs2:6.1f} {emoji(cat2)} {cat2}")
    diff = abs(cs1 - cs2)
    riskier = city1 if cs1 > cs2 else city2
    print(f"\n  {clr('HIGH')}{riskier} is riskier by {diff:.1f} points.{Fore.WHITE}\n")

# ── Banner ────────────────────────────────────────────────────
def show_banner():
    print()
    print(Fore.CYAN + Style.BRIGHT + "╔══════════════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + Style.BRIGHT + "        CLIMATE RISK INDIA — MULTI-HAZARD RISK ANALYSER          " + Fore.CYAN + "║")
    print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + "        Drought | Flood | Heatwave | Cyclone | Landslide          " + Fore.CYAN + "║")
    print(Fore.CYAN + Style.BRIGHT + "╚══════════════════════════════════════════════════════════════════╝")
    print(Fore.WHITE + "  32 Indian cities  |  2015–2023  |  For real estate risk assessment")

# ── Main loop ─────────────────────────────────────────────────
def main():
    show_banner()

    while True:
        show_city_list()
        city_input = input(Fore.WHITE + "Enter city name or number: ").strip()
        city_name  = resolve_city(city_input)

        if not city_name:
            print(Fore.RED + f"\n  '{city_input}' not recognised. Please try again.")
            continue

        year_input = input(Fore.WHITE + f"Enter year ({MIN_Y}–{MAX_Y}) or press Enter for latest ({MAX_Y}): ").strip()
        if year_input == "":
            year = MAX_Y
        else:
            try:
                year = int(year_input)
                if year not in YEARS:
                    print(Fore.RED + f"\n  Year out of range. Valid: {MIN_Y}–{MAX_Y}\n")
                    continue
            except ValueError:
                print(Fore.RED + "\n  Invalid year.\n")
                continue

        show_profile(city_name, year)

        while True:
            print(Fore.WHITE + "  Options:")
            print("    [1] View all years for this city")
            print("    [2] Compare with another city")
            print("    [3] Search a new city")
            print("    [4] Exit")
            opt = input(Fore.WHITE + "\n  Choice: ").strip()

            if opt == "1":
                show_history(city_name)
            elif opt == "2":
                show_city_list()
                city2_input = input(Fore.WHITE + "Enter city to compare with: ").strip()
                city2 = resolve_city(city2_input)
                if city2:
                    show_compare(city_name, year, city2)
                else:
                    print(Fore.RED + f"\n  '{city2_input}' not found.\n")
            elif opt == "3":
                break
            elif opt == "4":
                print(Fore.CYAN + "\n  Goodbye! 👋\n")
                sys.exit(0)
            else:
                print(Fore.RED + "  Invalid option.\n")

if __name__ == "__main__":
    main()
