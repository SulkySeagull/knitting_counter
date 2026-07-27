from pocket_tts import TTSModel
import sounddevice as sd
import time

class Speaker:
    def __init__(self):
        self.tts_model = TTSModel.load_model() 
        self.voice_state = self.tts_model.get_state_for_audio_prompt("./alba_voice.safetensors")

      
    def say(self, text):
        audio = self.tts_model.generate_audio(self.voice_state, text + " ")
        sd.play(audio.numpy(), self.tts_model.sample_rate)
        sd.wait()
        time.sleep(0.5)
        