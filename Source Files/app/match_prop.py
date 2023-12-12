from sqlalchemy import Column, Integer, String


class Prop():
    __tablename__ = "prop"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    pixelcount = Column(Integer)
    modeltype = Column(String(50))

def find_matching_prop(model_type, pixel_count, db):
    # Query for a matching prop
    matching_prop = db.query(Prop).filter_by(modeltype=model_type, pixelcount=pixel_count).first()

    return matching_prop


