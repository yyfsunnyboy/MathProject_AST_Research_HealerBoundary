from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    p1 = [2, 6]
    p2 = [1, 5]
    
    # Create fractions
    f1 = FractionOps.create(f"{p1[0]}/{p1[1]}")
    f2 = FractionOps.create(f"{p2[0]}/{p2[1]}")
    
    # Multiply them
    ans = FractionOps.mul(f1, f2)
    
    # Format question text
    p1_latex = f"\\frac{{{p1[0]}}}{{{p1[1]}}}"
    p2_latex = f"\\frac{{{p2[0]}}}{{{p2[1]}}}"
    question_text = f"Two independent events $A$ and $B$ have probabilities $P(A) = {p1_latex}$ and $P(B) = {p2_latex}$. What is the probability that both events occur? Express your answer as a simplified fraction."
    
    # Correct answer
    correct_answer = {
        "numerator": ans.numerator,
        "denominator": ans.denominator,
        "canonical_latex": FractionOps.to_latex(ans)
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "p1": p1,
            "p2": p2
        }
    }