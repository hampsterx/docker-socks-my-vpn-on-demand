from .routes import router
from fastapi import FastAPI
from starlette.responses import FileResponse


app = FastAPI(
    title="OpenVPN Socks Client Manager API",
    description="OpenVPN Socks Client Manager API",
    version="0.0.1",
    docs_url="/docs/",
    openapi_url="/docs/spec.json"
)

app.include_router(router)


@app.get('/health')
async def health():
    return {'status': "ok"}

@app.get("/", include_in_schema=False)
async def home():
    return {}

@app.get('/favicon.ico', include_in_schema=False)
async def fav():
    return FileResponse('static/favicon.ico')



