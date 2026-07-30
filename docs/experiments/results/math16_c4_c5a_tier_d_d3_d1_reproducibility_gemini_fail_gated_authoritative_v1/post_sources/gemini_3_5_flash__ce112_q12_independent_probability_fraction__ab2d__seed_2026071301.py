from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    p1 = [2, 6]
    p2 = [1, 5]
    
    # Create fractions using FractionOps
    p1_frac = FractionOps.create(f"{p1[0]}/{p1[1]}")
    p2_frac = FractionOps.create(f"{p2[0]}/{p2[1]}")
    
    # Calculate the independent probability (product of the two probabilities)
    ans_frac = FractionOps.mul(p1_frac, p2_frac)
    
    # Format LaTeX for the question
    p1_latex = f"\\frac{{{p1[0]}}}{{{p1[1]}}}"
    p2_latex = f"\\frac{{{p2[0]}}}{{{p2[1]}}}"
    
    question_text = (
        f"If the probability of event $A$ occurring is ${p1_latex}$ and the "
        f"probability of independent event $B$ occurring is ${p2_latex}$, "
        f"what is the probability that both events occur? Express your answer as a simplified fraction."
    )
    
    correct_answer = {
        "numerator": ans_frac.numerator,
        "denominator": ans_frac.denominator,
        "canonical_latex": FractionOps.to_latex(ans_frac)
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "p1": p1,
            "p2": p2
        }
    }