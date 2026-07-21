import random
from typing import Dict, Any

# Frozen sampled parameters as per task specification
FROZEN_PARAMS = {"p1": [2, 6], "p2": [1, 5]}


def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    """
    Generates a probability fraction problem based on frozen parameters.
    
    The task involves calculating the product of two independent probabilities p1 and p2.
    Given lists for possible values [p1_min, p1_max] and [p2_min, p2_max], 
    we select one value from each list to form a specific probability scenario.
    """
    # Select random integers within the frozen parameter ranges (inclusive)
    val_p1 = random.randint(*FROZEN_PARAMS["p1"])
    val_p2 = random.randint(*FROZEN_PARAMS["p2"])

    # Define probabilities as fractions: p1_val / 6 and p2_val / 5
    # Note: The problem implies a denominator of 6 for the first probability 
    # (since max value is 6) and 5 for the second.
    
    from core.prompts.domain_function_library import FractionOps
    
    numerator = val_p1 * val_p2
    denominator = 30  # LCM(6, 5) or simply 6*5 since independent events multiply denominators directly if bases are distinct primes like this context implies standard probability multiplication (e.g., P(A and B))

    fraction_result = FractionOps.create(numerator) / FractionOps.create(denominator)
    
    # Simplify to irreducible form using domain API logic implicitly handled by division or manual reduction if needed, 
    # but the task requires canonical latex for an irreducible fraction.
    # We will compute GCD manually to ensure irreducibility before formatting as per standard math requirements unless FractionOps handles it internally which is not specified here beyond creation/mul/to_latex.
    
    from fractions import gcd
    
    common = gcd(numerator, denominator)
    num_irred = numerator // common
    den_irred = denominator // common

    # Generate LaTeX for the irreducible fraction using domain API if available or standard formatting
    # The task specifies correct_answer must include canonical_latex. 
    # Using FractionOps.to_latex on a constructed fraction object would be ideal, but we need to construct it first.
    
    frac_obj = FractionOps.create(num_irred) / FractionOps.create(den_irred) if False else None
    
    # Reconstruct using domain API for the final answer string as requested: 
    # "correct_answer must include numerator, denominator, and canonical_latex"
    latex_str = f"{num_irred} \\over {den_irred}"

    return {
        "question_text": r"\text{Calculate the product of two independent probabilities } p_1 \text{ and } p_2. \text{ If } P(A) = \frac{\text{" + str(val_p1) + "}"} + r" that there are 6 equally likely outcomes, and } P(B) = \frac{\text{" + str(val_p2) + "}"} + r" that there are 5 equally likely outcomes. What is the probability of both events occurring? Express your answer as an irreducible fraction.",
        "correct_answer": {
            "numerator": num_irred,
            "denominator": den_irred,
            "canonical_latex": latex_str
        },
        "oracle_payload": FROZEN_PARAMS.copy()
    }