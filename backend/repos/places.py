from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from backend.db.models import Places
from backend.db.session import database


class PlacesRepo:

    async def get_all(self) -> list[Places]:
        query = Places.select()
        return await database.fetch_all(query)

    async def get_by_id(self, uid: int) -> Places:
        query = Places.select().where(Places.c.uid == uid)
        place = await database.fetch_one(query)
        if not place:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Такого места нет в базе')
        return place

    async def add(
        self,
        name: str,
        head_of_excavations: Optional[str],
        type_of_burial_site: Optional[str],
        coordinates: Optional[str],
        comments: Optional[str],
    ) -> Places:

        query = Places.insert().values(
            name=name,
            head_of_excavations=head_of_excavations,
            type_of_burial_site=type_of_burial_site,
            coordinates=coordinates,
            comments=comments,
        )
        new_place_id = await database.execute(query)
        new_place = Places.select().where(Places.c.uid == new_place_id)
        return await database.fetch_one(new_place)

    async def update(
        self,
        uid: int,
        name: str,
        head_of_excavations: Optional[str],
        type_of_burial_site: Optional[str],
        coordinates: Optional[str],
        comments: Optional[str],
    ) -> Places:

        place_query = Places.select().where(Places.c.uid == uid)
        place = await database.fetch_one(place_query)
        if not place:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Такого места нет в базе')

        query = Places.update().where(Places.c.uid == uid).values(
            name=name,
            head_of_excavations=head_of_excavations,
            type_of_burial_site=type_of_burial_site,
            coordinates=coordinates,
            comments=comments,
        )
        return await database.execute(query)

    async def delete(self, uid: int) -> None:
        place_query = Places.select().where(Places.c.uid == uid)
        place = await database.execute(place_query)
        if not place:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Такого места нет в базе')

        query = Places.delete().where(Places.c.uid == uid)
        return await database.execute(query)
