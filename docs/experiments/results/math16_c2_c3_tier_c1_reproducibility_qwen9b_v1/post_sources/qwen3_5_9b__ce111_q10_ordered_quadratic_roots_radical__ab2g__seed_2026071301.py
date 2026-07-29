def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Parse the equation to extract roots and coefficients for validation logic
    # Equation: (x - 2)^2 = 3 => x^2 - 4x + 1 = 0
    # Roots are 2 +/- sqrt(3)
    # Let a be the larger root, b be the smaller root.
    
    def canonical_latex(val):
        """Formats a value into canonical LaTeX string."""
        if isinstance(val, int):
            return f"{val}"
        elif isinstance(val, float):
            s = str(val)
            # Check for integer representation of floats (e.g., 2.0 -> 2)
            try:
                i_val = int(float(s))
                if abs(i_val - val) < 1e-9:
                    return f"{i_val}"
            except ValueError:
                pass
            
            # Check for simple radicals like sqrt(3), sqrt(5), etc.
            # We expect forms like "sqrt(n)" or "-sqrt(n)"
            
            if isinstance(val, float):
                 s = str(val)
                 
            return f"{val}"

    def parse_roots_from_equation(eq_str):
        """Simulates parsing the specific equation provided in frozen_params."""
        # Hardcoded logic for the specific frozen sample to ensure correctness without external math parsers
        if eq_str == "(x-2)^2=3":
            center = 2.0
            diff_sq_val = 3.0
            sqrt_diff = math.sqrt(diff_sq_val)
            
            root_a = center + sqrt_diff # Larger root (since sqrt(3) > 0)
            root_b = center - sqrt_diff # Smaller root
            
            return {
                "a": root_a,
                "b": root_b,
                "sqrt_term": math.sqrt(diff_sq_val),
                "radicand": diff_sq_val
            }
        else:
            raise ValueError("Equation not supported in this specific generation context.")

    def compute_target(a, b):
        """Computes 2a + b."""
        return 2 * a + b

    # Execute logic based on frozen parameters
    parsed = parse_roots_from_equation(frozen_params["equation"])
    
    # Calculate target value
    raw_target_val = compute_target(parsed["a"], parsed["b"])
    
    # Construct the radical coefficient and radicand for canonical representation
    sqrt_term = parsed["sqrt_term"]
    radicand = int(round(sqrt_term ** 2)) if sqrt_term != math.sqrt(radicand) else radicand
    
    # Determine sign of the radical part in the final answer expression? 
    # Actually, the target is a linear combination. We need to express it canonically.
    # Target: 2a + b = 2(2+sqrt3) + (2-sqrt3) = 4 + 2sqrt3 + 2 - sqrt3 = 6 + sqrt3
    
    # Re-evaluate based on the specific result structure required:
    # Result should be rational part + radical_coefficient * sqrt(radicand)
    
    a_val = parsed["a"]
    b_val = parsed["b"]
    
    total_rational_part = (2.0 * 2.0) + 2.0 - math.sqrt(3.0) # Wait, let's re-calculate algebraically
    
    # Algebraic expansion:
    # a = c + d, where c=2, d=sqrt(3)
    # b = c - d
    # Target = 2a + b = 2(c+d) + (c-d) = 2c + 2d + c - d = 3c + d
    # Result = 3*2 + sqrt(3) = 6 + 1*sqrt(3)
    
    rational_part = 6.0
    radical_coefficient = 1
    
    if abs(radical_coefficient) == 1:
        canonical_radical_str = f"\\sqrt{{{radicand}}}"
    else:
        # If coefficient is not +/- 1, we usually write k*sqrt(n). 
        # But the spec says radical_coefficient may be +1 or -1. 
        # Let's assume for this specific task it simplifies to coeff=1.
        canonical_radical_str = f"{radical_coefficient}*\\sqrt{{{radicand}}}"

    if rational_part == 0:
        final_latex_expr = canonical_radical_str
    elif radical_coefficient == 0: # Should not happen here but for safety
        final_latex_expr = str(int(rational_part))
    else:
        final_latex_expr = f"{int(round(rational_part))} {canonical_radical_str}"

    correct_answer_obj = {
        "result": float(raw_target_val), # The raw computed value 6 + sqrt(3) approx 7.732...
        "rational": int(round(rational_part)),
        "radical_coefficient": radical_coefficient,
        "radicand": radicand,
        "canonical_latex": final_latex_expr
    }

    question_text = (
        f"Solve the equation {frozen_params['equation']} for x. \n"
        f"If the roots are ordered such that $a > b$, compute the value of ${frozen_params['target']}$.\n\n"
        f"The answer should be expressed in the form $r \\pm k\\sqrt{n}$ where possible, or simplified."
    )

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_obj,
        "oracle_payload": frozen_params
    }