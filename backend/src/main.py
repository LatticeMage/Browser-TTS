from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pyttsx3
import asyncio

app = FastAPI()

class _TTS:
    engine = None
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        jp_voice_id = None
        for voice in voices:
            if "Japanese" in voice.name:
                jp_voice_id = voice.id
                break
        if jp_voice_id:
            self.engine.setProperty('voice', jp_voice_id)
        else:
            print("Japanese voice not found. Using default voice.")


    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()

    def close(self):
        if self.engine:
             self.engine.stop()
             del(self.engine)
             self.engine = None

class TTSRequest(BaseModel):
    text: str


@app.get("/test/")
async def test_route():
    return {"message": "Hello, World!"}

@app.post("/tts/")
async def speak_text(request_data: TTSRequest):
    try:
        text = request_data.text
        tts = _TTS()  # Create a new _TTS instance for every request
        tts.start(text)
        tts.close()   #clean the resources
        return JSONResponse(content={"message": "Text spoken successfully"}, status_code=200)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))



# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn

    backend_port = 28641
    uvicorn.run(app, host="0.0.0.0", port=backend_port, reload=True)