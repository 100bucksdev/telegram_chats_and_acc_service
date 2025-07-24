import uvicorn
from fastapi import FastAPI

from routers.account import account_router
from routers.ai_response import ai_response_router
from routers.chat import chat_router
from routers.data_for_processing import data_for_processing_router
from routers.messages import message_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(account_router, prefix="/account", tags=["accounts"])
    app.include_router(chat_router, prefix="/account/user/{user_id}/chat", tags=["chats"])

    app.include_router(message_router, prefix="/message", tags=["messages"])

    app.include_router(data_for_processing_router, prefix="/data-for-processing", tags=["data for processing"])

    app.include_router(ai_response_router, prefix="/ai-response", tags=["ai-response"])

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)