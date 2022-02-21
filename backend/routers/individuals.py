import json
from http import HTTPStatus
from typing import TypeVar

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ValidationError

from backend.repos.individuals import IndividualsRepo
from backend.repos.places import PlacesRepo
from backend.schemas import Individual, Place

router = APIRouter(
    prefix='/api/v1/individuals',
    tags=['individuals'],
)

individuals_repo = IndividualsRepo()
places_repo = PlacesRepo()
TC = TypeVar('TC', bound=BaseModel)


def to_json(items: list[TC]):
    return json.dumps([item.dict() for item in items])


@router.get('/')
def get_all_individuals():
    places = {place.uid: Place.from_orm(place) for place in places_repo.get_all()}
    entities = individuals_repo.get_all()
    individuals = [Individual.from_orm(entity) for entity in entities]

    for individual in individuals:
        individual.links['place'] = places.get(individual.place_uid)

    return to_json(individuals)


@router.get('/{uid}')
def get_individual(uid: int):
    entity = individuals_repo.get_by_uid(uid)
    if not entity:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого индивида нет в базе',
        )

    individual = Individual.from_orm(entity)
    place_entity = places_repo.get_by_id(individual.place_uid)
    individual.links['place'] = Place.from_orm(place_entity)
    return individual.dict()


@router.post('/', status_code=HTTPStatus.CREATED)
def create_individual(request: Request):
    payload = request.json
    if not payload:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Тело запроса не может быть пустым',
        )

    try:
        individual = Individual(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Неверный тип данных в запросе',
        )

    entity = individuals_repo.add(
        name=individual.name,
        place_id=individual.place_uid,
        year_of_excavation=individual.year_of_excavation,
        sex=individual.sex,
        age=individual.age,
        individual_type=individual.individual_type,
        preservation=individual.preservation,
        epoch=individual.epoch,
        comments=individual.comments,
    )
    individual = Individual.from_orm(entity)
    return individual.dict()


@router.put('/{uid}')
def update_individual(uid: int, request: Request):
    payload = request.json
    if not payload:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Тело запроса не может быть пустым',
        )

    try:
        individual = Individual(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Неверный тип данных в запросе',
        )

    entity = individuals_repo.update(
        uid=uid,
        name=individual.name,
        place_id=individual.place_uid,
        year_of_excavation=individual.year_of_excavation,
        sex=individual.sex,
        age=individual.age,
        individual_type=individual.individual_type,
        preservation=individual.preservation,
        epoch=individual.epoch,
        comments=individual.comments,
    )
    return Individual.from_orm(entity).dict()


@router.delete('/{uid}', status_code=HTTPStatus.NO_CONTENT)
def del_individual(uid: int):
    individuals_repo.delete(uid)
    return {}
