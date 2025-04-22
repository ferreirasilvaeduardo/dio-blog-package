from typing import Union

from databases.interfaces import Record
from sqlalchemy import func, select

from dio_blog.database import database
from dio_blog.exceptions import (
    ExistConflictError,
    NotFoundError,
    UnprocessableContentError,
)
from dio_blog.models.post import posts
from dio_blog.schemas.post import PostIn, PostUpdateIn


# pylint: disable=C0116
class PostService:
    # pylint: disable=C0116
    async def read_all(
        self,
        skip: int = 0,
        limit: Union[int, None] = None,
        published: bool | None = None,
    ) -> list[Record]:
        if (not skip or skip <= 0) and limit is None and published is None:
            raise UnprocessableContentError

        if limit is not None:
            if published is not None:
                query = posts.select().where(posts.c.published == published).limit(limit).offset(skip).order_by(posts.c.id)
            else:
                query = posts.select().limit(limit).offset(skip).order_by(posts.c.id)
        else:
            if published is not None:
                query = posts.select().where(posts.c.published == published).offset(skip).order_by(posts.c.id)
            else:
                query = posts.select().offset(skip).order_by(posts.c.id)
        return await database.fetch_all(query)

    async def read(self, post_id: int) -> Record:
        return await self.__get_by_id(post_id)

    async def create(self, post: PostIn) -> int | None:
        existing_post = await self.__get_by_title(post.title)
        if existing_post:
            return None

        query = posts.insert().values(
            title=post.title,
            content=post.content,
            published_at=post.published_at,
            published=post.published,
        )
        return await database.execute(query)

    async def update(self, post_id: int, post: PostIn) -> Record | None:
        existing_post = await self.__get_by_id(post_id)
        if not existing_post:
            return None

        update_query = (
            posts.update()
            .where(posts.c.id == post_id)
            .values(
                title=post.title,
                content=post.content,
                published_at=post.published_at,
                published=post.published,
            )
        )
        await database.execute(update_query)

        existing_post_update = await self.__get_by_id(post_id)
        if not existing_post_update:
            return None

        return existing_post_update

    async def partial_update(self, post_id: int, post: PostUpdateIn) -> Record | None | PostUpdateIn:
        existing_post = await self.__get_by_id(post_id)
        if not existing_post:
            return None

        # Criar um dicionário com os valores a serem atualizados, excluindo os None
        update_data = post.model_dump(exclude_unset=True)

        if not update_data:
            return post  # Se nenhum campo foi enviado para atualizar, retornar o post existente

        # Construir e executar a query de UPDATE com os valores fornecidos
        update_query = posts.update().where(posts.c.id == post_id).values(**update_data)

        await database.execute(update_query)

        existing_post_update = await self.__get_by_id(post_id)
        if not existing_post_update:
            return None

        return existing_post_update

    async def delete(self, post_id: int):
        existing_post = await self.count(post_id=post_id)
        if not existing_post:
            raise NotFoundError

        delete_query = posts.delete().where(posts.c.id == post_id)
        return await database.execute(delete_query)

    # async def count(self, post_id: int | None) -> int | None | Record:
    #     select_query = "select count(id) as total from posts where id = :id"
    #     result_post = await database.fetch_one(select_query, {"id": post_id})
    #     return result_post.total  # noqa
    async def count(
        self,
        published: bool | None = None,
        title: str | None = None,
        post_id: int | None = None,
    ) -> int:
        # Obtém o total de registros de posts com filtros opcionais usando SQLAlchemy.
        count_query = select(func.count(posts.c.id))  # pylint: disable=E1102

        if post_id is not None:
            count_query = count_query.where(posts.c.id == post_id)
        elif title is not None:
            count_query = count_query.where(posts.c.title.like(f"%{title}%"))
        elif published is not None:
            count_query = count_query.where(posts.c.published == published)

        result = await database.fetch_one(count_query)
        return result[0] if result else 0

    async def __get_by_id(self, post_id: int) -> Record:
        select_query = posts.select().where(posts.c.id == post_id)
        post = await database.fetch_one(select_query)
        if not post:
            raise NotFoundError
        return post

    async def __get_by_title(self, post_title: str) -> Record | None:
        select_query = posts.select().where(posts.c.title == post_title)
        post = await database.fetch_one(select_query)
        if post:
            raise ExistConflictError
        return post
