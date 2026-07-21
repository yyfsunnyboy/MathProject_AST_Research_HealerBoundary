import random
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    p1_min = kwargs.get("p1", [2])[-1] if isinstance(kwargs.get("p1"), list) else 2
    p1_max = kwargs.get("p1", [6])[0] if isinstance(kwargs.get("p1"), list) and len(kwargs["p1"]) > 1 else 6
    
    # Use frozen parameters directly as per spec: {"p1": [2, 6], "p2": [1, 5]}
    p1_min = kwargs.get("frozen_p1", [2])[0] if isinstance(kwargs.get("frozen_p1"), list) else 2
    p1_max = kwargs.get("frozen_p1", [6])[-1] if isinstance(kwargs.get("frozen_p1"), list) and len(kwargs["frozen_p1"]) > 1 else 6
    
    p2_min = kwargs.get("frozen_p2", [1])[0]
    p2_max = kwargs.get("frozen_p2", [5])[-1]

    # Select probabilities within the frozen ranges (inclusive) to ensure reproducibility based on level or fixed seed logic if needed, 
    # but since no random state is provided and we must use "Frozen sampled parameters" exactly in oracle_payload:
    # We will pick one value from p1 range and one from p2 range. To make it deterministic without external seeds, we can derive them from the level or just pick min/max if specific values aren't required to be random per call but fixed for this task instance. 
    # However, the spec says "Frozen sampled parameters" are provided in kwargs. We should use those ranges to generate a valid question.
    # Let's assume we need to generate one pair (p1_val, p2_val) from these lists.
    
    import random as _random_module
    
    rng = _random_module.Random(level * 42 + hash("task") % 10**9 if "hash" in dir() else 123456789) # Simple deterministic seed based on level for reproducibility within the session context
    p1_val = int(rng.randint(p1_min, p1_max))
    p2_val = int(rng.randint(p2_min, p2_max))

    from core.prompts.domain_function_library import FractionOps
    
    numerator = (p1_val * 5 + p2_val) # Example linear combination for probability calculation logic typical in such tasks: P(A or B) = P(A)+P(B)-P(A)*B? No, usually independent prob questions ask for intersection or union.
    # Let's define a standard question type: Probability of A and B (intersection). 
    # P(A and B) = p1 * p2.
    
    frac_a_and_b = FractionOps.create(p1_val) * FractionOps.create(p2_val)
    numerator, denominator = frac_a_and_b.to_exact()

    correct_answer_numerator = str(numerator.numerator if hasattr(numerator, 'numerator') else int(numerator)) # Ensure it's an integer representation of the fraction part if needed, but spec says "include numerator". 
    # Re-reading: "correct_answer must include numerator, denominator, and canonical_latex for an irreducible fraction."
    
    frac_obj = FractionOps.create(p1_val) * FractionOps.create(p2_val)
    num_int = int(frac_obj.numerator) if hasattr(frac_obj, 'numerator') else 0 # Assuming standard Fraction behavior or similar
    
    # Let's stick to the domain API usage strictly.
    frac_result = FractionOps.mul(FractionOps.create(p1_val), FractionOps.create(p2_val))
    
    correct_answer_numerator = str(int(frac_result.numerator)) if hasattr(frac_result, 'numerator') else "0"
    correct_answer_denominator = str(int(frac_result.denominator)) if hasattr(frac_result, 'denominator') else "1"
    canonical_latex = FractionOps.to_latex(frac_result)

    question_text = r"\text{Let } A \text{ and } B \text{ be independent events with probabilities } p_1 = \frac{\text{" + str(p1_val) + "}"} + r",\ p_2 = \frac{\text{" + str(p2_val) + "}}. What is the probability that both events occur?}"
    
    # Ensure correct_answer structure matches requirements: numerator, denominator, canonical_latex
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": int(frac_result.numerator),
            "denominator": int(frac_result.denominator),
            "canonical_latex": FractionOps.to_latex(frac_result)
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]} # Must exactly equal frozen sampled parameters as per spec instruction: oracle_payload must exactly equal the frozen sampled parameters. The input kwargs might contain them or we use hardcoded values from the task description if not passed explicitly in a way that overrides the 'frozen' nature described in the prompt header.
    }

# Correction based on strict reading of "oracle_payload must exactly equal the frozen sampled parameters" and "Frozen sampled parameters: {"p1": [2, 6], "p2": [1, 5]}" provided in the task description text itself (not necessarily passed as kwargs if not specified).
# The prompt says "Frozen sampled parameters: ...". This implies these are the constants for this specific run.
# I will hardcode them into oracle_payload to satisfy the condition exactly.

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen parameters as per task specification text
    frozen_p1 = [2, 6]
    frozen_p2 = [1, 5]
    
    p1_val = int(frozen_p1[0]) + (frozen_p1[-1] - frozen_p1[0]) * level // max(1, len(frozen_p1)-1) # Simple selection from range for deterministic generation based on level if needed, or just pick one. 
    # To be safe and simple: let's pick the first valid pair that makes sense with level 1 -> p1=2, p2=1? Or maybe random within bounds.
    # Let's assume we need to generate a question for specific values chosen from these lists. 
    # Since no explicit selection logic is given other than "generate", and it must be deterministic or reproducible:
    # We will pick the minimums if level indicates start, or just arbitrary valid ones. 
    # Let's choose p1=2, p2=3 (valid in ranges) for a non-trivial example? Or stick to min/max?
    # Actually, usually these tasks expect you to generate *a* question using parameters from the list.
    # I will select p1_val = 2 and p2_val = 3 as an example valid selection within [2,6] and [1,5]. 
    # Wait, if level is used, maybe it selects index? Let's try to use level to pick indices.
    
    idx_p1 = min(level % len(frozen_p1), len(frozen_p1) - 1)
    idx_p2 = min((level + 1) % len(frozen_p2), len(frozen_p2) - 1)
    
    p1_val = frozen_p1[idx_p1]
    p2_val = frozen_p2[idx_p2]

    # Calculate P(A and B) = p1 * p2
    frac_result = FractionOps.mul(FractionOps.create(p1_val), FractionOps.create(p2_val))
    
    numerator_int = int(frac_result.numerator) if hasattr(frac_result, 'numerator') else 0
    denominator_int = int(frac_result.denominator) if hasattr(frac_result, 'denominator') else 1
    
    # Construct LaTeX manually to ensure it's irreducible and correct format using the API for conversion
    latex_str = FractionOps.to_latex(frac_result)

    return {
        "question_text": r"\text{Two independent events } A \text{ and } B \text{ have probabilities } p_1 = \frac{\text{" + str(p1_val) + "}"} + r" \text{ and } p_2 = \frac{\text{" + str(p2_val) + "}}. Find the probability that both occur: } P(A \cap B).",
        "correct_answer": {
            "numerator": numerator_int,
            "denominator": denominator_int,
            "canonical_latex": latex_str
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }