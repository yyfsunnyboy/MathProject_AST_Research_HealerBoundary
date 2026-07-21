import random
from typing import Dict, Any

def generate(level=1, **kwargs) -> Dict[str, Any]:
    p1_min = kwargs.get("p1", [2])[-1] if isinstance(kwargs.get("p1"), list) else 2
    p1_max = kwargs.get("p1", [6])[0] if isinstance(kwargs.get("p1"), list) and len(kwargs["p1"]) > 1 else 6
    
    p2_min = kwargs.get("p2", [1])[-1] if isinstance(kwargs.get("p2"), list) else 1
    p2_max = kwargs.get("p2", [5])[0] if isinstance(kwargs.get("p2"), list) and len(kwargs["p2"]) > 1 else 5
    
    # Select specific values from the frozen ranges provided in task spec: {"p1": [2, 6], "p2": [1, 5]}
    p1 = random.randint(p1_min, p1_max)
    p2 = random.randint(p2_min, p2_max)
    
    # Calculate independent probability fraction (P(A and B) = P(A) * P(B))
    from core.prompts.domain_function_library import FractionOps
    
    frac_p1 = FractionOps.create(p1 / 6 if isinstance(kwargs.get("p1"), list) else p1/6) 
    # Re-evaluating based on standard probability interpretation for discrete uniform [min, max]
    total_outcomes_1 = kwargs["p1"][0] + (kwargs["p1"][-1] - kwargs["p1"][0]) if isinstance(kwargs.get("p1"), list) else 6
    
    # Using the frozen parameters directly as per instruction: p1 range [2,6], p2 range [1,5]
    # Assuming uniform distribution over integers in these ranges.
    n1 = kwargs["p1"][0] + (kwargs["p1"][-1] - kwargs["p1"][0]) if isinstance(kwargs.get("p1"), list) else 4 # count of numbers from 2 to 6 is 5? No, range(2,7) -> 5. Let's assume standard [a,b] inclusive size = b-a+1
    n1_size = kwargs["p1"][-1] - kwargs["p1"][0] + 1 if isinstance(kwargs.get("p1"), list) else 4
    
    # Actually, looking at the frozen parameters: {"p1": [2, 6], "p2": [1, 5]}
    # It implies p1 is chosen from {2,3,4,5,6} (size 5), p2 from {1,2,3,4,5} (size 5).
    # Or it could mean specific values. Given "frozen sampled parameters", let's pick one instance.
    
    val_p1 = random.randint(kwargs["p1"][0], kwargs["p1"][-1])
    val_p2 = random.randint(kwargs["p2"][0], kwargs["p2"][-1])
    
    # Probability of picking a specific number in uniform discrete range [a, b] is 1/(b-a+1)
    prob_1_denom = kwargs["p1"][-1] - kwargs["p1"][0] + 1 if isinstance(kwargs.get("p1"), list) else 6
    prob_2_denom = kwargs["p2"][-1] - kwargs["p2"][0] + 1 if isinstance(kwargs.get("p2"), list) else 5
    
    # Independent probability P(A and B) = (n/total_A) * (m/total_B)
    num_numerator = val_p1 * val_p2
    den_denominator = prob_1_denom * prob_2_denom
    
    frac_result = FractionOps.mul(FractionOps.create(num_numerator), FractionOps.create(den_denominator))
    
    latex_str = FractionOps.to_latex(frac_result)
    
    return {
        "question_text": r"Let $A$ be a random variable uniformly distributed over the integers in the range $[2, 6]$, and let $B$ be a random variable uniformly distributed over the integers in the range $[1, 5]$. If events $A=a_0$ and $B=b_0$ are independent, what is the probability of both occurring? Express your answer as an irreducible fraction.",
        "correct_answer": {
            "numerator": num_numerator,
            "denominator": den_denominator,
            "canonical_latex": latex_str
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }