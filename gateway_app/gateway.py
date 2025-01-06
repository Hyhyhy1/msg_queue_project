import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from gateway_app.notification_router import router

#@asynccontextmanager
#async def lifespan(app: FastAPI):
#    database_ = app.state.database
#    if not database_.is_connected:
#        await database_.connect()
#
#    yield
#
#    database_ = app.state.database
#    if database_.is_connected:
#        await database_.disconnect()

#app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)