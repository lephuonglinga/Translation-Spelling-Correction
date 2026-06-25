from nltk import wordpunct_tokenize, TreebankWordDetokenizer

from common import get_spellchecker, MIN_INPUT_LENGTH, detect_language, language_name

SPELL_LANGS = {"en","es","fr"}

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


def run_spellcheck(text):
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False,
                "error": f"Input text is too short. Enter at least {MIN_INPUT_LENGTH} characters long."
            }
    print('raw' + raw)
    code = detect_language(raw)
    print('code' + code)
    if code is None:
        return {
            "ok": False,
            "error": f"Could not detect language for input text."
        }

    print("language: " + language_name(code))
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
