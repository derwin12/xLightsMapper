from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

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

# Query all props in the database
props = db.query(Prop).all()

print("Starting app")
for prop in props:
    print(prop.id, prop.name, prop.modeltype, prop.pixelcount)

model_type_to_search = "Circle"
pixel_count_to_search = 200

matching_prop = db.query(Prop).filter_by(modeltype=model_type_to_search, pixelcount=pixel_count_to_search).first()

if matching_prop:
    print(
        f"Match found: Name={matching_prop.name}, Pixelcount={matching_prop.pixelcount}, Modeltype={matching_prop.modeltype}")
else:
    print("No match found.")

db.close()
