from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response

from lab4.pg_repository import PostgresVisitRepository
from lab4.repository import ServiceNotFoundError, VisitRepository
from lab4.schemas import ItemIn, ItemOut

router = APIRouter(prefix="/api/items", tags=["items"])


def get_repository() -> VisitRepository:
    return PostgresVisitRepository()


Repo = Annotated[VisitRepository, Depends(get_repository)]


def _unknown_service(error: ServiceNotFoundError) -> HTTPException:
    return HTTPException(
        status_code=422, detail=f"Невідома послуга: {', '.join(error.titles)}"
    )


@router.get("", response_model=list[ItemOut])
def list_items(repo: Repo) -> list[ItemOut]:
    return [ItemOut.from_visit(visit) for visit in repo.list_all()]


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, repo: Repo) -> ItemOut:
    visit = repo.get(item_id)
    if visit is None:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return ItemOut.from_visit(visit)


@router.post("", response_model=ItemOut, status_code=201)
def create_item(body: ItemIn, repo: Repo) -> ItemOut:
    try:
        visit = repo.create(body.to_new_visit())
    except ServiceNotFoundError as error:
        raise _unknown_service(error) from None
    return ItemOut.from_visit(visit)


@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, body: ItemIn, repo: Repo) -> ItemOut:
    try:
        visit = repo.update(item_id, body.to_new_visit())
    except ServiceNotFoundError as error:
        raise _unknown_service(error) from None
    if visit is None:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return ItemOut.from_visit(visit)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, repo: Repo) -> Response:
    if not repo.delete(item_id):
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return Response(status_code=204)
