# tts_jp.py

import pyttsx3
import threading

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

def tts_worker(text: str):
        tts = _TTS()
        try:
             tts.start(text)
        finally:
             tts.close()

def speak_text(text: str):
    threading.Thread(target=tts_worker, args=(text,), daemon=True).start()
    print(f"start speaking:{text}")