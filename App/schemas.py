
from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass  # it means that postcreate inherites all attributes of postBase

class Post(PostBase):
    id: int
    created_at: datetime
    class Config: # we should add this class so the pydantic model will read our data even if it wasnt dict format bcs here it is orm sqlalchemy and 
        #if we do not add this class it will cause us error
        orm_mode = True

