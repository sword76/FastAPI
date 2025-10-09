from fastapi import FastAPI
import uvicorn

from hotels import router as router_hotels

# Logging settings 
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(router_hotels)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=False, workers = 3)