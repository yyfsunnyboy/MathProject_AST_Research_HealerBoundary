def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    frozen_params = {
        "equation": equation,
        "order": order,
        "target": target
    }
    
    # Parse the specific quadratic case: (x-2)^2 = 3 => x^2 - 4x + 1 = 0
    a_coefficient = 1
    b_coefficient = -4
    c_coefficient = 1
    
    discriminant = b_coefficient**2 - 4*a_coefficient*c_coefficient
    sqrt_discriminant = math.sqrt(discriminant)
    
    # Roots: x = (-b ± sqrt(D)) / (2a)
    root_a_num = -b_coefficient + sqrt_discriminant
    root_b_num = -b_coefficient - sqrt_discriminant
    
    # Normalize to form a/b where b is the radical part for canonical representation if needed, 
    # but here we express as simplified fractions or radicals.
    # Since 2a+b is requested and order is a>b:
    # Root A (larger): (-(-4) + sqrt(16-4)) / 2 = (4 + sqrt(12))/2 = 2 + sqrt(3)
    # Root B (smaller): (4 - sqrt(12))/2 = 2 - sqrt(3)
    
    # Express roots in form p/q +/- r/sqrt(d) or similar canonical forms.
    # Here: x = 2 ± sqrt(3). 
    # Let's represent as rational + radical_coefficient * sqrt(radicand)/denom? 
    # Standard simplification: (4 ± 2*sqrt(3))/2 = 2 ± sqrt(3).
    
    # Construct canonical LaTeX for the answer based on target "2a+b" where a and b are roots.
    # Assuming 'a' is root_a, 'b' is root_b with order a>b.
    # Target: 2*root_a + root_b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    result_value = 6 + math.sqrt(3)
    
    # Construct canonical LaTeX string for the answer: "6+\\sqrt{3}" or similar depending on radical format.
    # The prompt asks for rational, radical_coefficient (may be +/-1), radicand, and canonical_latex.
    # We will structure correct_answer as a dict containing these fields plus the numeric value if needed, 
    # but typically 'correct_answer' in such contexts is the string or structured object representing the math result.
    # Based on "Structured comparison... do not rely on string-only equality", we likely need to return the answer 
    # in a specific structure that includes components for checking radical parts.
    
    correct_answer_dict = {
        "value": 6 + math.sqrt(3),
        "rational_part": 6,
        "radical_coefficient": 1,
        "radicand": 3,
        "canonical_latex": r"6+\sqrt{3}"
    }
    
    # Ensure correct_answer is the structured dict as per requirement to include specific fields.
    # If the system expects 'correct_answer' to be just the string for display but also checkable via components:
    # The instruction says "correct_answer must include result with rational, radical_coefficient...". 
    # So we return the dictionary directly or wrap it? Usually in these tasks, correct_answer is the value itself.
    # However, to satisfy "must include...", let's make sure the content matches.
    
    question_text = (
        r"Given the quadratic equation $$(x-2)^2=3$$ with roots ordered such that $$a>b$$, find the value of $$2a+b$$."
    )
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict, 
        # If strict string equality is expected for grading but components are needed for logic:
        # We provide the structured object. The oracle_payload must exactly equal frozen_params.
        "oracle_payload": frozen_params
    }