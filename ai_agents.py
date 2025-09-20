from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

tokenizer = AutoTokenizer.from_pretrained("ibm-granite/granite-3.3-2b-instruct")
model = AutoModelForCausalLM.from_pretrained("ibm-granite/granite-3.3-2b-instruct")
model.eval()

def rewrite_text(text, tone="Neutral"):
    messages = [{"role": "user", "content": f"Rewrite this text in a {tone} tone: {text}"}]
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=200)
    rewritten_text = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])
    key_phrases = [word for word in rewritten_text.split() if word.istitle()]
    return rewritten_text, key_phrases

def summarize_text(text):
    messages = [{"role": "user", "content": f"Summarize this text concisely: {text}"}]
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=100)
    summary = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])
    return summary

def generate_audio(text, voice="Lisa"):
    api_key = os.getenv("IBM_TTS_API_KEY")
    url = os.getenv("IBM_TTS_URL")
    authenticator = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(url)
    audio_file = "output.mp3"
    with open(audio_file, "wb") as audio:
        response = tts.synthesize(text, voice=f"{voice}_V3Voice", accept="audio/mp3").get_result()
        audio.write(response.content)
    return audio_file
