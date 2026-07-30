from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    p1 = [2, 6]
    p2 = [1, 5]
    
    f1 = FractionOps.create(p1[0], p1[1])
    f2 = FractionOps.create(p2[0], p2[1])
    res = FractionOps.mul(f1, f2)
    
    numerator = res["numerator"]
    denominator = res["denominator"]
    canonical_latex = res["canonical_latex"]
    
    question_text = f"Two independent events $A$ and $B$ have probabilities $P(A) = \\frac{{{p1[0]}}}{{{p1[1]}}}$ and $P(B) = \\frac{{{p2[0]}}}{{{p2[1]}}}$. What is the probability that both events occur? Express your answer as an irreducible fraction."
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
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