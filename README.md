# 🌍 Climate Risk India — Multi-Hazard Real Estate Risk Analyser

![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-green)
![Cities](https://img.shields.io/badge/Cities-32-informational)
![Hazards](https://img.shields.io/badge/Hazards-5-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A machine learning system that assigns a **0–100 climate risk score** to any of 32 Indian cities across 5 natural hazards — built for use by banks, insurers, and real estate developers in property pre-approval and risk assessment.

> **Research project** — Drought module by [@siddharthhq](https://github.com/siddharthhq) · Flood module by collaborator

---

## 🎯 What This Does

Think of it like a **credit score, but for climate risk.** Given a city and year, the system returns a score from 0 to 100 for each hazard type, plus a weighted composite score:

```
City: Mumbai | Year: 2023

  🌵 Drought Risk    →  12.4 / 100   LOW
  🌊 Flood Risk      →  74.3 / 100   HIGH
  🌡️  Heatwave Risk   →  55.1 / 100   HIGH
  🌀 Cyclone Risk    →  61.2 / 100   HIGH
  ⛰️  Landslide Risk  →   0.0 / 100   LOW

  ◈  Composite Score →  48.7 / 100   MEDIUM
     → "Annual climate review clause recommended."
```

---

## 🗺️ Coverage

**32 Indian cities(with a deep dive in delhi) | 2015–2023 | 288 scored location-year combinations**

| Module | Cities Covered |
|---|---|
| 🌵 Drought | Bengaluru, Bhopal, Bikaner, Chennai, Hyderabad, Jaisalmer, Jodhpur, Nagpur, Patna, Pune |
| 🌊 Flood | Above 10 + Guwahati, Kolkata, Mumbai, Srinagar, Varanasi |
| 🌡️ Heatwave | Same 15 as Flood |
| 🌀 Cyclone | Bhubaneswar, Chennai, Goa, Kochi, Kolkata, Mangaluru, Mumbai, Puducherry, Surat, Visakhapatnam |
| ⛰️ Landslide | Darjeeling, Dehradun, Gangtok, Kozhikode, Manali, Munnar, Mussoorie, Ooty, Shillong, Shimla |

---

## 📊 Key Findings

- **Nagpur** has the highest average composite risk score (32.8/100) — driven by extreme heatwave scores hitting 99/100 nearly every year
- **Jodhpur 2017** recorded the single highest composite score (49.0/100) — simultaneous drought and flood event
- **Dehradun** consistently scores the lowest (0.08/100) — low elevation, moderate climate, no cyclone/landslide exposure
- **83% of city-year combinations** fall in the LOW category — HIGH risk is concentrated in specific cities and years, not uniform across India
- **No city has reached VERY HIGH** on the composite — the weighted averaging across hazards naturally moderates extreme single-hazard scores

---

## 🏗️ Project Structure

```
climate-risk-india-drought/
│
├── drought/
│   ├── 00_Initial_Exploration.ipynb   ← EDA and Jodhpur case study
│   └── Module0_Drought_Risk.ipynb     ← Full drought pipeline
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
│   ├── Module5_Composite_Score.ipynb  ← Combines all 5 modules
│   └── Module6_Risk_Lookup.ipynb      ← Lookup function for any city
│
├── data/
│   └── outputs/
│       ├── composite_risk_scores.csv  ← Main output (288 rows)
│       ├── drought_risk_scores.csv
│       ├── flood_risk_scores.csv
│       ├── heatwave_risk_scores.csv
│       ├── cyclone_risk_scores.csv
│       ├── landslide_risk_scores.csv
│       ├── [module]_model.pkl         ← Trained XGBoost models
│       ├── [module]_feature_importance.png
│       └── composite_heatmap.png
│
├── requirements.txt
└── README.md
```

---

## ⚙️ How Each Module Works

Every hazard module follows the same pipeline:

```
Open-Meteo API (free, no key)
        │
        ▼
  Daily climate data
  (rainfall, temperature, wind, river discharge)
        │
        ▼
  Feature Engineering
  (SPI, water deficit, dry spell streaks,
   heat index days, peak discharge, elevation)
        │
        ▼
  XGBoost Classifier
  Train: 2015–2021 | Test: 2022–2023
        │
        ▼
  Risk Probability (0.0 – 1.0)
        │
        ▼
  Risk Score (0 – 100)
  LOW / MEDIUM / HIGH / VERY HIGH
```

### Composite Score Weights
```python
composite = (
    drought_score   * 0.25 +
    flood_score     * 0.30 +   ← highest weight, most economically damaging
    heatwave_score  * 0.20 +
    cyclone_score   * 0.15 +
    landslide_score * 0.10
)
```

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

**3. Run the notebooks in order**

Open VS Code, navigate into any module folder, and run the `.ipynb` file cell by cell. Start with `drought/Module0_Drought_Risk.ipynb` to understand the pattern, then move through modules 1–6.

**4. Check the outputs**

All results are saved to `data/outputs/`. The main file is `composite_risk_scores.csv`.

---

## 📡 Data Sources

All free, no API keys required:

| Source | What it provides | URL |
|---|---|---|
| Open-Meteo Archive | Daily rainfall, temperature, wind, ET0 | `archive-api.open-meteo.com` |
| Open-Meteo Flood | Daily river discharge | `flood-api.open-meteo.com` |
| OpenTopoData | Elevation (SRTM30m) | `api.opentopodata.org` |

---

## 🧠 Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` / `numpy` | Data processing and feature engineering |
| `requests` | API calls to Open-Meteo and OpenTopoData |
| `scipy` | Gamma distribution for SPI calculation |
| `xgboost` | Risk classification model |
| `scikit-learn` | Train/test split, evaluation metrics |
| `matplotlib` | Charts and feature importance plots |
| `jupyter` | Notebook environment |

---

## 📈 Model Performance

Each module is evaluated on held-out test data (2022–2023):

| Module | Metric | Notes |
|---|---|---|
| Drought | AUC-ROC, F1, Precision, Recall | SPI-12 is strongest predictor |
| Flood | AUC-ROC, F1, Precision, Recall | Peak river discharge dominates |
| Heatwave | AUC-ROC, F1, Precision, Recall | Days above 40°C most important |
| Cyclone | AUC-ROC, F1, Precision, Recall | Max windspeed is key feature |
| Landslide | AUC-ROC, F1, Precision, Recall | Elevation × rainfall interaction |

See individual `feature_importance.png` files in `data/outputs/` for per-module breakdowns.

---

## 🏦 Bank / Insurer Use Case

The composite score maps directly to a loan processing recommendation:

| Score | Category | Recommendation |
|---|---|---|
| 0–25 | 🟢 LOW | Standard loan processing applicable |
| 26–50 | 🟡 MEDIUM | Annual climate review clause recommended |
| 51–75 | 🟠 HIGH | Climate risk insurance clause required before approval |
| 76–100 | 🔴 VERY HIGH | Independent climate assessment mandatory before approval |

---

## 🤝 Contributing

This is an active research project. If you'd like to contribute:
- Add more cities to any module
- Improve the XPath/feature engineering
- Add a new hazard module (earthquake, air quality)
- Build the interactive dashboard (`main.py` / `app.py`)

Pull requests welcome. Open an issue first to discuss larger changes.

---

## 📄 License

MIT — free to use, modify, and distribute with attribution.
