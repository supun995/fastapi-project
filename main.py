from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict=post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"message": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    return { "detail" : my_posts[-1] }

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id : {id} not found"}
    return {"data": post} 

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    index= find_delete_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    my_posts.remove(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(post: Post,id: int):
    post_dict=post.dict()   
    ivalue = find_update_post(id)
    if ivalue == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    post_dict['id']= id
    my_posts[ivalue]=post_dict
    return my_posts