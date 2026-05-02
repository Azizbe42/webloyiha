def check(text):
    keywords = ["ai", "python", "data", "machine"]

    score = 0
    for k in keywords:
        if k in text.lower():
            score += 1

    return f"AI baho: {score}/4"
