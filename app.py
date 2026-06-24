import langcodes
import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException, DetectorFactory
from nltk import TreebankWordTokenizer
from nltk.tokenize import wordpunct_tokenize
from spellchecker import SpellChecker
from nltk.tokenize.treebank import TreebankWordDetokenizer

DetectorFactory.seed = 0
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

def fix_typos(text, code):
    spell = get_spellchecker(code)
    tokens = wordpunct_tokenize(text)
    fixed = []
    for token in tokens:
        if token.isalpha() and len(token) > 1:
            suggestion = spell.correction(token.lower()) or token
            suggestion = suggestion.title() if token.istitle() else suggestion
            suggestion = suggestion.upper() if token.isupper() else suggestion
            fixed.append(suggestion)
        else:
            fixed.append(token)

    return TreebankWordDetokenizer().detokenize(fixed), fixed != tokens

def run_translation(text, target_code):
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False,
                "error": f"Input text is too short. Enter at least {MIN_INPUT_LENGTH} characters long."
                }
    source = detect_language(raw)
    if source is None:
        return {"ok": False, "error": f"Could not detect language for input text."}

    if source == target_code:
        return {
            "ok": True,
            "source": language_name(source),
            "target": language_name(target_code),
            "translated": raw,
            "note": ""
        }

    try:
        translated = GoogleTranslator(source=source, target=target_code).translate(raw)
    except Exception as e:
        return {"ok": False, "error": str(e)}

    return {
        "ok": True,
        "source": language_name(source),
        "target": language_name(target_code),
        "translated": translated
    }

def run_spellcheck(text):
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False,
                "error": f"Input text is too short. Enter at least {MIN_INPUT_LENGTH} characters long."
            }
    code = detect_language(raw)
    if code is None:
        return {
            "ok": False,
            "error": f"Could not detect language for input text."
        }

    if code not in SPELL_LANGS:
        return {
            "ok": False,
            "error": f"Could not support language {language_name(code)} for input text."
        }

    fixed, changed = fix_typos(text, code)
    return{
        "ok": True,
        "language": language_name(code),
        "fixed": fixed,
        "changed": changed
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
        corrected_text = run_spellcheck(input_text)
        st.success(corrected_text)
