from fastapi import FastAPI

from app.routers.form_of_mind      import router as form_router
from app.routers.growth_challenge  import router as growth_router
from app.routers.reflection        import router as reflection_router
from app.routers.wisdom_capture    import router as wisdom_router

app = FastAPI(title="Unified Python Service", version="1.0")

app.include_router(form_router,      prefix="/form_of_mind",     tags=["Form of Mind"])
app.include_router(growth_router,    prefix="/growth_challenge", tags=["Growth Challenge"])
app.include_router(reflection_router,prefix="/reflection",       tags=["Reflection"])
app.include_router(wisdom_router,    prefix="/wisdom_capture",   tags=["Wisdom Capture"])

@app.get("/")
async def root():
    return {
        "services": [
            "/form_of_mind/process",
            "/growth_challenge/process",
            "/reflection/process",
            "/wisdom_capture/process",
        ]
    }
