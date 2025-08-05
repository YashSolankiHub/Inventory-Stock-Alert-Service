from fastapi import FastAPI, Request
from app.api.auth import AuthRoutes
from app.api.users import UsersRoutes
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from app.exceptions.base import AppException


app = FastAPI(title="Online Learning Platform")

app.include_router(AuthRoutes.get_router(),prefix="/auth")
app.include_router(UsersRoutes.get_router(),prefix="/users")



@app.exception_handler(AppException)
async def app_exception_handler(request:Request, exc:AppException):
    return JSONResponse(
        status_code= exc.status_code,
        content= {
            "sucsess":False,
            "error":exc.detail
        }
    )


# Add Bearer token support in Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI with Bearer Auth",
        version="1.0.0",
        description="Paste JWT token using Bearer scheme",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

