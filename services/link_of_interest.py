from sqlalchemy.orm import Session
from models.link_of_interest import LinkOfInterest as LinkOfInterestModel
from schemas.link_of_interest import LinkOfInterestCreate, LinkOfInterestUpdate

class LinkOfInterestService:
    def __init__(self, db: Session):
        self.db = db

    def create_link(self, link_data: LinkOfInterestCreate):
        db_link = LinkOfInterestModel(**link_data.dict())
        self.db.add(db_link)
        self.db.commit()
        self.db.refresh(db_link)
        return db_link

    def get_link(self, link_id: int):
        return self.db.query(LinkOfInterestModel).filter(LinkOfInterestModel.IdEnlace == link_id).first()

    def get_all_links(self):
        return self.db.query(LinkOfInterestModel).all()

    def update_link(self, link_id: int, link_data: LinkOfInterestUpdate):
        db_link = self.get_link(link_id)
        if not db_link:
            return None

        update_data = link_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_link, key, value)

        self.db.commit()
        self.db.refresh(db_link)
        return db_link

    def delete_link(self, link_id: int):
        db_link = self.get_link(link_id)
        if db_link:
            self.db.delete(db_link)
            self.db.commit()
            return True
        return False
