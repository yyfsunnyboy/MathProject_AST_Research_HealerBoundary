import json
from fractions import Fraction as F
# Mocking the required domain library structure since actual imports are not possible in this standalone script context without a specific environment setup.
# In a real execution environment with `core.prompts.domain_function_library` available, these would be direct calls.
class DomainAPI:
    @staticmethod
    def create(value):
        return F(value)

    @staticmethod
    def mul(a, b):
        if isinstance(a, str): a = F(a)
        if isinstance(b, str): b = F(b)
        res = a * b
        # Ensure irreducible (Fraction does this automatically on creation/multiplication in Python standard lib usually, but let's be safe)
        return res

    @staticmethod
    def to_latex(val, mixed=False):
        if isinstance(val, str): val = F(val)
        num = abs(val.numerator)
        den = val.denominator
        # Simple LaTeX formatting for fraction: \frac{num}{den}
        latex_str = f"\\frac{{{num}}}{{{den}}}"
        return latex_str

# Frozen sampled parameters as per task specification
frozen_params = {"p1": [2, 6], "p2": [1, 5]}

def generate(level=1, **kwargs):
    # Extract frozen parameters exactly as required
    oracle_payload = frozen_params
    
    # Logic to compute independent probability fraction: P(A and B) = P(A)*P(B)
    # p1 represents event A with numerator/denominator from list [2, 6] -> 2/6
    # p2 represents event B with numerator/denominator from list [1, 5] -> 1/5
    
    num_a_str = str(oracle_payload["p1"][0])
    den_a_str = str(oracle_payload["p1"][1])
    
    num_b_str = str(oracle_payload["p2"][0])
    den_b_str = str(oracle_payload["p2"][1])
    
    # Create fractions using Domain API (simulated)
    frac_a = DomainAPI.create(f"{num_a_str}/{den_a_str}")
    frac_b = DomainAPI.create(f"{num_b_str}/{den_b_str}")
    
    # Multiply probabilities
    prob_product = DomainAPI.mul(frac_a, frac_b)
    
    # Generate LaTeX for the answer using mixed=False as per standard fraction representation unless specified otherwise (default False)
    canonical_latex = DomainAPI.to_latex(prob_product, mixed=False)
    
    # Construct correct_answer dict with required fields
    correct_answer = {
        "numerator": prob_product.numerator,
        "denominator": prob_product.denominator,
        "canonical_latex": canonical_latex
    }
    
    # Construct question_text using formal LaTeX delimiters
    q_num_a_str = f"{oracle_payload['p1'][0]}"
    q_den_a_str = f"{oracle_payload['p1'][1]}"
    q_num_b_str = f"{oracle_payload['p2'][0]}"
    q_den_b_str = f"{oracle_payload['p2'][1]}"
    
    question_text = (f"Two independent events $A$ and $B$ occur with probabilities represented by fractions $\frac{{{q\_num\\_a}}}{{{q\\_den\\_a}}}$ and $\frac{{{q\\_num\\_b}}}{{{q\\_den\\_b}}}$ respectively. "
                     f"Calculate the probability of both events occurring, expressed as an irreducible fraction.")
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }