import asyncio
from fastapi import Query, Body, Path, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
import time

router = APIRouter(prefix="/hotels", tags=["Отели"])

# Put data model
class HotelPut(BaseModel):
    title: str
    name: str

# Patch data model
class HotelPatch(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None

# DB stub
hotels_db = {
    1: {'id': 1, 'title': 'Old Hotel Title', 'name': 'Old Hotel Name'},
    2: {'id': 2, 'title': 'Another Hotel Title', 'name': 'Anothe Hotel Name'},
    3: {'id': 3, 'title': 'Yet Another Hotel Title', 'name': 'Yes Anothe Hotel Name'},
    4: {'id': 4, 'title': 'Poor Imagination Hotel Title', 'name': 'Poor Imagination Hotel Title'},
    5: {'id': 5, 'title': 'Hotel Title 1', 'name': 'Hotel Title 1'},
    6: {'id': 6, 'title': 'Hotel Title 2', 'name': 'Hotel Title 2'},
    7: {'id': 7, 'title': 'Hotel Title 3', 'name': 'Hotel Title 3'},
    8: {'id': 8, 'title': 'Hotel Title 4', 'name': 'Hotel Title 4'},
}
 
@router.get('/sync/{id}')
def sync_func(id: int):
    print(f'Sync: Начат {id} - {time.time():.2f}')
    time.sleep(2)
    print(f'Sync: Закончен {id} - {time.time():.2f}')


@router.get('/async/{id}')
async def async_func(id: int):
    print(f'Async: Начат {id} - {time.time():.2f}')
    await asyncio.sleep(2)
    print(f'Async: Закончен {id} - {time.time():.2f}')


@router.get('',
            summary='Получение данных об отеле/отелях',
            description='Получить полных список отелей, либо конкретном отеле по ID или названию')
def hotels_get_info(id: int | None = Query(default = None, description = "ID Отеля"), 
                    title: str | None = Query(default = None, description = "Название отеля"),
                    page: int | None = Query(default = 1, description="Страница"),
                    per_page: int | None = Query(default = 3, description="Позиций на странице")):
    if id is not None:
        hotel = hotels_db.get(id)
        if not hotel:
            raise HTTPException(status_code=404, detail=f'Отсутсвует запись {id} в БД')
        return hotel
    
    if title is not None:
        for hotel in hotels_db.values():
            if hotel['title'].lower() == title.lower():
                return hotel
        raise HTTPException(status_code=404, detail=f'Отсутсвует запись {title} в БД')

    # Getting sorted hotels_db keys
    hotels_db_keys = sorted(hotels_db.keys())
    start = (page - 1) * per_page
    end = start + per_page
    if end > len(hotels_db_keys):
        end = len(hotels_db_keys.length())
    
    # Getting prompted page keys
    page_keys = hotels_db_keys[start:end]

    # Forming selected keys dictionary
    paged_hotels = {key: hotels_db[key] for key in page_keys}

    return list(paged_hotels.values())


@router.put('/{hotel_hoid}',
         summary='Полное обновление записи',
         description='Данная функция обновляет полностью запись об отела в базе данных')
def hotel_update(hotel_id: int = Query(description="ID отеля"), hotel: HotelPut = Query(description="Hotel Put Class")):
    if hotel_id not in hotels_db:
        # logger.error(f'Отсутсвует запись {hotel_id} в базе данных')
        raise HTTPException(status_code=404, detail=f'Отсутсвует запись {hotel_id} в БД')
    hotels_db[hotel_id] = hotel.model_dump()
    
    return {"hotel_id": hotel_id, "hotel": hotels_db[hotel_id]} 
    

@router.patch('/{hotel_id}', 
           summary='Частичное обновление записи',
           description='Данная функция производит частичное обновление записи об отеле в БД')
def hotel_partial_update(hotel_id: int = Path(description="ID отеля"), hotel: HotelPatch = Body(description="Hotel Patch Class")):
    if hotel_id not in hotels_db:
        # logger.error(f'Отсутсвует запись {hotel_id} в базе данных')
        raise HTTPException(status_code=404, detail=f'Отсутсвует запись {hotel_id} в базе данных')
    current_hotel = hotels_db[hotel_id]
    update_hotel_data =  hotel.model_dump(exclude_unset=True) # Include only passed fuilds
    if not update_hotel_data:
        raise HTTPException(status_code=400, detail='No fuilds provided for update')
    
    # Partial fuild update
    updated_data = {**current_hotel, **update_hotel_data}
    hotels_db[hotel_id] = updated_data

    return {"hotel_id": hotel_id, "hotel": updated_data} 