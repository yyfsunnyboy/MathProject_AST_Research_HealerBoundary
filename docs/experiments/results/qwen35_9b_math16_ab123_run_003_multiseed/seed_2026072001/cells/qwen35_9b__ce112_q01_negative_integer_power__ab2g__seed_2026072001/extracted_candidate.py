def generate(level=1, **kwargs):
    base = kwargs.get("base", -3)
    exponent = kwargs.get("exponent", 3)
    
    question_text = r"Calculate $(-\text{int}(\text{{abs}}(b)))^e$ where $b=\text{{%s}}$ and $e=\text{{%s}}$, simplifying the result." % (base, exponent).replace("%%", "%") if False else f"Calculate ${base}^{exponent}$ by hand. Note that the base is negative."
    
    # Re-constructing a safe text using string formatting carefully for LaTeX math mode request in prompt "formal LaTeX delimiters where math appears"
    question_text = r"Compute $(-3)^{3}$ manually, showing how the sign of the result is determined by the parity of the exponent." if base == -3 and exponent == 3 else f"Calculate ${base}^{exponent}$ carefully. Remember to apply the rules for negative bases raised to integer powers."
    
    correct_answer = int(base ** exponent)
    
    oracle_payload = {"base": base, "exponent": exponent}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }