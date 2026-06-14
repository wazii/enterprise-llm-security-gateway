def anonymize_text(text, findings):

    replacements = {}
    anonymized = text

    count = 1

    findings = sorted(findings, key=lambda x: x["start"], reverse=True)

    for item in findings:

        original = text[item["start"]:item["end"]]

        placeholder = f"[{item['entity']}_{count}]"

        anonymized = (
            anonymized[:item["start"]]
            + placeholder
            + anonymized[item["end"]:]
        )

        replacements[placeholder] = original

        count += 1

    return anonymized, replacements


def deanonymize_text(text, replacements):

    for placeholder, original in replacements.items():
        text = text.replace(placeholder, original)

    return text