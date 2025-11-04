# ECMS-AI — Starter Streamlit MVP

This is a minimal Streamlit-based MVP for the Smart Environmental Control & Management System.

## Features
- Waste image upload + heuristic classification (replace with ML model)
- Drainage reporting + simple risk heuristic + map
- Chemical waste recording with pH-based recommendations
- Forest NDVI recording
- SQLite database persistence (`ecms.db`)

## Run locally
1. Create a virtual env: `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
2. Install: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`

## Notes
- The image classifier is a placeholder. Swap `utils.classify_image` with a proper TensorFlow/PyTorch model for production.
- For geospatial features, consider replacing SQLite with Postgres + PostGIS.
