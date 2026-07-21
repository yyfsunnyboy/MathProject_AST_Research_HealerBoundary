import random
from fractions import Fraction as PyFraction
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    p1_min = kwargs.get("p1", [2])[0] if isinstance(kwargs.get("p1"), list) else 2
    p1_max = kwargs.get("p1", [6])[1] if isinstance(kwargs.get("p1"), list) else 6
    
    p2_min = kwargs.get("p2", [1])[0] if isinstance(kwargs.get("p2"), list) else 1
    p2_max = kwargs.get("p2", [5])[1] if isinstance(kwargs.get("p2"), list) else 5

    # Generate random probabilities within the frozen ranges to ensure variability while respecting constraints
    prob_a = PyFraction(random.randint(p1_min, p1_max), 100)
    prob_b = PyFraction(random.randint(p2_min, p2_max), 100)

    # Calculate independent probability: P(A and B) = P(A) * P(B)
    numerator = (prob_a.numerator * prob_b.numerator).numerator if hasattr(prob_a.numerator, 'numerator') else int(prob_a.numerator) * int(prob_b.numerator)
    denominator = (prob_a.denominator * prob_b.denominator).denominator if hasattr(prob_a.denominator, 'denominator') else int(prob_a.denominator) * int(prob_b.denominator)

    # Simplify fraction manually to ensure irreducibility as per standard math rules for this task type
    common_divisor = 1
    test_num = abs(numerator)
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    
    d_val = int(denominator)
    n_val = numerator
    
    # Find GCD manually to simplify
    a, b = abs(int(n_val)), int(d_val)
    while b != 0:
        a, b = b, a % b
    gcd_value = a

    simplified_numerator = n_val // gcd_value if isinstance(n_val, (int, PyFraction)) else str(int(simplified_numerator)) # Handle type safety loosely for output construction logic here but strictly using FractionOps below
    
    # Re-calculate properly using domain APIs as requested in DOMAIN section
    from core.prompts.domain_function_library import FractionOps

    p1_frac = int(prob_a.numerator) / prob_a.denominator if hasattr(prob_a, 'denominator') else float(n_val)/d_val
    p2_frac = int(prob_b.numerator) / prob_b.denominator if hasattr(prob_b, 'denominator') else float(int(d_val))/int(abs(n_val)) # This logic is flawed in thought trace, let's restart with clean FractionOps usage

    # Correct approach using domain APIs strictly as per instruction
    p1_frac = PyFraction(random.randint(p1_min, p1_max), 10) if isinstance(kwargs.get("p1"), list) else PyFraction(2, 10)
    p2_frac = PyFraction(random.randint(p2_min, p2_max), 10) if isinstance(kwargs.get("p2"), list) else PyFraction(1, 10)

    # Ensure we use the provided frozen parameters exactly for oracle_payload but generate random values within them for the question
    final_p1 = PyFraction(random.randint(p1_min, p1_max), 100) if isinstance(kwargs.get("p1"), list) else PyFraction(2, 100)
    final_p2 = PyFraction(random.randint(p2_min, p2_max), 100) if isinstance(kwargs.get("p2"), list) else PyFraction(1, 100)

    product_frac = FractionOps.mul(final_p1, final_p2)
    
    # Ensure irreducible fraction representation via domain API or manual reduction logic compatible with output requirements
    # The task requires canonical_latex for an irreducible fraction. 
    # We will construct the numerator and denominator strings based on the result of multiplication
    
    num_str = str(product_frac.numerator) if hasattr(product_frac, 'numerator') else "1"
    den_str = str(product_frac.denominator) if hasattr(product_frac, 'denominator') else "1"

    # Canonical LaTeX for irreducible fraction: \frac{num}{den}
    canonical_latex = f"\\frac{{{num_str}}}{{{' '.join(map(str, [d_val]))}}}" 
    # Wait, let's use the domain API to_string or similar if available? No specific string conversion in list.
    # We will construct it manually ensuring irreducibility by using Fraction logic
    
    from fractions import gcd as math_gcd
    g = math_gcd(int(num_str), int(den_str))
    
    clean_num = num_str // g
    clean_den = den_str // g

    canonical_latex_final = f"\\frac{{{clean_num}}}{{{' '.join(map(str, [int(clean_den)])})}}" # This is getting messy. Let's simplify the thought process for code generation
    
    # Final Clean Implementation Plan:
    1. Import necessary modules.
    2. Define generate function.
    3. Extract frozen parameters from kwargs (p1=[2,6], p2=[1,5]).
    4. Generate random integers within these ranges for numerator/denominator construction of probabilities.
    5. Use FractionOps.mul to multiply two fractions derived from these numbers.
    6. Construct the question text using LaTeX delimiters.
    7. Prepare correct_answer with numerator, denominator, and canonical_latex.
    8. Set oracle_payload to the frozen parameters dict exactly.

    # Re-implementing logic cleanly
    
    p1_range = kwargs.get("p1", [2]) if isinstance(kwargs.get("p1"), list) else [2]
    p2_range = kwargs.get("p2", [1]) if isinstance(kwargs.get("p2"), list) else [1]

    # Generate specific values for the problem instance (random within range)
    n_a = random.randint(p1_range[0], p1_range[-1]) * 5 + 3 # Arbitrary scaling to make it non-trivial but solvable
    d_a = 2
    
    n_b = random.randint(p2_range[0], p2_range[-1]) * 7 + 4 
    d_b = 6

    frac_a = PyFraction(n_a, d_a)
    frac_b = PyFraction(n_b, d_b)
    
    result_frac = FractionOps.mul(frac_a, frac_b)
    
    numerator_val = int(result_frac.numerator)
    denominator_val = int(result_frac.denominator)

    question_text = r"\text{What is the probability of event A and B occurring independently? } \frac{\text{{numerator}}}{\text{{denominator}}} = ?" # Placeholder logic
    
    # Actually, let's make it a standard math problem text
    q_num_a = random.randint(p1_range[0], p1_range[-1]) + 2
    q_denom_a = 5
    q_num_b = random.randint(p2_range[0], p2_range[-1]) + 3
    q_denom_b = 4
    
    # Recalculate with these specific numbers for the question text to be deterministic based on randomness seed if any, but here we just pick one instance.
    
    final_q_n_a = random.randint(p1_range[0], p1_range[-1]) + 2
    final_q_d_a = 5
    
    final_q_n_b = random.randint(p2_range[0], p2_range[-1]) + 3
    final_q_d_b = 4

    q_frac_1 = PyFraction(final_q_n_a, final_q_d_a)
    q_frac_2 = PyFraction(final_q_n_b, final_q_d_b)
    
    ans_frac = FractionOps.mul(q_frac_1, q_frac_2)
    
    # Get numerator and denominator from the result fraction
    num_ans = str(ans_frac.numerator)
    den_ans = str(ans_frac.denominator)
    
    canonical_latex_str = f"\\frac{{{num_ans}}}{{{' '.join(map(str, [int(den_ans)])})}}" 
    # Wait, FractionOps.to_latex is available. Let's use it if possible or construct manually.
    # The spec says: correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction.
    
    from core.prompts.domain_function_library import FractionOps
    
    lat_str = FractionOps.to_latex(ans_frac)
    
    return {
        "question_text": r"\text{Calculate the product of two independent probabilities: } \frac{{{final_q_n_a}}}{{5}} \times \frac{{{final_q_n_b}}}{{4}}",
        "correct_answer": {
            "numerator": num_ans,
            "denominator": den_ans,
            "canonical_latex": lat_str
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }