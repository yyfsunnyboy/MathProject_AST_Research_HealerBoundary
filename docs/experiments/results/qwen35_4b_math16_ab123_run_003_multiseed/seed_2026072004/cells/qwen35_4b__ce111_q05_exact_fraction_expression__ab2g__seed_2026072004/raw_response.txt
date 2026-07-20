def generate(level=1, **kwargs):
    import sympy
    
    expression_str = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Parse and simplify the expression using SymPy for exact arithmetic
    expr = sympy.sympify(expression_str)
    result = expr.simplify()
    
    # Extract numerator and denominator from the resulting Fraction or Rational object
    if hasattr(result, 'numerator'):
        num = int(result.numerator)
        den = int(result.denominator)
    else:
        raise ValueError("Result is not a rational number")
        
    canonical_latex = f"{result}"
    
    # Construct the question text using formal LaTeX delimiters for arithmetic operations
    question_text = r"\text{Simplify the expression } \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)"
    
    # Ensure canonical_latex is in standard LaTeX fraction format for irreducible fractions if it's a simple rational, otherwise use the evaluated form
    # SymPy's str() usually gives something like '4/9', we want to ensure it looks like math mode or just plain text representation of the number. 
    # The requirement asks for canonical_latex for an irreducible fraction. Let's format it nicely.
    
    if den == 1:
        formatted_str = f"{num}"
    else:
        formatted_str = f"\\frac{{{num}}}{{{den}}}"
        
    correct_answer_dict = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": formatted_str if den != 1 else str(num) + "\\quad (integer)" # Providing a safe latex representation or just the number logic. 
        # Actually standard practice for 'exact_fraction_expression' usually implies showing it as \frac{num}{den}. If integer, often accepted as is.
        # Let's stick to generating valid LaTeX that renders correctly.
    }
    
    if den == 1:
        correct_answer_dict["canonical_latex"] = f"{num}" 
    else:
        correct_answer_dict["canonical_latex"] = r"\frac{" + str(num) + "}{"} + str(den) + r"\""

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": kwargs if 'expression' not in locals() else {"expression": expression_str} # The frozen parameter is provided directly or via args. 
        # Re-reading spec: oracle_payload must exactly equal the frozen sampled parameters.
    }

# Correction to ensure strict adherence to frozen params and return structure based on task description logic without external input variability beyond what was fixed in the prompt context.
def generate(level=1, **kwargs):
    import sympy
    
    # Frozen parameter as per specification: {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    expression_str = frozen_params["expression"]
    
    # Parse and simplify the expression using SymPy for exact arithmetic
    expr = sympy.sympify(expression_str)
    result = expr.simplify()
    
    if hasattr(result, 'numerator'):
        num = int(result.numerator)
        den = int(result.denominator)
        
        canonical_latex_parts = [str(num), str(den)]
        canonical_latex = r"\frac{" + "".join(canonical_latex_parts) + r"\"" if den != 1 else f"{num}"
    else:
        raise ValueError("Result is not a rational number")
    
    question_text = r"\text{Simplify the expression } \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)"
    
    correct_answer_dict = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": canonical_latex if den != 1 else f"{num}" # Keeping it as a fraction representation is safer for the task type unless integer handling is specified otherwise. 
        # However, standard LaTeX rendering of an integer like '4/9' vs '4'. Let's use \frac always for consistency with "exact_fraction_expression".
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params # Must exactly equal the frozen sampled parameters. Note: The prompt says 'frozen' implies it's constant here. 
                                    # But if generate is called with extra kwargs, should oracle reflect only the specific freeze or all passed?
                                    # Spec: "oracle_payload must exactly equal the frozen sampled parameters". This usually means a hardcoded dict provided in the task context.
    }

# Final verification of logic based on strict constraints