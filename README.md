# 🌍 Climate Risk India — Multi-Hazard Real Estate Risk Analyser

![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-green)
![Cities](https://img.shields.io/badge/National-32%20Cities-informational)
![Delhi](https://img.shields.io/badge/Delhi-11%20Districts-red)
![Hazards](https://img.shields.io/badge/Hazards-7-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A machine learning system that assigns a **0–100 climate risk score** to Indian locations across multiple natural hazards — built for use by banks, insurers, and real estate developers in property pre-approval and risk assessment.

Two tiers of coverage:
- **National** — 32 cities across India, 5 hazards
- **Delhi Deep Dive** — all 11 districts, 7 hazards including AQI and water scarcity

> **Research project** — Drought module by [@siddharthhq](https://github.com/siddharthhq) · Flood module by collaborator

---

## 🎯 What This Does

Think of it like a **credit score, but for climate risk.** Given a location and year, the system returns a score from 0–100 per hazard plus a weighted composite:

**National example:**
```
City: Mumbai | Year: 2023

  🌵 Drought       →  12.4 / 100   LOW
  🌊 Flood         →  74.3 / 100   HIGH
  🌡️  Heatwave      →  55.1 / 100   HIGH
  🌀 Cyclone       →  61.2 / 100   HIGH
  ⛰️  Landslide     →   0.0 / 100   LOW
  ◈  Composite     →  48.7 / 100   MEDIUM
```

**Delhi deep dive example:**
```
District: North East Delhi | Year: 2023

  🌵 Drought            →  22.1 / 100   LOW
  🌊 Flood (Yamuna)     →  81.4 / 100   VERY HIGH
  🌡️  Heatwave           →  74.2 / 100   HIGH
  💨 Air Quality (AQI)  →  88.3 / 100   VERY HIGH
  💧 Water Scarcity     →  45.1 / 100   MEDIUM
  ◈  Delhi Composite    →  68.9 / 100   HIGH
  → "Climate risk insurance mandatory. Primary risks: Air Quality and Flood."
```

---

## 🗺️ Coverage

### National Module — 32 Cities

| Hazard | Cities |
|---|---|
| 🌵 Drought | Bengaluru, Bhopal, Bikaner, Chennai, Hyderabad, Jaisalmer, Jodhpur, Nagpur, Patna, Pune |
| 🌊 Flood | Above 10 + Guwahati, Kolkata, Mumbai, Srinagar, Varanasi |
| 🌡️ Heatwave | Same 15 as Flood |
| 🌀 Cyclone | Bhubaneswar, Chennai, Goa, Kochi, Kolkata, Mangaluru, Mumbai, Puducherry, Surat, Visakhapatnam |
| ⛰️ Landslide | Darjeeling, Dehradun, Gangtok, Kozhikode, Manali, Munnar, Mussoorie, Ooty, Shillong, Shimla |

### Delhi Deep Dive — 11 Districts

Central Delhi · East Delhi · New Delhi · North Delhi · North East Delhi · North West Delhi · Shahdara · South Delhi · South East Delhi · South West Delhi · West Delhi

Two additional hazards unique to the Delhi module:

**💨 Air Quality** — PM2.5 and AQI tracking per district per year using Open-Meteo Air Quality API. Counts days above WHO thresholds, tracks the Oct–Feb winter pollution season. Weighted at 25% of Delhi composite — same as flood — because AQI directly impacts property livability and value.

**💧 Water Scarcity** — combines rainfall deficit with a district-level groundwater stress index based on CGWB/DJB data. South Delhi scores critically over-exploited (1.0); North East Delhi is relatively safer (0.45).

---

## 📊 Key Findings

**National:**
- **Nagpur** has the highest average composite risk (32.8/100) — extreme heatwave scores of 99/100 nearly every year
- **Jodhpur 2017** recorded the highest single composite score (49.0/100) — simultaneous drought and flood event
- **Dehradun** is consistently the lowest risk city (0.08/100 avg)
- 83% of city-year combinations fall in LOW — HIGH risk is concentrated, not uniform

**Delhi:**
- **North East Delhi** is the highest-risk district — sits directly on the Yamuna floodplain with very high flood and AQI scores
- **South Delhi** faces the worst water scarcity — groundwater critically over-exploited
- **All 11 districts** score HIGH or VERY HIGH on Air Quality in winter months
- **South West and West Delhi** are the lowest flood-risk districts due to elevation and distance from Yamuna

---

## 🏗️ Project Structure

```
climate-risk-india-drought/
│
├── drought/
│   ├── 00_Initial_Exploration.ipynb
│   └── Module0_Drought_Risk.ipynb
│
├── flood/
│   └── Module1_Flood_Risk.ipynb
│
├── heatwave/
│   └── Module2_Heatwave_Risk.ipynb
│
├── cyclone/
│   └── Module3_Cyclone_Risk.ipynb
│
├── landslide/
│   └── Module4_Landslide_Risk.ipynb
│
├── composite/
│   ├── Module5_Composite_Score.ipynb
│   └── Module6_Risk_Lookup.ipynb
│
├── delhi/                                  ← DELHI DEEP DIVE
│   ├── Module_Delhi_00_EDA.ipynb
│   ├── Module_Delhi_01_Drought.ipynb
│   ├── Module_Delhi_02_Flood.ipynb
│   ├── Module_Delhi_03_Heatwave.ipynb
│   ├── Module_Delhi_04_AirQuality.ipynb    ← new hazard
│   ├── Module_Delhi_05_WaterScarcity.ipynb ← new hazard
│   ├── Module_Delhi_06_Composite.ipynb
│   └── Module_Delhi_07_Lookup.ipynb
│
├── data/outputs/
│   ├── composite_risk_scores.csv           ← National: 288 rows, 32 cities
│   ├── drought_risk_scores.csv
│   ├── flood_risk_scores.csv
│   ├── heatwave_risk_scores.csv
│   ├── cyclone_risk_scores.csv
│   ├── landslide_risk_scores.csv
│   ├── composite_heatmap.png
│   ├── [module]_model.pkl
│   ├── [module]_feature_importance.png
│   │
│   └── delhi/                              ← Delhi outputs
│       ├── delhi_composite_scores.csv      ← 154 rows, 11 districts × 14 years
│       ├── delhi_drought_scores.csv
│       ├── delhi_flood_scores.csv
│       ├── delhi_heatwave_scores.csv
│       ├── delhi_airquality_scores.csv
│       ├── delhi_waterscarcity_scores.csv
│       ├── delhi_composite_heatmap.png
│       ├── delhi_district_map.html         ← interactive folium map
│       └── [module]_model.pkl
│
├── main.py                                 ← CLI app (python3 main.py)
├── app.py                                  ← Web dashboard (streamlit run app.py)
└── requirements.txt
```

---

## ⚙️ How It Works

Every hazard module follows the same pipeline:

```
Open-Meteo APIs (free, no key required)
        │
        ▼
  Daily climate data per location
  (rainfall, temperature, wind, river discharge, PM2.5)
        │
        ▼
  Feature Engineering
  (SPI, water deficit, dry spell streaks, heat index,
   peak discharge, elevation, AQI thresholds)
        │
        ▼
  XGBoost Classifier
  National: Train 2015–2021 | Test 2022–2023
  Delhi:    Train 2010–2021 | Test 2022–2023
        │
        ▼
  Risk Probability (0.0 – 1.0)
        │
        ▼
  Risk Score (0–100) + Category
  LOW / MEDIUM / HIGH / VERY HIGH
```

### Composite Weights

**National:**
```python
composite = (drought × 0.25) + (flood × 0.30) + (heatwave × 0.20) + (cyclone × 0.15) + (landslide × 0.10)
```

**Delhi:**
```python
composite = (drought × 0.15) + (flood × 0.25) + (heatwave × 0.20) + (airquality × 0.25) + (waterscarcity × 0.15)
```
AQI gets a higher weight in Delhi because it is a chronic, year-round livability risk unique to the region.

---

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/siddharthhq/climate-risk-india-drought
cd climate-risk-india-drought
```

**2. Install dependencies**
```bash
pip3 install -r requirements.txt
```

**3. Run the interactive apps**

Terminal CLI:
```bash
python3 main.py
```

Web dashboard (opens at `http://localhost:8501`):
```bash
streamlit run app.py
```

**4. Or explore the notebooks directly**

Run notebooks in order within each module folder. Start with `drought/Module0_Drought_Risk.ipynb` to understand the pattern, then move through modules 1–6, then the `delhi/` folder.

---

## 📡 Data Sources

All free, no API keys required:

| Source | Variables | URL |
|---|---|---|
| Open-Meteo Archive | Rainfall, temperature, wind, ET0 | `archive-api.open-meteo.com` |
| Open-Meteo Flood | River discharge | `flood-api.open-meteo.com` |
| Open-Meteo Air Quality | PM2.5, PM10, AQI | `air-quality-api.open-meteo.com` |
| OpenTopoData | Elevation (SRTM30m) | `api.opentopodata.org` |

---

## 🧠 Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` / `numpy` | Data processing and feature engineering |
| `requests` | API calls |
| `scipy` | Gamma distribution for SPI calculation |
| `xgboost` | Risk classification model |
| `scikit-learn` | Train/test split, evaluation metrics |
| `matplotlib` | Charts and feature importance plots |
| `folium` | Interactive district map (Delhi module) |
| `streamlit` + `plotly` | Web dashboard |
| `colorama` | Colour-coded terminal output |

---

## 🏦 Bank / Insurer Use Case

| Score | Category | Recommendation |
|---|---|---|
| 0–25 | 🟢 LOW | Standard loan processing applicable |
| 26–50 | 🟡 MEDIUM | Annual climate review clause recommended |
| 51–75 | 🟠 HIGH | Climate risk insurance required before approval |
| 76–100 | 🔴 VERY HIGH | Independent climate assessment mandatory |

---

## 🤝 Contributing

Pull requests welcome. Priority areas:
- Expand Delhi module to sub-district / ward level
- Add earthquake risk module
- Add more states as deep-dive modules (Maharashtra, Gujarat)
- Improve the web dashboard with map visualisation

---

## 📄 License

MIT — free to use, modify, and distribute with attribution.
