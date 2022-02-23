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
    return await places_repo.get_all()


@router.get('/{uid}', response_model=Place)
async def get_place(uid: int):
    return await places_repo.get_by_id(uid)


@router.post('/', response_model=Place, status_code=HTTPStatus.CREATED)
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

    return await places_repo.add(
        name=place.name,
        head_of_excavations=place.head_of_excavations,
        type_of_burial_site=place.type_of_burial_site,
        coordinates=place.coordinates,
        comments=place.comments,
    )


@router.put('/{uid}', response_model=Place)
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

    await places_repo.update(
        uid=uid,
        name=place.name,
        head_of_excavations=place.head_of_excavations,
        type_of_burial_site=place.type_of_burial_site,
        coordinates=place.coordinates,
        comments=place.comments,
    )
    return await places_repo.get_by_id(uid)


@router.delete('/{uid}', status_code=HTTPStatus.NO_CONTENT)
async def del_place(uid: int):
    await places_repo.delete(uid)
    return {}
