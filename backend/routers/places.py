from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from backend.repos.places import PlacesRepo
from backend.schemas import Place

router = APIRouter(
    prefix='/api/v1/places',
    tags=['places'],
)

places_repo = PlacesRepo()


@router.get('/', response_model=List[Place])
async def get_all_places():
    #entities = places_repo.get_all()
    #places = [Place.from_orm(place) for place in entities]
    places = await places_repo.get_all()
    return [place.dict() for place in places]


@router.get('/{uid}')
def get_place(uid: int):
    place = places_repo.get_by_id(uid)
    if not place:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Такого места нет в базе')

    return Place.from_orm(place).dict()


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_place(request: Request):
    payload = await request.json()
    if not payload:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Тело запроса не может быть пустым',
        )

    try:
        place = Place(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Неверный тип данных в запросе',
        )

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
async def update_place(uid: int, request: Request):
    payload = await request.json()
    if not payload:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Тело запроса не может быть пустым',
        )

    try:
        place = Place(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Неверный тип данных в запросе',
        )

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


@router.delete('/{uid}', status_code=HTTPStatus.NO_CONTENT)
def del_place(uid: int):
    places_repo.delete(uid)
    return {}
