from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class WasteItem(Base):
    __tablename__ = "waste_data"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    classification = Column(String)
    recommended_action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DrainageRecord(Base):
    __tablename__ = "drainage_data"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    flow_status = Column(String)
    risk_level = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ChemicalRecord(Base):
    __tablename__ = "chemical_waste"
    id = Column(Integer, primary_key=True, index=True)
    chemical_name = Column(String)
    ph_level = Column(Float)
    recommendation = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ForestRecord(Base):
    __tablename__ = "forest_cover"
    id = Column(Integer, primary_key=True, index=True)
    vegetation_index = Column(Float)
    alert_level = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = None
SessionLocal = None

def init_db(sqlite_path="ecms.db"):
    global engine, SessionLocal
    engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
