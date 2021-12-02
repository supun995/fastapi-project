from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='1995', 
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('Database connection was successfull!')
        break
    except Exception as error:
        print('Database Connection Failed!!!')
        time.sleep(2)

my_posts = [{"title":"content of title 1","content":"LA","id": 1 },{"title":"content of title 2","content":"NY","id": 2 }]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_delete_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_update_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def read_root():
    return {"Hello": "World all"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING * """,(post.title,post.content))
    conn.commit()
    new_post = cursor.fetchone()
    return {"message": new_post }

@app.get("/posts/latest")
def get_latest_post():
    return { "detail" : my_posts[-1] }

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    id_post=cursor.fetchone()
    if not id_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id : {id} not found"}
    return {"data": id_post} 

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(post: Post,id: int):
    cursor.execute("""UPDATE posts SET title = %s, content= %s WHERE id = %s returning *""",(post.title,post.content,str(id),))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return {"data" : updated_post}