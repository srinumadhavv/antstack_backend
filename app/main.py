from fastapi import FastAPI
from .routers import coupons,checkout
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
app=FastAPI()

app.include_router(coupons.router)
app.include_router(checkout.router)

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/new") #path operation
def root():
    return{"message":{"tag":"Hello World!!"}}

@app.get("/board") #path operation
def root2():
    board_data = {
        'tasks': {
            'task-1':{'id':'task-1','content':'create-video'},
            'task-2':{'id':'task-2','content':'create-video2'},
        },
        'columns':{
            'column-1': {
                'id':'column-1',
                'title':'to-do',
                'taskIds':['task-2','task-3']
            },
            'column-2': {
                'id':'column-2',
                'title':'to-do',
                'taskIds':['task-1']
            }
        },
        'columnOrder':['column-1','column-2']
        }
    return{'board':board_data}
