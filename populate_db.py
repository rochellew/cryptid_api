from app.database import engine
from app.models import Base, Cryptid
from sqlalchemy.orm import Session

cryptids_data = [
    {"name": "Bigfoot", "description": "A giant, hairy creature seen in North America.", "image_url": "https://cdn.myportfolio.com/5ee7f0be3e5cd8452558aeb334846108/0300fd3afd9d54a329d6e0be_rw_1200.jpg?h=2fb8a6276599ecd0fd8570768982add2"},
    {"name": "Mothman", "description": "A humanoid with wings and glowing red eyes, seen in West Virginia.", "image_url": "https://cdnb.artstation.com/p/assets/images/images/028/129/005/large/james-bousema-mothman-color.jpg?1593559620"},
    {"name": "Loch Ness Monster", "description": "An aquatic monster reported in Scotland's Loch Ness.", "image_url": "https://imgc.allpostersimages.com/img/posters/english-school-loch-ness-monster_u-l-q1nidro0.jpg?artHeight=550&artPerspective=n&artWidth=550&background=ffffff"},
]

def populate():
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    for cryptid in cryptids_data:
        db_cryptid = Cryptid(**cryptid)
        session.add(db_cryptid)
    session.commit()

if __name__ == "__main__":
    populate()
