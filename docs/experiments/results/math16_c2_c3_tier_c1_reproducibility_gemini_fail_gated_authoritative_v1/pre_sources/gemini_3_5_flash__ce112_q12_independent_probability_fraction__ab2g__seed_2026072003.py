from fractions import Fraction

def generate(level=1, **kwargs):
    p1 = [2, 6]
    p2 = [1, 5]
    
    f1 = Fraction(p1[0], p1[1])
    f2 = Fraction(p2[0], p2[1])
    ans_fraction = f1 * f2
    
    numerator = ans_fraction.numerator
    denominator = ans_fraction.denominator
    
    question_text = (
        f"If the probability of event $A$ is $\\frac{{{p1[0]}}}{{{p1[1]}}}$ and the probability of "
        f"event $B$ is $\\frac{{{p2[0]}}}{{{p2[1]}}}$, and $A$ and $B$ are independent events, "
        f"what is the probability that both events occur? Express your answer as a fraction in simplest form."
    )
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": f"\\frac{{{numerator}}}{{{denominator}}}"
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "p1": p1,
            "p2": p2
        }
    }