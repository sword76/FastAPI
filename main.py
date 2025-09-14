from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import Optional
# import logging

# Logging settings 
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)

app = FastAPI()

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
    2: {'id': 2, 'title': 'Anothe Hotel Title', 'name': 'Anothe Hotel Name'},
}

@app.get('/hotels')
def hotels_get_info():
    return({'message:': 'Hotels List'})


@app.put('/hotel/{hotel_id}')
def hotel_update(hotel_id: int, hotel: HotelPut):
    if hotel_id not in hotels_db:
        # logger.error(f'Отсутсвует запись {hotel_id} в базе данных')
        raise HTTPException(status_code=404, detail=f'Отсутсвует запись {hotel_id} в базе данных')
    hotels_db[hotel_id] = hotel.model_dump()
    
    return {"hotel_id": hotel_id, "hotel": hotels_db[hotel_id]} 
    

@app.patch('/hotel/{hotel_id}')
def hotel_partial_update(hotel_id: int, hotel: HotelPatch):
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


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)