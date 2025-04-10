from typing import Union

from fastapi import APIRouter, Depends, status

from dio_blog.security import login_required
from dio_blog.services.post import PostService
from dio_blog.schemas.post import PostIn, PostUpdateIn
from dio_blog.views.post import PostOut

# https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure
router = APIRouter(
    prefix="/posts",
    tags=["post"],
    dependencies=[Depends(login_required)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

service = PostService()


@router.get("/", response_model=list[PostOut])
async def read_posts(skip: int = 0, limit: Union[int, None] = None, published: bool | None = None):
    return await service.read_all(skip=skip, limit=limit, published=published)


@router.get("/{post_id}", response_model=PostOut)
async def read_post(post_id: int):
    return await service.read(post_id=post_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    last_record_id = await service.create(post=post)
    return {
        **post.model_dump(),
        "id": last_record_id,
    }  # Irá retornar de acordo com postout


@router.put("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post: PostIn):
    updated_result = await service.update(post_id=post_id, post=post)
    return updated_result


@router.patch("/{post_id}", response_model=PostOut)
async def partial_update_post(post_id: int, post: PostUpdateIn):
    updated_result = await service.partial_update(post_id=post_id, post=post)

    return updated_result


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    await service.delete(post_id=post_id)

    return status.HTTP_204_NO_CONTENT  # Retorna um status 204 No Content em caso de sucesso
