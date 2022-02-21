from typing import Optional

from fastapi import HTTPException

from backend.db.models import Places
from backend.db.session import db_session


class PlacesRepo:

    def get_all(self) -> list[Places]:
        return db_session.query(Places).all()

    def get_by_id(self, uid: int):
        return db_session.query(Places).get(uid)

    def add(
        self,
        name: str,
        head_of_excavations: Optional[str],
        type_of_burial_site: Optional[str],
        coordinates: Optional[str],
        comments: Optional[str],
    ) -> Places:
        new_place = Places(
            name=name,
            head_of_excavations=head_of_excavations,
            type_of_burial_site=type_of_burial_site,
            coordinates=coordinates,
            comments=comments,
        )
        db_session.add(new_place)
        db_session.commit()
        return new_place

    def update(
        self,
        uid: int,
        name: str,
        head_of_excavations: Optional[str],
        type_of_burial_site: Optional[str],
        coordinates: Optional[str],
        comments: Optional[str],
    ) -> Places:
        place = db_session.query(Places).get(uid)

        if not place:
            raise HTTPException(status_code=404, detail='Такого индивида нет в базе')

        place.name = name
        place.uid = uid
        place.head_of_excavations = head_of_excavations
        place.type_of_burial_site = type_of_burial_site
        place.coordinates = coordinates
        place.comments = comments

        db_session.commit()
        return place

    def delete(self, uid: int) -> None:
        place = db_session.query(Places).get(uid)
        if not place:
            return

        db_session.delete(place)
        db_session.commit()
