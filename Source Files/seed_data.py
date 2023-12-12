from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the SQLAlchemy database connection
DATABASE_URL = 'sqlite:///instance/props.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Prop model
class Prop(Base):
    __tablename__ = "prop"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pixelcount = Column(Integer)
    modeltype = Column(String)

# Create the database table
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Sample data
sample_data = [
    {"name": "Prop 1", "pixelcount": 100, "modeltype": "Arches"},
    {"name": "Prop 2", "pixelcount": 150, "modeltype": "Tree 360"},
    {"name": "Prop 3", "pixelcount": 80, "modeltype": "Candy Canes"},
    {"name": "Prop 4", "pixelcount": 200, "modeltype": "Circle"},
    {"name": "Prop 5", "pixelcount": 120, "modeltype": "Icicles"},
    {"name": "Prop 6", "pixelcount": 90, "modeltype": "Single Line"},
    {"name": "Prop 7", "pixelcount": 180, "modeltype": "Star"},
    {"name": "Prop 8", "pixelcount": 130, "modeltype": "Arches"},
    {"name": "Prop 9", "pixelcount": 160, "modeltype": "Candy Canes"},
    {"name": "Prop 10", "pixelcount": 110, "modeltype": "Circle"},
]

# Add sample data to the database
for data in sample_data:
    prop = Prop(name=data["name"], pixelcount=data["pixelcount"], modeltype=data["modeltype"])
    db.add(prop)

# Commit the changes
db.commit()

# Close the session
db.close()

print("Sample data added to the database.")
