from fastapi import FastAPI

app = FastAPI(title="IT Ticket Management System")


@app.get("/")
def root():
    return {"message": "IT Ticket Management System API is running"}