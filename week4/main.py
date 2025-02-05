from typing import Annotated
from fastapi import Request, FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app=FastAPI()
app.add_middleware(SessionMiddleware, secret_key='middleware_secret_key')


@app.get("/")
async def index(request: Request):
  return templates.TemplateResponse(
    request=request, name="index.html"
  )


@app.post("/signin")
async def signin(
  request: Request, 
  username: Annotated[str, Form()], 
  password: Annotated[str, Form()]
  ):
  if not username or not password:
    return RedirectResponse(url="/error?message=請輸入帳號與密碼", status_code=303)
  
  elif username != "test" or password != "test":
    return RedirectResponse(url="/error?message=帳號、或密碼輸入錯誤", status_code=303)
  
  else:
    request.session["signed_in"] = True
    return RedirectResponse(url="/member", status_code=303)


@app.get("/member")
async def member(request: Request):
  signed_in = request.session.get("signed_in", False)
  if signed_in:
    return templates.TemplateResponse(
      request=request, 
      name="member.html"
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


@app.get("/signout")
async def signout(request: Request):
  request.session["signed_in"] = False
  return RedirectResponse(url="/")


@app.get("/square/{num}")
async def square(
  request: Request,
  num: int):
  result = num * num
  return templates.TemplateResponse(
    request=request, name="square.html", context={"message": result}
  )


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")