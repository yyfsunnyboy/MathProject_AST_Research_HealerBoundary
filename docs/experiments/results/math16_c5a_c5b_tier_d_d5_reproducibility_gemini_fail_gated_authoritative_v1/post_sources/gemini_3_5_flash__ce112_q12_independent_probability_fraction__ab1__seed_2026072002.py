def generate(level=1, **kwargs):
    import math

    p1 = [2, 6]
    p2 = [1, 5]
    
    num = p1[0] * p2[0]
    den = p1[1] * p2[1]
    
    g = math.gcd(num, den)
    ans_num = num // g
    ans_den = den // g
    
    question_text = (
        f"The probability of event $A$ occurring is $\\frac{{{p1[0]}}}{{{p1[1]}}}$ "
        f"and the probability of event $B$ occurring is $\\frac{{{p2[0]}}}{{{p2[1]}}}$. "
        f"If $A$ and $B$ are independent events, what is the probability that both events occur?"
    )
    
    correct_answer = {
        "numerator": ans_num,
        "denominator": ans_den,
        "canonical_latex": f"\\frac{{{ans_num}}}{{{ans_den}}}"
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "p1": p1,
            "p2": p2
        }
    }