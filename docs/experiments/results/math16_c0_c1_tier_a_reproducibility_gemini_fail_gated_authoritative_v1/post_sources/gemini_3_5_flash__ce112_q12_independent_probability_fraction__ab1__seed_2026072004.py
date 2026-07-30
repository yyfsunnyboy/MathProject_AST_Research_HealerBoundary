import math

def generate(level=1, **kwargs):
    p1 = kwargs.get("p1", [2, 6])
    p2 = kwargs.get("p2", [1, 5])
    
    num = p1[0] * p2[0]
    den = p1[1] * p2[1]
    g = math.gcd(num, den)
    ans_num = num // g
    ans_den = den // g
    
    question_text = f"Two independent events $A$ and $B$ have probabilities $P(A) = \\frac{{{p1[0]}}}{{{p1[1]}}}$ and $P(B) = \\frac{{{p2[0]}}}{{{p2[1]}}}$. What is the probability that both events occur?"
    
    correct_answer = {
        "numerator": ans_num,
        "denominator": ans_den,
        "canonical_latex": f"\\frac{{{ans_num}}}{{{ans_den}}}"
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