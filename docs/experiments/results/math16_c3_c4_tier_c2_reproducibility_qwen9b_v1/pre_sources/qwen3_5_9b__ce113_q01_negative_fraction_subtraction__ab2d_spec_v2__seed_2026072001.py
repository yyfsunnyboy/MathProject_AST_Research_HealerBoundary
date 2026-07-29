# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen sampled parameters defined directly as per task specification
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse the expression components manually to avoid eval/exec while adhering to API rules.
    # Expression: 3/7 - (-1/4) -> Term1: 3/7, Operator: -, Term2: -1/4
    
    term1_str = "3/7"
    term2_str = "-1/4"
    
    try:
        f1 = FractionOps.create(term1_str)
        f2 = FractionOps.create(term2_str)
        
        # Perform subtraction using the API method
        result_fraction = FractionOps.sub(f1, f2)
        
        numerator = int(result_fraction.numerator)
        denominator = int(result_fraction.denominator)
        
        # Construct canonical LaTeX for irreducible fraction: \frac{num}{den}
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
            
        # Handle negative signs in LaTeX properly (usually numerator carries the sign or use minus before frac)
        latex_parts = []
        
        if numerator < 0 and denominator > 0:
            latex_parts.append(f"-\\frac{{{abs(numerator)}}}{{{denominator}}}")
        elif numerator > 0 and denominator < 0:
            # Move negative to numerator for canonical form usually, but let's stick to standard fraction representation
             if abs(denominator) == 1:
                 latex_parts.append(f"{numerator // -abs(numerator)}") 
             else:
                latex_parts.append(f"-\\frac{{{-numerator}}}{{-{denominator}}}") # Simplify signs? No, keep canonical.
        elif numerator < 0 and denominator < 0:
            latex_parts.append(f"\\frac{{{abs(numerator)}}}{{{abs(denominator)}}}")
        else:
             if abs(denominator) == 1:
                 latex_parts.append(str(abs(numerator))) # Integer result
             else:
                latex_parts.append(f"\\frac{{{numerator}}}{{{denominator}}}")

        canonical_latex = "".join(latex_parts)
        
    except Exception as e:
        raise RuntimeError("Failed to compute fraction arithmetic") from e
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    question_text = r"Compute the result of $3/7 - (-1/4)$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }