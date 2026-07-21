import math
from fractions import Fraction

def generate(level=1, **kwargs):
    p1_list = kwargs.get("p1", [2, 6])
    p2_list = kwargs.get("p2", [1, 5])
    
    # Select random values from the frozen sampled parameters lists (simulating a single draw)
    p1_val = p1_list[0] if len(p1_list) > 0 else 2
    p2_val = p2_list[0] if len(p2_list) > 0 else 1
    
    # Calculate probability of independent events: P(A and B) = P(A) * P(B)
    prob_a = Fraction(p1_val, 6)
    prob_b = Fraction(p2_val, 5)
    
    total_prob = prob_a * prob_b
    
    numerator = int(total_prob.numerator)
    denominator = int(total_prob.denominator)
    
    question_text = r"Let $A$ and $B$ be independent events. If $P(A) = \frac{2}{6}$ and $P(B) = \frac{1}{5}$, what is the probability of both $A$ and $B$ occurring? Express your answer as an irreducible fraction $\frac{n}{d}$. Find the values of $n$ and $d$."
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": f"\\frac{{{numerator}}}{{"{denominator}"}}"
    }
    
    oracle_payload = {"p1": p1_list, "p2": p2_list}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }