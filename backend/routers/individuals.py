from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from backend.repos.individuals import IndividualsRepo
from backend.repos.places import PlacesRepo
from backend.schemas import Individual

router = APIRouter(
    prefix='/api/v1/individuals',
    tags=['individuals'],
)

individuals_repo = IndividualsRepo()
places_repo = PlacesRepo()


@router.get('/', response_model=List[Individual])
async def get_all_individuals():
    return await individuals_repo.get_all()


@router.get('/{uid}')
async def get_individual(uid: int):
    return await individuals_repo.get_by_uid(uid)


@router.post('/', response_model=Individual, status_code=HTTPStatus.CREATED)
async def create_individual(request: Request):
    payload = await request.json()
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

    return await individuals_repo.add(
        name=individual.name,
        place_uid=individual.place_uid,
        year_of_excavation=individual.year_of_excavation,
        sex=individual.sex,
        age=individual.age,
        individual_type=individual.individual_type,
        preservation=individual.preservation,
        epoch=individual.epoch,
        comments=individual.comments,
    )


@router.put('/{uid}', response_model=Individual)
async def update_individual(uid: int, request: Request):
    payload = await request.json()
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

    await individuals_repo.update(
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
    return await individuals_repo.get_by_uid(uid)


@router.delete('/{uid}', status_code=HTTPStatus.NO_CONTENT)
async def del_individual(uid: int):
    await individuals_repo.delete(uid)
    return {}
