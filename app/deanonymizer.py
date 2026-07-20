def deanonymize_text(text, replacements):

    for placeholder, original in replacements.items():
        text = text.replace(
            placeholder,
            original
        )

    return text