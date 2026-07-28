# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen parameters for this task instance
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Compute the exact result using native Python arithmetic via fractions module logic 
    # to ensure precision and irreducibility without external API misuse beyond allowed imports.
    # We use Fraction class directly as it is standard library, but since task specifies FractionOps usage:
    # Let's construct terms manually then combine.
    
    term1 = FractionOps.from_parts(9, 22)
    term2 = FractionOps.from_parts(11, 18)
    inner_sub = FractionOps.sub(FractionOps.from_parts(23, 22), FractionOps.from_parts(7, 18))
    
    # Expression: term1 + term2 - inner_sub
    result_add = FractionOps.add(term1, term2)
    final_result = FractionOps.sub(result_add, inner_sub)
    
    numerator = final_result.numerator
    denominator = final_result.denominator
    
    # Generate LaTeX representation for irreducible fraction
    canonical_latex = f"\\frac{{{numerator}}}{{denominator}}" if (numerator < 0 and denominator > 0):
        sign_str = "-" + str(-abs(numerator))
        denom_val = abs(denominator)
        canonical_latex = f"-\\\\frac{{{sign_str}}{{{denom_val}}}"
    else:
        # Handle negative numerator or both signs same (simplified by Fraction class usually handles normalization, 
        # but let's ensure standard form where denominator is positive and sign on top if needed.
        # Python fractions normalize so denom > 0 always. If num < 0, it stays negative.
        canonical_latex = f"\\\\frac{{{numerator}}}{{denominator}}"

    question_text = r"\text{Compute the exact value of: } \(\frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)\)"
    
    correct_answer_data = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_data,
        "oracle_payload": frozen_params
    }