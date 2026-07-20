def generate(level=1, **kwargs):
    import json
    
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    count = IntegerOps.safe_eval(f"len([x for x in range(10**9 + 7) if {IntegerOps.is_divisible.__name__}(x, {divisor_val}) and {IntegerOps.is_divisible.__name__}(x, {multiple_val}))")

    correct_answer_json = json.dumps({"count": count}, ensure_ascii=False).replace("\\", "\\\\")
    
    question_text = r"""Find the number of integers $n$ such that $1 \le n < 10^9 + 7$, where $n$ is a multiple of both $\{divisor\_of\}$ and $\{multiple\_of\}$. The count should be computed modulo $(10^9 + 7)$."""

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": json.loads(correct_answer_json),
        "oracle_payload": oracle_payload
    }