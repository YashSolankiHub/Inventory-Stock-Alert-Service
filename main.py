from fastapi import FastAPI, Request
from app.api.auth import AuthRoutes
from app.api.users import UsersRoutes
from app.api.category import CategoryRoutes
from app.api.product import ProductRoutes
from app.api.warehouse import WarehouseRoutes
from app.api.supplier import SupplierRoutes
from app.api.purchase_order import PORoutes
from app.api.po_item import POItemRoutes
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from app.exceptions.base import APIException


app = FastAPI(title="Online Learning Platform")

app.include_router(AuthRoutes.get_router(),prefix="/auth")
app.include_router(UsersRoutes.get_router(),prefix="/users")
app.include_router(CategoryRoutes.get_router(),prefix="")
app.include_router(ProductRoutes.get_router(),prefix="")
app.include_router(WarehouseRoutes.get_router(),prefix="/warehouses")
app.include_router(SupplierRoutes.get_router(),prefix="/suppliers")
app.include_router(PORoutes.get_router(),prefix="/purchase_order")
app.include_router(POItemRoutes.get_router(),prefix="/purchase_order_items")



@app.exception_handler(APIException)
async def app_exception_handler(request:Request, exc:APIException):
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

