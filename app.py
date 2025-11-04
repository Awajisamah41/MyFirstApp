import streamlit as st
from db import init_db, SessionLocal, WasteItem, DrainageRecord, ChemicalRecord, ForestRecord
from utils import classify_image, save_uploaded_file
import pandas as pd
from streamlit_folium import st_folium
import folium

DB_PATH = "sqlite:///ecms.db"

init_db("ecms.db")

st.set_page_config(page_title="ECMS-AI Dashboard", layout="wide")

st.title("Smart Environmental Control & Management System (ECMS-AI) — MVP")

menu = ["Dashboard","Waste Management","Drainage Monitoring","Chemical Waste","Forest Monitor"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Waste Management":
    st.header("Waste Management — Image Classification (MVP)")
    uploaded = st.file_uploader("Upload an image of waste", type=["png","jpg","jpeg"])
    if uploaded:
        img_path = save_uploaded_file(uploaded, dest_folder="uploads")
        result = classify_image(img_path)
        st.image(img_path, caption="Uploaded image", use_column_width=True)
        st.markdown(f"**Predicted class:** {result['label']}")
        st.markdown(f"**Confidence (heuristic score):** {result['score']:.2f}")
        st.markdown(f"**Recommended action:** {result['recommended_action']}")
        # Save to DB
        db = SessionLocal()
        item = WasteItem(filename=img_path, classification=result['label'],
                         recommended_action=result['recommended_action'])
        db.add(item); db.commit(); db.close()
        st.success("Saved to database.")
    st.markdown("---")
    if st.checkbox("Show waste records"):
        db = SessionLocal()
        rows = db.query(WasteItem).all()
        db.close()
        df = pd.DataFrame([{"id":r.id,"filename":r.filename,"classification":r.classification,"action":r.recommended_action,"ts":r.timestamp} for r in rows])
        st.dataframe(df)

elif choice == "Drainage Monitoring":
    st.header("Drainage & Waterborne Disease Risk")
    with st.form("drain_form"):
        loc = st.text_input("Location (e.g., Lat,Lng or address)")
        flow = st.selectbox("Flow status", ["normal","slow","blocked","stagnant"])
        population = st.number_input("Nearby population density (people/km²)", min_value=0, value=1000)
        submit = st.form_submit_button("Submit")
    if submit:
        # simple risk heuristic
        risk_score = 0
        if flow in ["blocked","stagnant"]: risk_score += 50
        risk_score += (population/1000)*20
        risk_level = "High" if risk_score>50 else ("Medium" if risk_score>20 else "Low")
        st.markdown(f"**Predicted waterborne disease risk:** {risk_level} (score {risk_score:.1f})")
        db = SessionLocal()
        rec = DrainageRecord(location=loc, flow_status=flow, risk_level=risk_level)
        db.add(rec); db.commit(); db.close()
        st.success("Drainage record saved.")
    st.markdown("---")
    st.subheader("Map of submitted drainage records")
    db = SessionLocal()
    records = db.query(DrainageRecord).all()
    db.close()
    m = folium.Map(location=[6.5244,3.3792], zoom_start=6)
    for r in records:
        # try to parse lat,lng
        try:
            lat,lng = [float(x.strip()) for x in r.location.split(",")]
        except:
            lat,lng = 6.5244,3.3792
        folium.Marker([lat,lng], popup=f"{r.flow_status} / {r.risk_level}").add_to(m)
    st_folium(m, width=700)

elif choice == "Chemical Waste":
    st.header("Chemical Waste — Safety & Neutralization")
    with st.form("chem_form"):
        chem_name = st.text_input("Chemical name")
        ph = st.number_input("pH level", value=7.0, step=0.1, format="%.1f")
        submit = st.form_submit_button("Evaluate")
    if submit:
        action = ""
        if ph < 3:
            action = "Highly acidic — neutralize with suitable base (e.g., dilute NaOH) and follow PPE guidelines."
        elif ph > 11:
            action = "Highly basic — neutralize with suitable acid (e.g., dilute HCl) and follow PPE guidelines."
        else:
            action = "Near neutral — standard containment and disposal measures."
        st.markdown(f"**Recommendation:** {action}")
        db = SessionLocal()
        rec = ChemicalRecord(chemical_name=chem_name, ph_level=ph, recommendation=action)
        db.add(rec); db.commit(); db.close()
        st.success("Chemical record saved.")
    if st.checkbox("Show chemical records"):
        db = SessionLocal()
        rows = db.query(ChemicalRecord).all()
        db.close()
        st.dataframe([{"id":r.id,"chemical":r.chemical_name,"ph":r.ph_level,"rec":r.recommendation,"ts":r.timestamp} for r in rows])

elif choice == "Forest Monitor":
    st.header("Forest Cover Monitoring (MVP)")
    st.markdown("Upload a satellite image or provide a simple NDVI value to record forest health.")
    ndvi = st.slider("Simulated NDVI value (-1 to 1)", -1.0, 1.0, 0.3, 0.01)
    if st.button("Record NDVI"):
        status = "Healthy" if ndvi>0.3 else ("At Risk" if ndvi>0 else "Degraded")
        db = SessionLocal()
        rec = ForestRecord(vegetation_index=ndvi, alert_level=status)
        db.add(rec); db.commit(); db.close()
        st.success(f"Recorded NDVI {ndvi:.2f} — status: {status}")
    if st.checkbox("Show forest records"):
        db = SessionLocal()
        rows = db.query(ForestRecord).all()
        db.close()
        st.dataframe([{"id":r.id,"ndvi":r.vegetation_index,"status":r.alert_level,"ts":r.timestamp} for r in rows])

else:
    st.header("Dashboard — Analytics")
    # simple analytics
    db = SessionLocal()
    wcount = db.query(WasteItem).count()
    dcount = db.query(DrainageRecord).count()
    ccount = db.query(ChemicalRecord).count()
    fcount = db.query(ForestRecord).count()
    db.close()
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Waste items", wcount)
    col2.metric("Drainage reports", dcount)
    col3.metric("Chemical records", ccount)
    col4.metric("Forest records", fcount)
    st.markdown("Use the sidebar to navigate modules.")
