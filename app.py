import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, LanguageDetectException
from nltk.tokenize import wordpunct_tokenize
from spellchecker import SpellChecker

MIN_INPUT_LENGTH = 3

SPELL_LANGS = {"en","es","fr","pt", "de", "ru","ar", "eu", "lv","nl"}

TARGET_LANGS ={
    "Tiếng Việt": "vi", 
    "Tiếng Anh": "en", 
    "Tiếng Pháp": "fr", 
    "Tiếng Nhật": "ja", 
    "Tiếng Trung (Giản thể)": "zh-CN", 
    "Tiếng Hàn": "ko", 
    "Tiếng Đức": "de"
}

st.title("Streamlit NLP Pipeline Demo")
st.text("Provide 2 application: Text Translation and Text Correction")
tab_translation, tab_correction = st.tabs(["Text Translation", "Text Correction"])
with tab_translation:
    st.header("Text Translation")
    input_text = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Select target language:", ["French", "Spanish", "German"])
    if st.button("Translate"):
        # Placeholder for translation logic
        translated_text = f"Translated '{input_text}' to {target_language}."
        st.success(translated_text)

with tab_correction:
    st.header("Text Correction")
    st.text("Supported Languages: English, French, Spanish")
    input_text = st.text_area("Enter text to correct:")
    if st.button("Correct"):
        # Placeholder for correction logic
        corrected_text = f"Corrected '{input_text}'."
        st.success(corrected_text)