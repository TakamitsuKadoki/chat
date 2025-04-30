# app.py（Colab上でFastAPIサーバーを立ててngrokで公開）

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from pyngrok import ngrok
import uvicorn
import nest_asyncio

# Colab対応：複数回起動エラーを防ぐ
nest_asyncio.apply()

# FastAPIインスタンス作成
app = FastAPI()

# リクエストの型を定義
class ChatRequest(BaseModel):
    message: str
    conversationHistory: list = []

# POSTエンドポイント
@app.post("/generate")
def generate(request: ChatRequest):
    user_message = request.message
    history = request.conversationHistory

    # 仮の応答（ここをGemmaなどで置き換えてもOK）
    response_text = f"あなたのメッセージ『{user_message}』を受け取りました！"

    # 会話履歴に追加
    updated_history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": response_text}
    ]

    return JSONResponse(content={
        "success": True,
        "response": response_text,
        "conversationHistory": updated_history
    })

# ngrokで外部公開
public_url = ngrok.connect(8000)
print(f"🚀 公開URL: {public_url}/generate")

# サーバー起動
uvicorn.run(app, host="0.0.0.0", port=8000)