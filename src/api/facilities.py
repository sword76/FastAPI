from fastapi import Query, Body, APIRouter

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("",
            summary='Получение данных о всех удобствах для номеров',
            description='Получение данных о всех удобствах без фильтрации')
async def get_facilities(
                    pagination: PaginationDep,
                    db: DBDep,
):
    per_page = pagination.per_page or 5
    return await db.facilities.get_all(offset=per_page*(pagination.page-1))


@router.post("",
            summary='Добавление удобства',
            description='Добавить удобство, только поле title')
async def create_hotel(db: DBDep,
                       facility_data: FacilityAdd = Body(openapi_examples={
    "1": {
        "summary": "Фен",
        "value": { 
            "title": "Фен в номере",
        }
    },
    "2": {
        "summary": "Спутниковое ТВ",
        "value": {
            "title": "Спутниковое телевидиние",
        }
    }
})
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
