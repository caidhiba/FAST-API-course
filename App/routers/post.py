
from .. import models, schemas, utils
from fastapi import Depends, FastAPI, HTTPException, Response, status,APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db


router = APIRouter()
@router.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()  #this retrieves all te posts from our posts table
    # sqlalchemy helps us using python more thansql, which helps u using databases without having a solid 
    # understanding on what sql commands to use, for example in here, db.query will retrieve all the posts from
    #  our table which is equivalant to select from in sql,
    #  then we add a methode(.all) fr example, to really run smth with thetable that got retreived.
    return posts 


@router.get("/posts")
def get_posts(db : Session = Depends(get_db), response_model=schemas.Post):
    # # we are going to use the cursor to excute queries
    # cursor.execute("""SELECT * FROM posts""")
    # # to actually run the command we use:
    # posts = cursor.fetchall()
    posts =  db.query(models.Post).all()
    return posts


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


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db : Session = Depends(get_db)):
    # # post_dict = post.dict()
    # # post_dict['id'] = randrange(1, 10000000)
    # # my_posts.append(post_dict)
    # # print(post)
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s,%s) RETURNING *""",(post.title, post.content))
    # # we used %s here so that when a user enters some weird sql commands in the body as a title etc, 
    # # there wont be a problem of vulnerability that will ruin our database
    # new_post = cursor.fetchone()
    # conn.commit() 
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    # this method is not efficient if we have 50 fields to fill, so we use **post.dict()se tat when we add new fields it automotacally 
    # unpack eveything without adding them manually to the query
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# now let's create a path application to retrieve a single post
@router.get("/posts/{id}")
def get_post(id: int, db : Session = Depends(get_db), response_model=schemas.Post):
    # post = find_post(int(id))
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()#first will stop searching when finding the first id that matches

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id :{id} was not found"
        )
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    # finding the index in our array that matches the desired id
    # index = find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} is not found"
        )
    post.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    # my_posts.pop(index)
    # return {"message" : {"my post was successfully deleted"}}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update_post(id: int, post: schemas.PostBase, db : Session = Depends(get_db), response_model=schemas.Post):
    # index = find_index_post(id)
    # cursor.execute("""UPDATE posts 
    #                SET title =%s, content = %s, published = %s
    #                WHERE id = %s
    #                returning *""",
    #                (post.title,post.content, post.published, id))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    # post_dict = post.dict()  # Convertit ton objet post (de type Post, créé par Pydantic) en dictionnaire Python.
    # post_dict["id"] = id  # Ajoute la clé "id" dans le dictionnaire pour être sûr que ton post mis à jour garde le même identifiant.
    # my_posts[index] = post_dict  # remplace l’ancien post (celui à la position index dans la liste) par le nouveau dictionnaire mis à jour.
    return post_query.first()

