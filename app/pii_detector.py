from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

def detect_pii(text: str):
    results = analyzer.analyze(
        text=text,
        language="en"
    )

    results = [
        r for r in results
        if r.entity_type != "URL"
    ]

    findings = []

    for result in results:
        findings.append({
            "entity": result.entity_type,
            "start": result.start,
            "end": result.end,
            "score": round(result.score, 2)
        })

    return findings