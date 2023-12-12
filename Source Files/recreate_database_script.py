from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the SQLAlchemy database connection
DATABASE_URL = "sqlite:///instance/props.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Prop model
class Prop(Base):
    __tablename__ = "prop"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    pixelcount = Column(Integer)
    modeltype = Column(String(50))

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Add data to the database

prop = Prop(name="test", pixelcount=123, modeltype="Candy Canes")
db.add(prop)

prop = Prop(name="Prop 1", pixelcount=100, modeltype="Arches")
db.add(prop)

prop = Prop(name="Prop 2", pixelcount=150, modeltype="Tree 360")
db.add(prop)

prop = Prop(name="Prop 3", pixelcount=80, modeltype="Candy Canes")
db.add(prop)

prop = Prop(name="Prop 4", pixelcount=200, modeltype="Circle")
db.add(prop)

prop = Prop(name="Prop 5", pixelcount=120, modeltype="Icicles")
db.add(prop)

prop = Prop(name="Prop 6", pixelcount=90, modeltype="Single Line")
db.add(prop)

prop = Prop(name="Prop 7", pixelcount=180, modeltype="Star")
db.add(prop)

prop = Prop(name="Prop 8", pixelcount=130, modeltype="Arches")
db.add(prop)

prop = Prop(name="Prop 9", pixelcount=160, modeltype="Candy Canes")
db.add(prop)

prop = Prop(name="Prop 10", pixelcount=110, modeltype="Circle")
db.add(prop)

prop = Prop(name="Prop 1", pixelcount=100, modeltype="Arches")
db.add(prop)

prop = Prop(name="Prop 2", pixelcount=150, modeltype="Tree 360")
db.add(prop)

prop = Prop(name="Prop 3", pixelcount=80, modeltype="Candy Canes")
db.add(prop)

prop = Prop(name="Prop 4", pixelcount=200, modeltype="Circle")
db.add(prop)

prop = Prop(name="Prop 5", pixelcount=120, modeltype="Icicles")
db.add(prop)

prop = Prop(name="Prop 6", pixelcount=90, modeltype="Single Line")
db.add(prop)

prop = Prop(name="Prop 7", pixelcount=180, modeltype="Star")
db.add(prop)

prop = Prop(name="Prop 8", pixelcount=130, modeltype="Arches")
db.add(prop)

prop = Prop(name="Prop 9", pixelcount=160, modeltype="Candy Canes")
db.add(prop)

prop = Prop(name="Prop 10", pixelcount=110, modeltype="Circle")
db.add(prop)

prop = Prop(name="test", pixelcount=321, modeltype="Arches")
db.add(prop)

# Commit the changes
db.commit()

# Close the session
db.close()

print("Data added to the database.")
