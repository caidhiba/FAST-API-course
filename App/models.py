
# every model represents a table in our databse

from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
# this code will create the table for us instead of doing it manually in postgresadmin

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default= 'TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    