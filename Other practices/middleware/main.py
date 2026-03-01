from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import logging
import time 
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')

@app.middleware('http')
async def logging_middleware(request:Request,call_next):
    print('middleware started')
    start_time = time.time()
    print(f'URL: {request.url}, Method : {request.method}')

    response = await call_next(request)

    end_time = time.time()
    process_time = end_time-start_time

    print(f'Code: {response.status_code},Time Taken {process_time}',)

    print("middleware ended")
    return response

@app.get('/')
def greet():
    print("hiiii i am the method")
    return JSONResponse({'meg':"okkkk"})