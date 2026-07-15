# ============================================================
# Climate Risk India — Multi-Hazard Real Estate Risk Analyser
# ============================================================
# Covers: Drought, Flood, Heatwave, Cyclone, Landslide
# Cities: 32 Indian cities
# Years:  2015–2023
#
# HOW TO RUN:
# Web:  streamlit run app.py
#       Then open http://localhost:8501
#       (Install: pip3 install streamlit plotly pandas)
# ============================================================

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Climate Risk India",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paths ─────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "data", "outputs")

# ── Load data (cached) ────────────────────────────────────────
@st.cache_data
def load_data():
    comp     = pd.read_csv(os.path.join(OUT, "composite_risk_scores.csv"))
    drought  = pd.read_csv(os.path.join(OUT, "drought_risk_scores.csv"))
    flood    = pd.read_csv(os.path.join(OUT, "flood_risk_scores.csv"))
    heatwave = pd.read_csv(os.path.join(OUT, "heatwave_risk_scores.csv"))
    cyclone  = pd.read_csv(os.path.join(OUT, "cyclone_risk_scores.csv"))
    landslide= pd.read_csv(os.path.join(OUT, "landslide_risk_scores.csv"))
    
    # Merge Delhi districts as cities
    delhi_path = os.path.join(OUT, "delhi", "delhi_composite_scores.csv")
    if os.path.exists(delhi_path):
        d_comp = pd.read_csv(delhi_path)
        d_comp = d_comp.rename(columns={
            "district": "city",
            "delhi_composite_score": "composite_score",
            "delhi_composite_category": "composite_category"
        })
        comp = pd.concat([comp, d_comp], ignore_index=True)
        # Fill missing hazards (e.g. cyclone/landslide for Delhi, air quality for national)
        comp = comp.fillna(0)

    heatmap_path = os.path.join(OUT, "composite_heatmap.png")
    return comp, drought, flood, heatwave, cyclone, landslide, heatmap_path

composite, drought_df, flood_df, heat_df, cyclone_df, slide_df, heatmap_path = load_data()

CITIES = sorted(composite["city"].unique())
YEARS  = sorted(composite["year"].unique())

# ── Colour helpers ────────────────────────────────────────────
CAT_COLORS = {
    "LOW":       "#2ecc71",
    "MEDIUM":    "#f39c12",
    "HIGH":      "#e67e22",
    "VERY HIGH": "#e74c3c",
}
CAT_BG = {
    "LOW":       "#d5f5e3",
    "MEDIUM":    "#fef9e7",
    "HIGH":      "#fdebd0",
    "VERY HIGH": "#fadbd8",
}
CAT_EMOJI = {
    "LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "VERY HIGH": "🔴"
}

def cat_from_score(score):
    if score <= 25:   return "LOW"
    elif score <= 50: return "MEDIUM"
    elif score <= 75: return "HIGH"
    else:             return "VERY HIGH"

def get_row(city, year):
    r = composite[(composite["city"] == city) & (composite["year"] == year)]
    return r.iloc[0] if not r.empty else None

def get_city_history(city):
    return composite[composite["city"] == city].sort_values("year")

def get_recommendation(cat):
    recs = {
        "LOW":       ("✅ LOW RISK", "Standard loan processing applicable. No special climate clause needed.", "success"),
        "MEDIUM":    ("🔔 MEDIUM RISK", "Annual climate review clause recommended in the loan agreement.", "info"),
        "HIGH":      ("⚠️ HIGH RISK", "Climate risk insurance clause required before loan approval.", "warning"),
        "VERY HIGH": ("🚨 VERY HIGH RISK", "Independent climate assessment mandatory before approval. Consider insurance requirement.", "error"),
    }
    return recs.get(cat, recs["LOW"])

# ── Styling ───────────────────────────────────────────────────
st.markdown("""
<style>
    .risk-card {
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .score-big {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 8px 0;
    }
    .score-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.7;
    }
    .cat-badge {
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 6px;
    }
    .hazard-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid rgba(0,0,0,0.06);
        font-size: 0.95rem;
    }
    .section-header {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #888;
        margin: 20px 0 8px 0;
    }
    [data-testid="stSidebar"] {
        background: #0f1117;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ── Render city panel (cards + charts for one city) ───────────
def render_city_panel(city, year, key_suffix=""):
    row = get_row(city, year)
    if row is None:
        st.warning(f"No data for {city} in {year}.")
        return

    scores = {
        "drought_risk_score":   float(row.get("drought_risk_score",  0) or 0),
        "flood_risk_score":     float(row.get("flood_risk_score",    0) or 0),
        "heatwave_risk_score":  float(row.get("heatwave_risk_score", 0) or 0),
        "cyclone_risk_score":   float(row.get("cyclone_risk_score",  0) or 0),
        "landslide_risk_score": float(row.get("landslide_risk_score",0) or 0),
        "airquality_risk_score": float(row.get("airquality_risk_score",0) or 0),
        "waterscarcity_risk_score": float(row.get("waterscarcity_risk_score",0) or 0),
    }
    comp_score = float(row["composite_score"])
    comp_cat   = str(row["composite_category"])
    bg         = CAT_BG[comp_cat]
    col_hex    = CAT_COLORS[comp_cat]

    # Previous year delta
    prev_row = get_row(city, year - 1) if year > YEARS[0] else None
    delta_val = None
    if prev_row is not None:
        delta_val = comp_score - float(prev_row["composite_score"])

    # ── Top 3 cards ──────────────────────────────────────────
    col1, col2, col3 = st.columns([1.2, 1.4, 1.4])

    with col1:
        delta_str = f"{delta_val:+.1f} vs {year-1}" if delta_val is not None else ""
        st.markdown(f"""
        <div class="risk-card" style="background:{bg}; border-left: 5px solid {col_hex}; text-align:center;">
            <div class="score-label">Composite Risk Score</div>
            <div class="score-big" style="color:{col_hex};">{comp_score:.1f}<span style="font-size:1.4rem; font-weight:400;">&thinsp;/&thinsp;100</span></div>
            <div class="cat-badge">{CAT_EMOJI[comp_cat]} {comp_cat}</div>
            <div style="font-size:0.8rem; color:#666; margin-top:6px;">{delta_str}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        hazard_labels = [
            ("🌵 Drought",   scores["drought_risk_score"]),
            ("🌊 Flood",     scores["flood_risk_score"]),
            ("🌡️ Heatwave",  scores["heatwave_risk_score"]),
            ("🌀 Cyclone",   scores["cyclone_risk_score"]),
            ("⛰️ Landslide", scores["landslide_risk_score"]),
        ]
        
        # Only add these if they have scores (applies to Delhi)
        if scores["airquality_risk_score"] > 0 or scores["waterscarcity_risk_score"] > 0:
            hazard_labels.extend([
                ("💨 Air Quality", scores["airquality_risk_score"]),
                ("🚰 Water Scarcity", scores["waterscarcity_risk_score"])
            ])
            
        rows_html = "".join(
            f'<div class="hazard-row"><span>{ico}</span>'
            f'<span style="color:{CAT_COLORS[cat_from_score(sc)]};font-weight:700;">{sc:.1f}</span></div>'
            for ico, sc in hazard_labels
        )
        st.markdown(f"""
        <div class="risk-card" style="background:#fafafa; border: 1px solid #eee;">
            <div class="score-label">Individual Hazard Scores</div>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)

    with col3:
        title, msg, kind = get_recommendation(comp_cat)
        rec_bg = {"success": "#d5f5e3", "info": "#d6eaf8", "warning": "#fdebd0", "error": "#fadbd8"}[kind]
        rec_col = {"success": "#1e8449", "info": "#1a5276", "warning": "#935116", "error": "#922b21"}[kind]
        st.markdown(f"""
        <div class="risk-card" style="background:{rec_bg}; border-left: 5px solid {rec_col};">
            <div class="score-label">Bank / Insurer Recommendation</div>
            <div style="font-weight:700; font-size:1.05rem; color:{rec_col}; margin: 8px 0 4px 0;">{title}</div>
            <div style="font-size:0.9rem; color:#333;">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tabs ────────────────────────────────────────────────
    tabs = st.tabs(["📈 Score History", "🕸️ Hazard Breakdown", "🏙️ City Comparison", "🗺️ Heatmap"])

    # Tab 1 — Score History
    with tabs[0]:
        hist = get_city_history(city)
        fig  = go.Figure()

        # Individual hazard lines (thin, dashed)
        hazard_traces = [
            ("drought_risk_score",   "Drought",   "#8B4513"),
            ("flood_risk_score",     "Flood",     "#1565C0"),
            ("heatwave_risk_score",  "Heatwave",  "#E53935"),
            ("cyclone_risk_score",   "Cyclone",   "#7B1FA2"),
            ("landslide_risk_score", "Landslide", "#558B2F"),
        ]
        for col, name, color in hazard_traces:
            vals = [float(hist[hist["year"] == y][col].values[0]) if not hist[hist["year"] == y].empty else 0 for y in YEARS]
            fig.add_trace(go.Scatter(
                x=list(YEARS), y=vals, mode="lines+markers", name=name,
                line=dict(color=color, dash="dot", width=1.5),
                marker=dict(size=5), visible="legendonly",
            ))

        # Composite as bold main line, coloured by category
        comp_vals = []
        comp_cats = []
        for y in YEARS:
            r = hist[hist["year"] == y]
            comp_vals.append(float(r["composite_score"].values[0]) if not r.empty else None)
            comp_cats.append(str(r["composite_category"].values[0]) if not r.empty else "LOW")

        fig.add_trace(go.Scatter(
            x=list(YEARS), y=comp_vals, mode="lines+markers+text",
            name="Composite", text=[f"{v:.0f}" if v else "" for v in comp_vals],
            textposition="top center",
            line=dict(color="#2c3e50", width=3),
            marker=dict(size=9, color=[CAT_COLORS.get(c, "#888") for c in comp_cats],
                        line=dict(width=2, color="#2c3e50")),
        ))

        # Threshold lines
        for y_val, label, dash in [(75, "VERY HIGH threshold", "dash"), (50, "HIGH threshold", "dot"), (25, "MEDIUM threshold", "dot")]:
            fig.add_hline(y=y_val, line_dash=dash, line_color="gray", line_width=1,
                          annotation_text=label, annotation_position="right",
                          annotation_font_size=10, annotation_font_color="gray")

        fig.update_layout(
            title=f"Risk Score History — {city}",
            xaxis_title="Year", yaxis_title="Risk Score (0–100)",
            yaxis=dict(range=[0, 105]),
            legend=dict(orientation="h", y=-0.2),
            height=400, margin=dict(l=40, r=40, t=50, b=80),
            plot_bgcolor="#fafafa", paper_bgcolor="white",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True, key=f"history_{key_suffix}")

    # Tab 2 — Radar chart
    with tabs[1]:
        categories = ["Drought", "Flood", "Heatwave", "Cyclone", "Landslide"]
        values = [
            scores["drought_risk_score"],
            scores["flood_risk_score"],
            scores["heatwave_risk_score"],
            scores["cyclone_risk_score"],
            scores["landslide_risk_score"],
        ]
        
        if scores["airquality_risk_score"] > 0 or scores["waterscarcity_risk_score"] > 0:
            categories.extend(["Air Quality", "Water Scarcity"])
            values.extend([scores["airquality_risk_score"], scores["waterscarcity_risk_score"]])
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"rgba({','.join(str(int(col_hex.lstrip('#')[i:i+2], 16)) for i in (0,2,4))}, 0.2)",
            line=dict(color=col_hex, width=2),
            name=f"{city} ({year})",
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title=f"Hazard Breakdown — {city} ({year})",
            height=420, margin=dict(l=40, r=40, t=60, b=40),
            showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True, key=f"radar_{key_suffix}")

    # Tab 3 — City comparison bar chart
    with tabs[2]:
        yr_data = composite[composite["year"] == year].copy()
        yr_data = yr_data.sort_values("composite_score", ascending=True)
        yr_data["color"] = yr_data["composite_category"].map(CAT_COLORS)
        yr_data["selected"] = yr_data["city"] == city

        colors = []
        for _, r in yr_data.iterrows():
            if r["city"] == city:
                colors.append("#2c3e50")  # highlight selected city
            else:
                colors.append(CAT_COLORS.get(str(r["composite_category"]), "#888"))

        fig = go.Figure(go.Bar(
            x=yr_data["composite_score"],
            y=yr_data["city"],
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}" for v in yr_data["composite_score"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>",
        ))
        fig.update_layout(
            title=f"All Cities — Composite Risk Score ({year})",
            xaxis=dict(range=[0, 110], title="Composite Score"),
            yaxis_title="",
            height=max(500, len(yr_data) * 22),
            margin=dict(l=120, r=60, t=50, b=40),
            plot_bgcolor="#fafafa", paper_bgcolor="white",
        )
        # Threshold lines
        for x_val, label in [(25, "LOW/MEDIUM"), (50, "MEDIUM/HIGH"), (75, "HIGH/VERY HIGH")]:
            fig.add_vline(x=x_val, line_dash="dash", line_color="gray", line_width=1,
                          annotation_text=label, annotation_position="top",
                          annotation_font_size=9, annotation_font_color="gray")
        st.plotly_chart(fig, use_container_width=True, key=f"compare_{key_suffix}")

    # Tab 4 — Heatmap image
    with tabs[3]:
        if os.path.exists(heatmap_path):
            st.image(heatmap_path, caption="Multi-Hazard Climate Risk Heatmap — All Cities (Latest Year)", use_container_width=True)
        else:
            st.warning("Heatmap image not found. Run the composite notebook to generate it.")


# ═══════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 8px 0 4px 0;">
    <h1 style="margin:0; font-size:2rem; font-weight:800;">🌍 Climate Risk India</h1>
    <p style="margin:0; color:#666; font-size:1rem;">
        Multi-Hazard Real Estate Risk Analyser &nbsp;·&nbsp;
        <b>32 cities</b> &nbsp;·&nbsp; Drought · Flood · Heatwave · Cyclone · Landslide
    </p>
</div>
<hr style="margin: 12px 0 24px 0; border: none; border-top: 1px solid #eee;">
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Select Location")
    city = st.selectbox("City", CITIES, index=CITIES.index("Mumbai") if "Mumbai" in CITIES else 0)
    year = st.slider("Year", int(YEARS[0]), int(YEARS[-1]), int(YEARS[-1]))
    analyse = st.button("🔎 Analyse Risk", type="primary", use_container_width=True)

    st.divider()
    st.markdown("### ⚖️ Compare Mode")
    compare_mode = st.checkbox("Compare two cities")
    city2 = None
    if compare_mode:
        other_cities = [c for c in CITIES if c != city]
        city2 = st.selectbox("Compare with", other_cities, index=other_cities.index("Chennai") if "Chennai" in other_cities else 0)

    st.divider()
    st.markdown("""
    <div style="font-size:0.75rem; color:#aaa; line-height:1.6;">
        <b>Score Scale</b><br>
        🟢 0–25 &nbsp; LOW<br>
        🟡 26–50 MEDIUM<br>
        🟠 51–75 HIGH<br>
        🔴 76–100 VERY HIGH<br><br>
        <b>Composite Weights</b><br>
        Flood 30% · Drought 25%<br>
        Heatwave 20% · Cyclone 15%<br>
        Landslide 10%
    </div>
    """, unsafe_allow_html=True)

# ── Main content ──────────────────────────────────────────────
if not compare_mode:
    st.markdown(f"## 📍 {city} &nbsp; <span style='color:#888; font-size:1rem;'>({year})</span>", unsafe_allow_html=True)
    render_city_panel(city, year, key_suffix="main")
else:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"## 📍 {city} &nbsp; <span style='color:#888; font-size:0.9rem;'>({year})</span>", unsafe_allow_html=True)
        render_city_panel(city, year, key_suffix="left")
    with col_b:
        st.markdown(f"## 📍 {city2} &nbsp; <span style='color:#888; font-size:0.9rem;'>({year})</span>", unsafe_allow_html=True)
        render_city_panel(city2, year, key_suffix="right")

    # Difference summary
    row1 = get_row(city,  year)
    row2 = get_row(city2, year)
    if row1 is not None and row2 is not None:
        s1, s2 = float(row1["composite_score"]), float(row2["composite_score"])
        diff   = abs(s1 - s2)
        riskier = city if s1 > s2 else city2
        safer   = city2 if s1 > s2 else city

        st.divider()
        st.markdown(f"""
        <div style="background:#f0f0f0; border-radius:10px; padding:16px 24px; text-align:center;">
            <span style="font-size:1rem; font-weight:600;">
                <b>{riskier}</b> is riskier than <b>{safer}</b> by
                <span style="color:#e74c3c; font-size:1.2rem;">&nbsp;{diff:.1f} points</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
