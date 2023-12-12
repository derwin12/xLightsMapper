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

# Query all props in the database
props = db.query(Prop).all()

# Generate a Python script to recreate the database
script_content = f"""
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
"""

for prop in props:
    script_content += f"""
prop = Prop(name="{prop.name}", pixelcount={prop.pixelcount}, modeltype="{prop.modeltype}")
db.add(prop)
"""

# Close the session
script_content += """
# Commit the changes
db.commit()

# Close the session
db.close()

print("Data added to the database.")
"""

# Write the script to a file
with open("recreate_database_script.py", "w") as script_file:
    script_file.write(script_content)

print("Script to recreate the database has been generated: recreate_database_script.py")
