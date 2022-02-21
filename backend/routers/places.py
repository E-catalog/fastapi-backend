import json
from typing import TypeVar

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ValidationError

from backend.repos.places import PlacesRepo
from backend.schemas import Place

router = APIRouter(
    prefix='/api/v1/places',
    tags=['places']
)

places_repo = PlacesRepo()
TC = TypeVar('TC', bound=BaseModel)


def to_json(items: list[TC]):
    return json.dumps([item.dict() for item in items])


@router.get('/')
def get_all_places():
    entities = places_repo.get_all()
    places = [Place.from_orm(place) for place in entities]
    return to_json(places)


@router.get('/{uid}')
def get_place(uid: int):
    place = places_repo.get_by_id(uid)
    if not place:
        raise HTTPException(status_code=404, detail='Такого места нет в базе')

    return Place.from_orm(place).dict()


@router.post('/', status_code=201)
def create_place(request: Request):
    payload = request.json
    if not payload:
        raise HTTPException(status_code=400, detail='Тело запроса не может быть пустым')

    try:
        place = Place(**payload)
    except ValidationError as error:
        raise HTTPException(status_code=400, detail='Неверный тип данных в запросе')

    entity = places_repo.add(
        name=place.name,
        head_of_excavations=place.head_of_excavations,
        type_of_burial_site=place.type_of_burial_site,
        coordinates=place.coordinates,
        comments=place.comments,
    )
    new_place = Place.from_orm(entity)
    return new_place.dict()


@router.put('/{uid}')
def update_place(uid: int, request: Request):
    payload = request.json
    if not payload:
        raise HTTPException(status_code=400, detail='Тело запроса не может быть пустым')

    try:
        place = Place(**payload)
    except ValidationError as error:
        raise HTTPException(status_code=400, detail='Неверный тип данных в запросе')

    entity = places_repo.update(
        uid=uid,
        name=place.name,
        head_of_excavations=place.head_of_excavations,
        type_of_burial_site=place.type_of_burial_site,
        coordinates=place.coordinates,
        comments=place.comments,
    )
    updated_place = Place.from_orm(entity)
    return updated_place.dict()


@router.delete('/{uid}', status_code=204)
def del_place(uid: int):
    places_repo.delete(uid)
    return
