# from random import randrange
# import time
# from typing import Optional
# from fastapi import FastAPI, HTTPException, Response, status
# from fastapi.params import Body
# from pydantic import BaseModel

# import psycopg2
# from psycopg2.extras import RealDictCursor

# app = FastAPI()
# #to define the structure of a post and add constraints, we create a class then we use instances 
# # of it with the contrainsts that we need 
# class Post(BaseModel):
#     title: str
#     content: str
#     published : bool = True #if the user doesnt enter a value its true by default and dont throw err
#     # rating: Optional[int] = None
# # we use library psycopg2 to connect our api to a database like we see down below
# while True:
#     try:
   
#     conn = psycopg2.connect(host = 'localhost',database ='fastapi',user='postgres', password='wang',
#                             cursor_factory=RealDictCursor)
#     cursor = conn.cursor() #we are calling the fucntion connand saving it to the var cursor
# # and this library is kinda weird cs it doesnt state the name of columns only the values thats why we have to import another thing with the instruction from psycopg2.extras 
# # import RealDictCursor so we canadd preperty cursor_factory that makes it show the name of the column and the valuen
#     print("connection to database was successful")
#     except Exception as error:
#     print("connection failed to database")
#     print("error:", error)
#     time.sleep(2)
#     my_posts = [{"title":"title of post 1", "content":"content of post 1", "id" : 1}, {"title":"title of post 2", "content":"content of post 2", "id" : 2}]

#     def find_post(id):
#     for(p)in my_posts:
#         if p["id"] == id:
#             return p;

#     def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
        
#     @app.get("/")
# #the path here references the path that we have to go to to see the result displayed, here its / bcs we have no specifications
#     async def root():
#         return {"message": "welcome to my api.....,"}
#     @app.get("/posts")
#     def get_posts():
#         return {"data": "this is your posts"}

# # @app.post("/posts")
# # def create_posts(post : Post):
# #  #to get the data from our api we have to add this parametre,its going to extract all the firelds
# #  #from the body and convert it into python dictionnary and store it inside the variable that we 
# #  #called payload
# #  #after creatin a class we can replace payload: dict = Body(...) by the name of class saved in a var
# #     print(post)
# #     return{"data" : post}

# #now we are going to write path operation to create a post request so it recupere data from user
# #and creates a post and add itto an array of posts called my_posts
#     @app.post("/posts", status_code=status.HTTP_201_CREATED)
#     def create_posts(post : Post):
#      post_dict = post.dict()
#      post_dict['id'] = randrange(1, 10000000)
#      my_posts.append(post_dict)
#     print(post)
#     return{"data" : post_dict}



# #now let's create a path application to retrieve a single post
#     @app.get("/posts/{id}")
#     def get_post(id :int):
#      post = find_post(int(id))
#      if not post:
#         HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                       detail= f"post with id :{id} was not found")
#      return {"post details" : post}

#     @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
#     def delete_post(id :int):
#     # finding the index in our array that matches the desired id
#             index = find_index_post(id);
#             my_posts.pop(index)
#     # return {"message" : {"my post was successfully deleted"}}
#         if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post {id} is not found")
     
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} not found"
#         )

#     post_dict = post.dict() #Convertit ton objet post (de type Post, créé par Pydantic) en dictionnaire Python.
#     post_dict["id"] = id#Ajoute la clé "id" dans le dictionnaire pour être sûr que ton post mis à jour garde le même identifiant.
#     my_posts[index] = post_dict#emplace l’ancien post (celui à la position index dans la liste)par le nouveau dictionnaire mis à jour.
#     return {"data": post_dict}



from random import randrange
import time
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()



# to define the structure of a post and add constraints, we create a class then we use instances 
# of it with the contrainsts that we need 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # if the user doesnt enter a value its true by default and dont throw err
    # rating: Optional[int] = None

# we use library psycopg2 to connect our api to a database like we see down below
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='wang',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()  # we are calling the fucntion conn and saving it to the var cursor
        # and this library is kinda weird cs it doesnt state the name of columns only the values 
        # thats why we have to import another thing with the instruction from psycopg2.extras 
        # import RealDictCursor so we can add preperty cursor_factory that makes it show the name 
        # of the column and the value
        print("connection to database was successful")
        break
    except Exception as error:
        print("connection failed to database")
        print("error:", error)
        time.sleep(2)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
# the path here references the path that we have to go to to see the result displayed, here its /
# bcs we have no specifications
async def root():
    return {"message": "welcome to my api.....,"}

@app.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):
    return {"status" : "success" }


@app.get("/posts")
def get_posts():
    # we are going to use the cursor to excute queries
    cursor.execute("""SELECT * FROM posts""")
    # to actually run the command we use:
    posts = cursor.fetchall()
    return {"data": posts}


# @app.post("/posts")
# def create_posts(post : Post):
#  # to get the data from our api we have to add this parametre,its going to extract all the firelds
#  # from the body and convert it into python dictionnary and store it inside the variable that we 
#  # called payload
#  # after creatin a class we can replace payload: dict = Body(...) by the name of class saved in a var
#     print(post)
#     return{"data" : post}

# now we are going to write path operation to create a post request so it recupere data from user
# and creates a post and add it to an array of posts called my_posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(1, 10000000)
    # my_posts.append(post_dict)
    # print(post)
    cursor.execute("""INSERT INTO posts (title, content) VALUES (%s,%s) RETURNING *""",(post.title, post.content))
    # we used %s here so that when a user enters some weird sql commands in the body as a title etc, 
    # there wont be a problem of vulnerability that will ruin our database
    new_post = cursor.fetchone()
    conn.commit() 
    return {"data": new_post}



# now let's create a path application to retrieve a single post
@app.get("/posts/{id}")
def get_post(id: int):
    # post = find_post(int(id))
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id :{id} was not found"
        )
    return {"post details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # finding the index in our array that matches the desired id
    # index = find_index_post(id)
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} is not found"
        )
    conn.commit()
    # my_posts.pop(index)
    # return {"message" : {"my post was successfully deleted"}}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = find_index_post(id)
    cursor.execute("""UPDATE posts 
                   SET title =%s, content = %s, published = %s
                   WHERE id = %s
                   returning *""",
                   (post.title,post.content, post.published, id))
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    conn.commit()
    # post_dict = post.dict()  # Convertit ton objet post (de type Post, créé par Pydantic) en dictionnaire Python.
    # post_dict["id"] = id  # Ajoute la clé "id" dans le dictionnaire pour être sûr que ton post mis à jour garde le même identifiant.
    # my_posts[index] = post_dict  # remplace l’ancien post (celui à la position index dans la liste) par le nouveau dictionnaire mis à jour.
    return {"data": updated_post}
