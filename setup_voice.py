from pocket_tts import TTSModel, export_model_state

model = TTSModel.load_model()
voice_state = model.get_state_for_audio_prompt("alba")
export_model_state(voice_state, "./alba_voice.safetensors")
print("Voice state saved!")