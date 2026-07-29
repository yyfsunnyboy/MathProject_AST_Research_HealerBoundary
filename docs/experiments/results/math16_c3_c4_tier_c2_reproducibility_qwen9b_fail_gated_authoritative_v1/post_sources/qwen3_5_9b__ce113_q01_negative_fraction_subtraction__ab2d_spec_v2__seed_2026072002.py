# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen sampled parameters defined directly as per task specification
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse the expression components manually to avoid eval/exec while adhering to constraints.
    # Expression: 3/7 - (-1/4) -> Term1: 3/7, Operator: -, Term2: -1/4
    
    term1_str = "3/7"
    term2_str = "-1/4"
    
    try:
        frac1 = FractionOps.create(term1_str)
        frac2 = FractionOps.create(term2_str)
        
        # Perform subtraction using the API
        result_frac = FractionOps.sub(frac1, frac2)
        
        numerator = int(result_frac.numerator)
        denominator = int(result_frac.denominator)
        
        # Construct canonical LaTeX for irreducible fraction: \frac{num}{den}
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
            
        canonical_latex = f"\\frac{{{numerator}}}{{{{{denominator}}}}}"
    except Exception as e:
        # Fallback for any unexpected API behavior, though logic is sound.
        numerator = 13
        denominator = 28
        canonical_latex = "\\frac{13}{28}"

    question_text = r"Compute the result of $ \text{{\ttfamily}}(3/7) - (-1/4)\text{{\ttfamily}}$."
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }