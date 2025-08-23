from fastapi import FastAPI
import uvicorn
from questions_bank.controllers import question_controller

app = FastAPI()
app.include_router(question_controller.router)


def main():
    # TODO: add reload param
    uvicorn.run("questions_bank.main:app", host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
