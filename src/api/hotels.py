from fastapi import Query, Body, APIRouter

from src.repositories.hotels import HotelsRepository

from src.api.dependencies import DBDep, PaginationDep

from src.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
            summary='Получение данных об отелях',
            description='Получить полных список отелей, либо конкретном отеле по названию или местоположению')
async def get_hotels(
                    pagination: PaginationDep,
                    db: DBDep,
                    title: str | None = Query(None, description="Название отеля"),
                    location: str | None = Query(None, description="Местоположение отеля")
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_all(
        location=location, 
        title=title, 
        limit=per_page, 
        offset=per_page*(pagination.page-1),
    )
    

@router.get("/hotel_id",
            summary='Получение данных об отеле по ID',
            description='Получить все данных по отелю на основании его ID')
async def get_hotels(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("",
            summary='Добавление отеля',
            description='Добавить отель с полями title и location')
async def create_hotel(db: DBDep,
                       hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Отель в Сочи",
        "value": { 
            "title": "Отель Солнцеу моря 5 звезд",
            "location": "г. Сочи, ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Отель в Дубай",
        "value": {
            "title": "Отель Рай й фонтана",
            "location": "г. Дубай, ул. Шейха, 2",
        }
    }
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
         summary='Полное обновление записи об отеле',
         description='Данная функция обновляет полностью запись об отела в базе данных',
         )
async def edit_hotel(db: DBDep,
                     hotel_id: int, 
                     hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}
    
    
@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title",
            )
async def partially_edit_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPatch,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
