from deep_translator import GoogleTranslator

from common import detect_language, language_name, MIN_INPUT_LENGTH


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