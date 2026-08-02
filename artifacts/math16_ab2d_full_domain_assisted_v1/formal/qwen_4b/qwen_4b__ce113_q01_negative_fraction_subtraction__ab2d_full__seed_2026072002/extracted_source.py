def generate(level=1, **kwargs):
    frozen_params = kwargs.get("oracle_payload", {"expression": "3/7 - (-1/4)"})
    
    # Parse the expression: 3/7 and -(-1/4) which is effectively adding 1/4.
    # The problem asks for 3/7 - (-1/4). 
    # We can parse this as subtracting a negative fraction, or simply add positive fractions.
    # Let's follow the instruction to construct operands preserving signs if needed.
    
    # Operand A: 3/7
    num_a = 3
    den_a = 7
    
    # Operand B: -1/4 (the term being subtracted)
    # The expression is 3/7 - (-1/4). 
    # So we are computing Fraction(3, 7) minus Fraction(-1, 4).
    
    a = FractionOps.from_parts(num_a, den_a)
    b = FractionOps.from_parts(-1, 4)
    
    result_fraction = FractionOps.sub(a, b)
    
    # Assemble correct_answer according to the contract:
    # numerator and denominator must be integers (irreducible fraction is guaranteed by from_parts/sub logic usually, 
    # but let's ensure we use standard properties or re-construct if necessary. 
    # The domain ops return Fraction objects which are canonical in Python).
    
    correct_answer = {
        "numerator": result_fraction.numerator,
        "denominator": result_fraction.denominator,
        "canonical_latex": str(result_fraction)  # Standard string representation of a fraction is usually acceptable as 'p/q' or '\frac{...}{...}'? 
                                                # The contract says canonical_latex. Let's check the example in domain API: to_latex returns '\\frac{2}{7}'.
                                                # However, standard Fraction str might be enough if it matches expected format, but let's use to_latex for safety as per "canonical_latex" name.
        }

    correct_answer["canonical_latex"] = FractionOps.to_latex(result_fraction)

    return {
        "question_text": frozen_params.get("expression", "").replace("/", "\\frac{") + "\n\\left( -\n\\right)", 
                   # Wait, the instruction says: use as question_text. The provided text is in Chinese and LaTeX format.
                   # I should output exactly what was given or a slightly formatted version if needed?
                   # "use as question_text" implies using the string directly. But the input has raw latex like \frac{3}{7}. 
                   # Let's stick to the exact provided text for safety, perhaps escaping newlines if it contains them in the prompt representation.
                   # The frozen_params only had expression key. The task description block says: "精確計算 ... 答案須化為最簡分數。"
                   pass

    # Re-reading the input carefully: 
    # ## Frozen task description (use as question_text)
    # 精確計算
    # \[
    # \frac{3}{7}-\left(-\frac{1}{4}\right).
    # \]
    # 答案須化為最簡分數。
    
    raw_question = "精確計算\n\\[\n\\frac{3}{7}-\\left(-\\frac{1}{4}\\right).\n\\]\n答案須化為最簡分數。"

    return {
        "question_text": raw_question,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
