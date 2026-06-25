import streamlit as st

from spelling_correction import run_spellcheck
from translation import run_translation

st.title("Streamlit NLP Pipeline Demo")
st.text("Provide 2 application: Text Translation and Text Correction")
tab_translation, tab_correction = st.tabs(["Text Translation", "Text Correction"])

with tab_translation:
    st.header("Text Translation")
    input_text = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Select target language:", ["en", "Spanish", "German"])
    if st.button("Translate"):
        # Placeholder for translation logic
        translated_text = run_translation(input_text, target_language)
        st.success(translated_text)


with tab_correction:
    st.header("Text Correction")
    st.text("Supported Languages: English, French, Spanish")
    input_text = st.text_area("Enter text to correct:")
    if st.button("Correct"):
        corrected_text = run_spellcheck(input_text)
        st.success(corrected_text)
