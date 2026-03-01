from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
app = FastAPI()

app.mount('/static',StaticFiles(directory='static'),name='static')

template = Jinja2Templates(directory='templates')

@app.get('/')
def get_index_page(request:Request):
    return template.TemplateResponse('index.html',{'request':request,"client_ip": request.client.host , 'client_url':request.url}) # type: ignore


