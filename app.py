import os
import uvicorn
from fastapi import FastAPI, Response
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from controller.app_controller import application
from controller.auth_controller import authentication

# Fetch environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "KlgH6AzYDeZeGwD288to79I3vTHT8wp7")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
DATABASE_NAME = os.getenv("DATABASE_NAME", "UserDatabase")
USER_COLLECTION_NAME = os.getenv("USER_COLLECTION_NAME", "User")
EMBEDDING_COLLECTION_NAME = os.getenv("EMBEDDING_COLLECTION_NAME", "Embedding")
MONGODB_URL_KEY = os.getenv("MONGODB_URL_KEY", "mongodb+srv://awais:awais1122@cluster0.crj8r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

STATIC_DIR = os.getenv("STATIC_DIR", "static")
TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", "templates")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
PORT = int(os.getenv("PORT", 8000))

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=os.path.join(os.getcwd(), TEMPLATES_DIR))

@app.get("/")
def read_root():
    try:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        return templates.TemplateResponse("error.html", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/test")
def test_route():
    return Response("Testing CI-CD")

app.include_router(authentication.router)
app.include_router(application.router)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, debug=DEBUG_MODE)
