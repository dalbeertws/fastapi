
from fastapi import FastAPI
from sql_app import models
from sql_app.database import engine
from routers.user import router as user_router
from routers.post import router as post_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)


@app.get('/')
def hello():
    return {'res': 'hello'}