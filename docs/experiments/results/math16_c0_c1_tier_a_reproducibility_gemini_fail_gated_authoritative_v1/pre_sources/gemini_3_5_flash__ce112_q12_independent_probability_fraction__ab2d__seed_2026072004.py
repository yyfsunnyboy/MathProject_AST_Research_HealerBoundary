from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    p1 = [2, 6]
    p2 = [1, 5]
    
    f1 = FractionOps.create(f"{p1[0]}/{p1[1]}")
    f2 = FractionOps.create(f"{p2[0]}/{p2[1]}")
    
    ans = FractionOps.mul(f1, f2)
    
    p1_str = f"\\frac{{{p1[0]}}}{{{p1[1]}}}"
    p2_str = f"\\frac{{{p2[0]}}}{{{p2[1]}}}"
    
    question_text = f"If the probability of event $A$ occurring is ${p1_str}$ and the probability of event $B$ occurring is ${p2_str}$, and $A$ and $B$ are independent events, what is the probability that both events occur? Express your answer as a simplified fraction."
    
    correct_answer = {
        "numerator": ans.numerator,
        "denominator": ans.denominator,
        "canonical_latex": FractionOps.to_latex(ans)
    }
    
    oracle_payload = {
        "p1": p1,
        "p2": p2
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }