from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pyttsx3
import asyncio
import concurrent.futures
import threading

app = FastAPI()


class TTS_Engine():
    _engine = None
    _lock = threading.Lock()
    _jp_voice_id = None

    @classmethod
    def get_engine(cls):
        with cls._lock:
            if cls._engine is None:
                 cls._engine = pyttsx3.init()
                 voices = cls._engine.getProperty('voices')

                 for voice in voices:
                    if "Japanese" in voice.name:
                        cls._jp_voice_id = voice.id
                        break

                 if cls._jp_voice_id:
                     cls._engine.setProperty('voice', cls._jp_voice_id)
                 else:
                     print("Japanese voice not found. Using default voice.")
            return cls._engine

    @classmethod
    def close(cls):
         with cls._lock:
            if cls._engine is not None:
                cls._engine.stop()
                cls._engine = None

class TTSRequest(BaseModel):
    text: str


def speak_text_sync(text: str):
    """Runs pyttsx3 in a synchronous way."""
    engine = TTS_Engine.get_engine()
    try:
        engine.say(text)
        engine.runAndWait()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/test/")
async def test_route():
    return {"message": "Hello, World!"}


@app.post("/tts/")
async def speak_text(request_data: TTSRequest):
    try:
        text = request_data.text
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await asyncio.get_running_loop().run_in_executor(
                    executor, speak_text_sync, text
                )

        if result["status"] == "success":
            return JSONResponse(content={"message": "Text spoken successfully"}, status_code=200)
        else:
            print(f"Error: {result['message']}")
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail=str(e))

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn

    backend_port = 28641
    uvicorn.run(app, host="0.0.0.0", port=backend_port, reload=True)

    # Clean up resources
    TTS_Engine.close()