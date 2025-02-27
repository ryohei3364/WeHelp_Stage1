from typing import Annotated
from fastapi import Request, FastAPI, Form, Response, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import mysql.connector, os, hashlib, json

HASH_SECRET_KEY=os.getenv("HASH_SECRET_KEY")
MIDDLEWARE_SECRET_KEY=os.getenv("MIDDLEWARE_SECRET_KEY")
MYSQL_PW=os.getenv("MYSQL_PW")

app=FastAPI()
app.add_middleware(SessionMiddleware, secret_key=MIDDLEWARE_SECRET_KEY)
load_dotenv()


def hash(text):
  sha = hashlib.sha256()
  sha.update((str(text) + HASH_SECRET_KEY).encode("utf-8"))
  return sha.hexdigest()

def encodeToken(data):
  return str(data)+"."+hash(data) 

def decodeToken(token):
  parts=token.split(".")
  if len(parts)==2:
    data=parts[0]
    hashshit=parts[1]
    if hash(data)==hashshit:
      return data


con=mysql.connector.connect(
  user="root",
  password=MYSQL_PW,
  host="localhost",
  database="website",
  buffered=True
)
cursor=con.cursor()


@app.get("/")
async def index(request: Request):
  return templates.TemplateResponse(
    request=request, name="index.html",
  )

@app.post("/signup")
async def signup(
  request: Request,
  name: Annotated[str, Form()], 
  username: Annotated[str, Form()], 
  password: Annotated[str, Form()], 
  ):
  request.session["signed_in"] = False

  cursor.execute("SELECT username FROM member WHERE username=%s",(username,))
  check_username=cursor.fetchone()
  
  if check_username:
    return RedirectResponse(url="/error?message=這個帳號已被註冊，請選擇其他名稱", status_code=303)
  else:
    cursor.execute(
      "INSERT INTO member(name,username,password)" 
      "VALUES(%s,%s,%s)",(name,username,password)
    )
    con.commit()
    return RedirectResponse(url="/success?message=恭喜註冊成功，請回首頁登入系統", status_code=303)

@app.post("/signin")
async def signin(
  request: Request, 
  username: Annotated[str, Form()], 
  password: Annotated[str, Form()]
  ):
  cursor.execute(
    "SELECT id,name,username,password FROM member "
    "WHERE username=%s AND password=%s",
    (username,password)
  )
  check_account=cursor.fetchone()

  if check_account:
    request.session["user_info"] = {
      "member_id": encodeToken(check_account[0]),
      "name": check_account[1],
      "username": check_account[2]
    }
    request.session["signed_in"] = True
    return RedirectResponse(url="/member", status_code=303)
  else:
    request.session["signed_in"] = False
    return RedirectResponse(url="/error?message=帳號或密碼輸入錯誤，請重新輸入", status_code=303)

@app.get("/api/member")
async def search_user(request: Request, username: str):
  signed_in = request.session.get("signed_in", False)
  if signed_in:
    cursor.execute("SELECT id, name, username FROM member WHERE username=%s", (username,))
    data = cursor.fetchone()
        
    if data:
      return {"data": {"id": data[0], "name": data[1], "username": data[2]}}
    else:
      return {"data": None}
  else:
    return {"data": None}
    
@app.patch("/api/member")
async def udpate_user(request: Request):
  signed_in = request.session.get("signed_in", False)
  if signed_in:
    try:
      data=await request.json()
      new_name = data["name"]
      request.session["user_info"]["name"] = new_name
      username = request.session["user_info"]["username"]

      cursor.execute("UPDATE member SET name=%s WHERE username=%s", (new_name,username))
      con.commit()
      return {"ok": True}
    except:
      return {"error": True}
  else:
    return {"error": True}

@app.get("/member")
async def member(request: Request):
  signed_in = request.session.get("signed_in", False)

  if signed_in:
    user_info = request.session.get("user_info")

    cursor.execute(
      "SELECT member.id,member.name,message.content,message.id "
      "FROM member INNER JOIN message ON member.id=message.member_id "
      "ORDER BY message.id DESC"
    ) 
    data=cursor.fetchall() 

    return templates.TemplateResponse(
      request=request, 
      name="member.html",
      context={
        "name": user_info['name'],
        "token_member_id": decodeToken(user_info['member_id']),
        "messages": data
      }
    )
  else:
    return RedirectResponse(url="/")
  
@app.get("/error")
async def error(
  request: Request,
  message: str=None):
  return templates.TemplateResponse(
    request=request, 
    name="error.html", 
    context={"message": message}
  )

@app.get("/success")
async def success(
  request: Request,
  message: str=None):
  return templates.TemplateResponse(
    request=request, 
    name="success.html", 
    context={"message": message}
  )

@app.get("/signout")
async def signout(request: Request):
  request.session.clear()
  return RedirectResponse(url="/")

@app.post("/createMessage")
async def createMessage(
  request: Request,
  message: Annotated[str, Form()]
):
  signed_in = request.session.get("signed_in", False)

  if signed_in:
    user_info = request.session.get("user_info")
    member_id = decodeToken(user_info['member_id'])

    cursor.execute(
      "INSERT INTO message(member_id, content) VALUES (%s,%s)",
      (member_id, message)
    )
    con.commit()
    return RedirectResponse(url="/member", status_code=303)
  else:
    return RedirectResponse(url="/")

@app.post("/deleteMessage")
async def deleteMessage(
  request: Request,
  member_id: Annotated[str, Form()],
  message_id: Annotated[str, Form()]
  ):
    user_info = request.session.get("user_info")
    token_member_id = decodeToken(user_info['member_id'])

    if not user_info:
      return RedirectResponse(url="/error?message=沒有登入資訊，請重新登入", status_code=303)
    
    elif token_member_id != member_id:
      return RedirectResponse(url="/error?message=沒有刪除留言的權限，請重新確認", status_code=303)
    else:
      cursor.execute(
      "DELETE FROM message WHERE id = %s", (message_id,)
      )
      con.commit()
      return RedirectResponse(url="/member", status_code=303)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")