import streamlit as st
from ai_agents import rewrite_text, summarize_text, generate_audio
import os

st.set_page_config(page_title="EchoVerse – AI Audiobook Creator", page_icon="🎧", layout="wide")
st.title("🎧 EchoVerse – AI Audiobook Creator")
st.write("Convert text into expressive, AI-generated narration with tone, summarization, and voice options.")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
user_text = st.text_area("Paste your text here:", height=200)

if uploaded_file is not None:
    user_text = uploaded_file.read().decode("utf-8")

tone = st.selectbox("Select Tone", ["Neutral", "Inspiring", "Suspenseful"])
voice = st.selectbox("Select Voice", ["Lisa", "Michael", "Allison"])
summarize = st.checkbox("Summarize before narration")
highlight = st.checkbox("Highlight key phrases")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Generate Narration") and user_text.strip():
    text_to_use = summarize_text(user_text) if summarize else user_text
    rewritten_text, key_phrases = rewrite_text(text_to_use, tone)
    display_text = rewritten_text
    if highlight and key_phrases:
        for phrase in key_phrases:
            display_text = display_text.replace(phrase, f"**{phrase}**")
    col1, col2 = st.columns(2)
    col1.subheader("Original Text")
    col1.write(user_text)
    col2.subheader("AI Rewritten Text")
    col2.markdown(display_text)
    audio_file_path = generate_audio(rewritten_text, voice)
    st.audio(audio_file_path)
    st.session_state.history.append({
        "text": rewritten_text,
        "audio": audio_file_path,
        "tone": tone,
        "voice": voice
    })

st.subheader("Past Narrations")
for item in st.session_state.history[::-1]:
    st.markdown(f"**Tone:** {item['tone']} | **Voice:** {item['voice']}")
    st.audio(item["audio"])

