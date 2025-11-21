
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass  # it means that postcreate inherites all attributes of postBase

# class PostUpdate(PostBase):

