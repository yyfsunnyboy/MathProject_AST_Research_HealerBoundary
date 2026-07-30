import fractions

def generate(level=1, **kwargs):
    # Frozen parameters
    p1 = [2, 6]
    p2 = [1, 5]
    
    # Calculate the product of the two probabilities
    f1 = fractions.Fraction(p1[0], p1[1])
    f2 = fractions.Fraction(p2[0], p2[1])
    ans_fraction = f1 * f2
    
    numerator = ans_fraction.numerator
    denominator = ans_fraction.denominator
    
    if denominator == 1:
        canonical_latex = f"{numerator}"
    else:
        canonical_latex = f"\\frac{{{numerator}}}{{{denominator}}}"
        
    question_text = (
        f"The probability of event $A$ occurring is $\\frac{{{p1[0]}}}{{{p1[1]}}}$ "
        f"and the probability of event $B$ occurring is $\\frac{{{p2[0]}}}{{{p2[1]}}}$. "
        f"If $A$ and $B$ are independent events, what is the probability that both events occur? "
        f"Express your answer as a simplified fraction."
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "p1": p1,
            "p2": p2
        }
    }