from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.sql import join

from backend.db.models import Individuals, Places
from backend.db.session import database


class IndividualsRepo:

    async def get_all(self) -> list[Individuals]:
        query = Individuals.select().select_from(join(Individuals, Places))
        return await database.fetch_all(query)

    async def get_by_uid(self, uid: int) -> Individuals:
        new_join = join(Individuals, Places)
        query = Individuals.select().select_from(new_join).where(Individuals.c.uid == uid)
        individual = await database.fetch_one(query)
        if not individual:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Такого индивида нет в базе',
            )
        return individual

    async def add(
        self,
        name: str,
        place_uid: int,
        year_of_excavation: Optional[int],
        sex: Optional[str],
        age: Optional[str],
        individual_type: Optional[str],
        preservation: Optional[str],
        epoch: Optional[str],
        comments: Optional[str],
    ) -> Individuals:

        query = Individuals.insert().values(
            name=name,
            place_uid=place_uid,
            sex=sex,
            age=age,
            year_of_excavation=year_of_excavation,
            individual_type=individual_type,
            preservation=preservation,
            epoch=epoch,
            comments=comments,
        )
        new_individual_uid = await database.execute(query)
        new_individual = Individuals.select().where(Individuals.c.uid == new_individual_uid)
        return await database.fetch_one(new_individual)

    async def update(
        self,
        uid: int,
        name: str,
        place_id: int,
        year_of_excavation: Optional[int],
        sex: Optional[str],
        age: Optional[str],
        individual_type: Optional[str],
        preservation: Optional[str],
        epoch: Optional[str],
        comments: Optional[str],
    ) -> Individuals:

        individual_query = Individuals.select().where(Individuals.c.uid == uid)
        individual = await database.fetch_one(individual_query)
        if not individual:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Такого индивида нет в базе',
            )

        query = Individuals.update().where(Individuals.c.uid == uid).values(
            name=name,
            place_uid=place_id,
            sex=sex,
            age=age,
            year_of_excavation=year_of_excavation,
            individual_type=individual_type,
            preservation=preservation,
            epoch=epoch,
            comments=comments,
        )
        return await database.execute(query)

    async def delete(self, uid: int) -> None:
        query = Individuals.select().where(Individuals.c.uid == uid)
        individual = await database.fetch_one(query)
        if not individual:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Такого индивида нет в базе',
            )
        query = Individuals.delete().where(Individuals.c.uid == uid)
        return await database.execute(query)
