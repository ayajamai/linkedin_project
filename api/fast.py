from fastapi import FastAPI

app = FastAPI()


# define a root `/` endpoint
@app.get("/")
def index():
    return {"ok": True}
