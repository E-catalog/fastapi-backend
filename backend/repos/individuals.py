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
        query = Individuals.select().where(Individuals.c.uid == uid)
        return await database.fetch_one(query)

    def add(
        self,
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
        new_individual = Individuals(
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
        db_session.add(new_individual)
        db_session.commit()
        return new_individual

    def update(
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
        individual = db_session.query(Individuals).get(uid)

        if not individual:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Такого индивида нет в базе',
            )

        individual.name = name
        individual.place_uid = place_id
        individual.sex = sex
        individual.age = age
        individual.year_of_excavation = year_of_excavation
        individual.individual_type = individual_type
        individual.preservation = preservation
        individual.epoch = epoch
        individual.comments = comments

        db_session.commit()
        return individual

    def delete(self, uid: int) -> None:
        individual = db_session.query(Individuals).get(uid)
        if not individual:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Такого индивида нет в базе',
            )

        db_session.delete(individual)
        db_session.commit()
