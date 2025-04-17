import os
import sys

# Adicione o diretório do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_app():
    from contextlib import asynccontextmanager  # noqa

    from fastapi import FastAPI  # noqa

    from dio_blog.config import settings  # noqa
    from dio_blog.controllers.auth import router as router_auth  # noqa
    from dio_blog.controllers.post import router as router_post  # noqa
    from dio_blog.database import database, engine, metadata  # noqa

    # metadata.create_all(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await database.connect()  # noqa
        metadata.create_all(engine)
        yield
        await database.disconnect()  # noqa

    app_create_app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)
    app_create_app.include_router(router_auth)
    app_create_app.include_router(router_post)

    # @app_create_app.on_event("startup")
    # async def startup():
    #     await database.connect()

    # @app_create_app.on_event("shutdown")
    # async def shutdown():
    #     await database.disconnect()

    return app_create_app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

# def __exemplo_01_create_app():
#
#     from datetime import UTC, datetime
#     from typing import Union
#
#     from fastapi import FastAPI
#
#     app = FastAPI()
#
#     @app.get("/")
#     def read_root():
#         return {"Hello": "World"}
#
#     @app.get("/items1/{item_id}")
#     def read_items1(item_id: int, q: Union[str, None] = None):
#         return {"item_id": item_id, "q": q}
#
#     @app.get("/items2/")
#     async def read_items2(q: str | None = None):
#         results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#         if q:
#             results.update({"q": q})
#         return results
#
#     @app.get("/items3/")
#     async def read_items3(q: str | None = None):
#         results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#         if q:
#             results.update({"q": q})
#         return results
#
#     @app.get("/posts/{framework}")
#     def read_posts(framework: str):
#         return {
#             "posts": [
#                 {
#                     "title": f" - {str(framework)} :: "
#                     + datetime.now(UTC).strftime("%d/%m/%Y %H:%M:%S"),
#                     "date": datetime.now(UTC),
#                 },
#                 {
#                     "title": f" - {str(framework)} :: "
#                     + datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
#                     "date": datetime.now(),
#                 },
#             ]
#         }
#
#     return app
#
#
# def __exemplo_02_create_app():
#
#     from enum import Enum
#
#     from fastapi import FastAPI
#
#     class ModelName(str, Enum):
#         alexnet = "alexnet"
#         resnet = "resnet"
#         lenet = "lenet"
#
#     app = FastAPI()
#
#     @app.get("/models/{model_name}")
#     async def get_model(model_name: ModelName):
#         if model_name is ModelName.alexnet:
#             return {"model_name": model_name, "message": "Deep Learning FTW!"}
#
#         if model_name.value == "lenet":
#             return {"model_name": model_name, "message": "LeCNN all the images"}
#
#         return {"model_name": model_name, "message": "Have some residuals"}
#
#     return app
#
#
# def __exemplo_03_create_app():
#
#     from fastapi import FastAPI
#
#     app = FastAPI()
#
#     fake_items_db = [
#         {"item_EX1-0": "Ex1-0", "tipo": True},
#         {"item_EX1-1": "Ex1-1", "tipo": True},
#         {"item_EX1-2": "Ex1-2", "tipo": True},
#         {"item_EX1-3": "Ex1-3", "tipo": True},
#         {"item_EX1-4": "Ex1-4", "tipo": True},
#         {"item_EX1-5": "Ex1-5", "tipo": False},
#         {"item_EX1-6": "Ex1-6", "tipo": True},
#         {"item_EX1-7": "Ex1-7", "tipo": True},
#         {"item_EX1-8": "Ex1-8", "tipo": True},
#         {"item_EX1-9": "Ex1-9", "tipo": True},
#         {"item_EX2-0": "Ex2-0", "tipo": True},
#         {"item_EX2-1": "Ex2-1", "tipo": True},
#         {"item_EX2-2": "Ex2-2", "tipo": True},
#         {"item_EX2-3": "Ex2-3", "tipo": True},
#         {"item_EX2-4": "Ex2-4", "tipo": True},
#         {"item_EX2-5": "Ex2-5", "tipo": False},
#         {"item_EX2-6": "Ex2-6", "tipo": True},
#         {"item_EX2-7": "Ex2-7", "tipo": True},
#         {"item_EX2-8": "Ex2-8", "tipo": True},
#         {"item_EX2-9": "Ex2-9", "tipo": True},
#     ]
#
#     @app.get("/items/")
#     async def read_item(skip: int, limit: int = 10, tipo: bool | None = None):
#         return [
#             item
#             for item in fake_items_db[skip: skip + limit]
#             if (tipo is None or item["tipo"] == tipo)
#         ]
#
#     # Ações:
#
#     return app
#
#
# def __exemplo_04_create_app():
#
#     from fastapi import FastAPI
#
#     app = FastAPI()
#
#     @app.get("/items/{item_id}")
#     async def read_item(item_id: str, q: str | None = None):
#         if q:
#             return {"item_id": item_id, "q": q}
#         return {"item_id": item_id}
#
#     # Ações:
#
#     return app
#
#
# # https://fastapi.tiangolo.com/tutorial/body/
# def __exemplo_request_body_01():
#     from datetime import UTC, datetime
#     from typing import Union
#
#     from fastapi import FastAPI
#     from pydantic import BaseModel
#
#     class Item(BaseModel):
#         name: str
#         description: str | None = None
#         price: float
#         tax: Union[float, None] = None  # é a mesma coisa :: tax: float | None = None
#         active: Union[bool, None] = None
#         data: datetime = datetime.now(UTC)
#
#     app = FastAPI()
#
#     @app.post("/items/")
#     async def create_item(item: Item):
#         return item
#
#     return app
#
#
# # https://fastapi.tiangolo.com/tutorial/body/
# def __exemplo_request_body_02():
#     from datetime import UTC, datetime
#     from typing import Union
#
#     from fastapi import FastAPI, status
#     from pydantic import BaseModel
#
#     fake_list = []
#
#     class Item(BaseModel):
#         name: str
#         description: str | None = None
#         price: float
#         tax: Union[float, None] = None  # é a mesma coisa :: tax: float | None = None
#         active: Union[bool, None] = None
#         data: datetime = datetime.now(UTC)
#
#     app = FastAPI()
#
#     @app.post("/items/", status_code=status.HTTP_201_CREATED)
#     async def create_item(item: Item):
#         item_dict = item.model_dump()  # é a mesma coisa item.dict()
#         price_with_tax = (
#             item.price + (item.price * item.tax) if item.tax is not None else item.price
#         )
#         item_dict.update({"price_with_tax": price_with_tax})
#         fake_list.append(item_dict)
#         return item_dict
#
#     @app.get("/items/")
#     async def read_itens(
#         skip: int = 0, limit: Union[int, None] = None, active: bool | None = None
#     ):
#         if not fake_list or not fake_list[skip:]:
#             return []
#         end_skip = len(fake_list) if limit is None else skip + limit
#         return [
#             item
#             for item in fake_list[skip:end_skip]
#             if (active is None or item["active"] == active)
#         ]
#
#     @app.put("/items/{item_id}")
#     async def update_item(item_id: int, item: Item):
#         return {"item_id": item_id, **item.dict()}
#
#     return app
#
#
# # Cookie Parameters
# # https://fastapi.tiangolo.com/tutorial/cookie-params/
# def __exemplo_cookie_parameters_01():
#
#     from typing import Annotated, Union
#
#     from fastapi import Cookie, FastAPI, Header, Response
#
#     # Cookie é uma classe "irmã" de e . Ele também herda da mesma classe comum.PathQueryParam
#     # Mas lembre-se de que quando você importa , , e outros de , essas são na verdade funções que retornam classes especiais.QueryPathCookiefastapi
#     # RESUMO: Declare cookies com , usando o mesmo padrão comum que e .CookieQueryPath
#
#     app = FastAPI()
#
#     fake_list = [
#         {
#             "name": "teste1",
#             "description": None,
#             "price": 1.2,
#             "tax": 0.2,
#             "active": True,
#             "data": "2025-01-31T13:02:25.610420+00:00",
#             "price_with_tax": 1.44,
#         },
#         {
#             "name": "teste2",
#             "description": None,
#             "price": 1.2,
#             "tax": 0.2,
#             "active": False,
#             "data": "2025-02-31T13:02:25.610420+00:00",
#             "price_with_tax": 1.44,
#         },
#         {
#             "name": "teste3",
#             "description": None,
#             "price": 1.2,
#             "tax": 0.2,
#             "active": True,
#             "data": "2025-03-31T13:02:25.610420+00:00",
#             "price_with_tax": 1.44,
#         },
#         {
#             "name": "teste4",
#             "description": None,
#             "price": 1.2,
#             "tax": 0.2,
#             "active": True,
#             "data": "2025-04-31T13:02:25.610420+00:00",
#             "price_with_tax": 1.44,
#         },
#         {
#             "name": "teste5",
#             "description": None,
#             "price": 1.2,
#             "tax": 0.2,
#             "active": True,
#             "data": "2025-05-31T13:02:25.610420+00:00",
#             "price_with_tax": 1.44,
#         },
#         {
#             "name": "teste6",
#             "description": None,
#             "price": 1.2,
#             "tax": 0.2,
#             "active": False,
#             "data": "2025-07-31T13:02:25.610420+00:00",
#             "price_with_tax": 1.44,
#         },
#         {
#             "name": "teste7",
#             "description": None,
#             "price": 1.2,
#             "tax": 0.2,
#             "active": True,
#             "data": "2025-07-31T13:02:25.610420+00:00",
#             "price_with_tax": 1.44,
#         },
#     ]
#
#     @app.get("/items/")
#     async def read_items(
#         response: Response,
#         skip: int = 0,
#         limit: Union[int, None] = None,
#         active: bool | None = None,
#         ads_id: Annotated[Union[str, None], Cookie()] = None,
#         user_agent: Annotated[Union[str, None], Header()] = None,
#     ):
#         if ads_id:
#             informacao_cookie_ads_id = {"ads_id": ads_id}
#         else:
#             informacao_cookie_ads_id = {"message": "Cookie 'ads_id' não encontrado"}
#         response.set_cookie(key="user", value="exemplo_de_usuario@exemplo.com.br")
#         if user_agent:
#             informacao_cookie_user_agent = {"user_agent": user_agent}
#         else:
#             informacao_cookie_user_agent = {
#                 "message": "Header 'user_agent' não encontrado"
#             }
#         if not fake_list or not fake_list[skip:]:
#             return []
#         end_skip = len(fake_list) if limit is None else skip + limit
#         new_list = [
#             item
#             for item in fake_list[skip:end_skip]
#             if (active is None or item["active"] == active)
#         ]
#         return {
#             "Cookies": [informacao_cookie_ads_id, informacao_cookie_user_agent],
#             "list": new_list,
#         }
#
#     return app
#
#
# # https://fastapi.tiangolo.com/tutorial/response-model/
# def __exemplo_response_model_01():
#
#     from fastapi import FastAPI
#     from pydantic import BaseModel
#
#     app = FastAPI()
#
#     fake_list = []
#
#     class Item(BaseModel):
#         name: str
#         description: str | None = None
#         price: float
#         tax: float | None = None
#         tags: list[str] = []
#
#     @app.post("/items/")
#     async def create_item(item: Item) -> Item:
#         fake_list.append(item)
#         return item
#
#     @app.get("/items/")
#     async def read_items() -> list[Item]:
#         list_ex = [
#             Item(name="Portal Gun", price=42.0),
#             Item(name="Plumbus", price=32.0),
#         ]
#         if fake_list:
#             list_ex.extend(fake_list)
#         return list_ex
#
#     return app
#
#
# # https://fastapi.tiangolo.com/tutorial/response-model/
# def __exemplo_response_model_02():
#
#     from fastapi import FastAPI
#     from pydantic import BaseModel
#
#     app = FastAPI()
#
#     class Item(BaseModel):
#         name: str
#         # message: str , caso não coloco, não aparece
#
#     # response_model, é prioritario, mesmo que retorno da funcao informe diferente.
#     @app.get("/items/", response_model=Item)
#     async def read_items() -> dict[str, str]:
#         return {"name": "item", "message": "oi"}
#
#     return app
