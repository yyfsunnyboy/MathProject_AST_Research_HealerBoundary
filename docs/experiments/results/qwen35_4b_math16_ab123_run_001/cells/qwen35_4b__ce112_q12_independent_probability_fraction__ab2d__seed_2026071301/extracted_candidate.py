def generate(level=1, **kwargs):
    f_ensures_fraction 0: int * int / (int) -> raw fraction
    
from fractions import gcd as _gcd
import sys

class LocalFractionOps:
    @staticmethod
    def create(value):
        if isinstance(value, tuple) and len(value) == 2:
            num = value[0]
            den = value[1]
            common = _gcd(num, den)
            return (num // common, den // common) # Returns irreducible numerator, denominator as tuple
        
    @staticmethod
    def mul(a, b):
        na, da = a
        nb, db = b
        g = _gcd(na * nb, da * db)
        num = (na * nb) // g
        den = (da * db) // g
        return (num, den)

    @staticmethod
    def to_latex(val):
        if isinstance(val, tuple) and len(val) == 2:
            # Assuming irreducible based on spec "irreducible fraction" requirement often handled by create/mul correctly or we enforce it.
            # If the input is not reduced yet (unlikely for p1/p2 which are given as integers), reduce first.
            n, d = val
            g = _gcd(n, d)
            return f"{n // g}/{d // g}"
        raise ValueError("Expected tuple of numerator and denominator")

# Task: independent_probability_fraction -> P(A intersection B) where A has prob p1, B has prob p2.
# Input format: ["p", "q"] likely means probability = p/q? Or is it a sample list [n, d]? 
# Spec says "Frozen sampled parameters": {"p1": [2, 6], "p2": [1, 5]}
# This implies P(A) = 2/6 and P(B) = 1/5. We need to calculate independent probability product (A * B).

frozen_params = {
    "p1": [2, 6], 
    "p2": [1, 5]
}

def generate(level=1, **kwargs):
    p1_tuple = frozen_params["p1"] # List -> Tuple expected by ops? Or just pass directly. Let's normalize to tuple for safety in logic below if needed, but spec says return exact dict keys.
    p2_tuple = frozen_params["p2"]

    # Convert lists to tuples for consistent domain API usage simulation
    op_p1 = LocalFractionOps.create(p1_tuple) 
    op_p2 = LocalFractionOps.create(p2_tuple) 

    result_op = LocalFractionOps.mul(op_p1, op_p2)
    
    num_simplified, den_simplified = result_op

    canonical_latex_str = str(num_simplified).split('/')[0] + "/" + str(den_simplified)[len(str(num_simplified))-3:] # Wait no simple formatting. Let's use the to_latex helper which expects tuple or raw frac logic? 
    # Re-checking LocalFractionOps.to_latex signature: returns string representation of fraction n/d
    lat_result = f"{num_simplified}/{den_simplified}"

    question_text = r"\text{Calculate the probability that both independent events occur, given } P(A) = \frac{\text{{{p1[0]}}}{\text{{{p1[1]]}}} \text{ and } P(B) = \frac{\text{{{p2[0]}}}{\text{{{p2[1]]}}}}. The result should be an irreducible fraction."

    # Prepare correct answer components
    numerator_val = num_simplified
    denominator_val = den_simplified
    
    oracle_payload = frozen_params 

    return {
        "question_text": question_text, 
        "correct_answer": f"numerator: {{{numerator_val}}}, denominator: {{{denominator_val}}}, canonical_latex: \\\\frac{{{{{numerator_val}}}}}{{{denominator_val}}}", # Correct latex format requested. Need formal LaTeX delimiters around fraction.
        "oracle_payload": oracle_payload
    }