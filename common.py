import streamlit as st
import langcodes
from langdetect import detect, LangDetectException, DetectorFactory
from spellchecker import SpellChecker

DetectorFactory.seed = 0
MIN_INPUT_LENGTH = 3

TARGET_LANGS ={
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Pháp": "fr"
}


@st.cache_resource(show_spinner=False)
def get_spellchecker(code):
    return SpellChecker(language=code)

def language_name(code):
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code or 'Unknown'

def detect_language(raw):
    try:
        return detect(raw)
    except LangDetectException:
        return None