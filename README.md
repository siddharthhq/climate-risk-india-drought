# Climate Risk India — Drought Module

This module computes drought risk scores for Indian property locations.

## What This Does
- Fetches rainfall and ET0 data from Open-Meteo API
- Computes drought features: water deficit, dry days, SPI
- Trains an XGBoost model to predict drought probability
- Outputs a 0–100 drought risk score per location

## Folder Structure
drought/        → Jupyter notebooks
data/raw/       → Raw downloaded data
data/outputs/   → Charts, CSVs, trained model

## Cities Covered
Jodhpur, Jaisalmer, Bikaner, Nagpur, Pune, Chennai, Bengaluru, Hyderabad, Bhopal, Patna