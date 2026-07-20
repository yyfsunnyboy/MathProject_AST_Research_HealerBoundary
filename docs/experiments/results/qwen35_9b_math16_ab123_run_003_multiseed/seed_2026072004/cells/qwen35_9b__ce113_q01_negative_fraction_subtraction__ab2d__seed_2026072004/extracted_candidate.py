def generate(level=1, **kwargs):
    frozen_params: Dict[str, Any] = {"expression": "3/7 - (-1/4)"}
    
    # Parse expression manually to ensure correctness without external parsers if needed, 
    # but spec says oracle_payload must exactly equal frozen sampled parameters.
    # We just return the dict as required. The task logic is internal validation for us.
    
    expr = "3/7 - (-1/4)"
    
    # Calculate correct answer using domain APIs or standard math if library fails, 
    # but spec mandates use of FractionOps.create and sub where possible.
    # Let's parse the string to numbers/tuples first.
    
    def parse_frac(s):
        s = s.strip()
        if s.startswith('-'):
            parts = [int(p) for p in s[1:].split('/')]
            return (parts[0], parts[1])
        elif '/' in s:
            parts = [int(p) for p in s.split('/')]
            return (parts[0], parts[1])
        else:
            val = int(s)
            return (val, 1)

    term1_str = "3/7"
    term2_str = "-(-1/4)" # The expression is A - B where B is (-1/4). 
    # Actually the string is "3/7 - (-1/4)". This means Term1 minus Term2.
    # Term 1: 3/7 -> (3, 7)
    # Term 2 inside parens: -1/4 -> (-1, 4). The operation is subtraction of this term? 
    # Wait, standard math notation "a - b" where b = "-(-1/4)" implies adding positive 1/4.
    # Let's interpret the string literally as an expression tree if possible or simplify:
    # Value = (3/7) - (-1/4) = 3/7 + 1/4
    
    t1_n, t1_d = parse_frac("3/7")
    
    inner_val_str = "-1/4"
    inner_t2_n, inner_t2_d = parse_frac(inner_val_str) # This gives (-1, 4) representing -1/4.
    
    # The expression is: (3/7) - [(-1/4)] 
    # So we subtract the fraction represented by "-1/4".
    # Subtraction of a negative number becomes addition.
    
    # Using FractionOps.sub(a, b) computes a - b.
    result_tuple = FractionOps.sub((t1_n, t1_d), (inner_t2_n, inner_t2_d))
    
    n_ans, d_ans = result_tuple
    
    # Generate LaTeX for the answer
    latex_answer_str = f"\\frac{{{n_ans}}}{{{d_ans}}}"
    
    if n_ans < 0:
        latex_answer_str = rf"-\\frac{{{-n_ans}}}{{{d_ans}}}"

    correct_answer_dict = {
        "numerator": n_ans,
        "denominator": d_ans,
        "canonical_latex": latex_answer_str
    }
    
    question_text = r"Compute the result of \[ 3/7 - (-1/4) \]."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }