from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse frozen_params to create fractions for the two groups.
    oracle_payload = kwargs.get("oracle_payload", {})
    
    p1_num = oracle_payload["p1"][0]
    p1_den = oracle_payload["p1"][1]
    a = FractionOps.from_parts(p1_num, p1_den)  # Probability of success in group 1
    
    p2_num = oracle_payload["p2"][0]
    p2_den = oracle_payload["p2"][1]
    b = FractionOps.from_parts(p2_num, p2_den)  # Probability of success in group 2

    # Calculate the probability that both events occur (independent multiplication).
    result_fraction = FractionOps.mul(a, b)
    
    # Construct the correct_answer according to the task-specific contract.
    canonical_latex = FractionOps.to_latex(result_fraction)
    
    return {
        "question_text": oracle_payload["p1"][0] + "/" + str(oracle_payload["p1"][1]) + "\n" + 
                         oracle_payload["p2"][0] + "/" + str(oracle_payload["p2"][1]), # Placeholder for stem logic if needed, but prompt says use provided text.
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }

# Correction: The question_text must be the exact string provided in the task block.
def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Use the frozen_params directly as oracle_payload (passed via kwargs or extracted if needed)
    # Based on instructions: "oracle_payload must equal this object" which is provided in the task block.
    # We assume it's passed in **kwargs for a generic generate function, 
    # but since no specific input args are given other than level and kwargs, we construct from frozen_params directly if not present?
    # Actually, looking at typical patterns: oracle_payload should be extracted or constructed to match the requirement.
    # The prompt says "oracle_payload must equal this object". I will assume it's passed in **kwargs for robustness 
    # OR simply reconstruct based on the task description constants if strictly required by 'frozen_params' availability.
    
    # Re-reading: "Frozen params (oracle_payload must equal this object)" is listed under Task section.
    # In a real scenario, these would be injected into kwargs or global scope for generation. 
    # I will assume they are available in **kwargs as 'frozen_params' to ensure the function works generically.
    
    frozen_params = kwargs.get("frozen_params", {})
    
    p1_num = frozen_params["p1"][0]
    p1_den = frozen_params["p1"][1]
    a = FractionOps.from_parts(p1_num, p1_den)

    p2_num = frozen_params["p2"][0]
    p2_den = frozen_params["p2"][1]
    b = FractionOps.from_parts(p2_num, p2_den)

    # Independent probability: P(A and B) = P(A) * P(B)
    result_fraction = FractionOps.mul(a, b)
    
    canonical_latex = FractionOps.to_latex(result_fraction)
    
    return {
        "question_text": "第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。",
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }

# Final clean implementation ensuring no external dependencies beyond the allowed import.
from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Retrieve oracle payload from kwargs (as per typical task injection pattern) or use provided constants if strictly static?
    # The prompt implies these are 'frozen' for this specific run but the function should be generic. 
    # I will assume they are passed in `**kwargs` under a key like `oracle_payload`. If not, we might need to infer from context which is risky.
    # However, looking at the instruction "oracle_payload must equal this object", and the task block provides it explicitly.
    # To be safe and compliant with 'generate(level=1, **kwargs)', I will look for `frozen_params` in kwargs as that matches the description of frozen data.
    
    oracle_data = kwargs.get("frozen_params") or { "p1": [2, 6], "p2": [1, 5] } # Fallback to task constants if not passed
    
    p1_num = oracle_data["p1"][0]
    p1_den = oracle_data["p1"][1]
    
    p2_num = oracle_data["p2"][0]
    p2_den = oracle_data["p2"][1]

    # Create fractions representing probabilities: 2/6 and 1/5
    frac_a = FractionOps.from_parts(p1_num, p1_den)
    frac_b = FractionOps.from_parts(p2_num, p2_den)

    # Multiply them for independent events
    result_frac = FractionOps.mul(frac_a, frac_b)

    return {
        "question_text": "第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。",
        "correct_answer": {
            "numerator": result_frac.numerator,
            "denominator": result_frac.denominator,
            "canonical_latex": FractionOps.to_latex(result_frac)
        },
        "oracle_payload": oracle_data
    }

# Wait, the previous block had a duplicate definition. I will provide only one clean function at the end of this thought process to be outputted.
