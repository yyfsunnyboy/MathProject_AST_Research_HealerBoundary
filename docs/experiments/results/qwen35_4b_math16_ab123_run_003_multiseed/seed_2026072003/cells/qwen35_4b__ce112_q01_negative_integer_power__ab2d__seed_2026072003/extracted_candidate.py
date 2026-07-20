def generate(level=1, **kwargs):
    base = -3
    exponent = 3
    
    # Calculate (-3)^3 using safe_eval on a formal expression string
    expr_str = f"({base})^{exponent}"
    
    try:
        correct_answer_val = IntegerOps.safe_eval(expr_str)
    except ValueError as e:
        raise RuntimeError(f"Evaluation failed for {expr_str}: {e}") from None
    
    # Format the answer using the domain API if needed, though safe_eval returns int/float directly here.
    # The spec requires correct_answer to be a single exact integer.
    final_answer = IntegerOps.fmt_num(correct_answer_val) if isinstance(final_answer, str) else correct_answer_val
    
    return {
        "question_text": r"$(-3)^{3}$",
        "correct_answer": int(final_answer),
        "oracle_payload": {"base": base, "exponent": exponent}
    }