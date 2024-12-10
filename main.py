from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import requests

app = FastAPI()


@app.get("/")
async def main_route():
    return {"message": "Hello World"}


@app.post("/ask-ai")
async def ask_ai(data: dict):
    url = "http://localhost:11434/api/chat"
    json_data = {
        "model": "llama3",
        "messages": [{"role": "user", "content": "hello how are you?"}],
        "stream": True,
    }

    response = requests.post(url, json=json_data)

    if response.status_code == 200:

        async def generate():
            for line in response.iter_lines():
                if line:
                    yield line

        return StreamingResponse(generate(), media_type="application/json")
    else:
        return {"error": f"API call failed with status code {response.status_code}"}
