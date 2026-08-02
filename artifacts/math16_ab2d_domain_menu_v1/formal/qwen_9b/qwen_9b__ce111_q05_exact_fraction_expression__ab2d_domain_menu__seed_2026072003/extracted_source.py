from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse frozen_params to get the expression components
    expr_str = kwargs.get("frozen_params", {}).get("expression")
    
    # The task is: 9/22 + 11/18 - (23/22 - 7/18)
    # We will construct this step-by-step using the API
    
    # Term 1: 9/22
    t1 = FractionOps.from_parts(9, 22)
    
    # Term 2: 11/18
    t2 = FractionOps.from_parts(11, 18)
    
    # Inner parenthesis term A: 23/22
    ta = FractionOps.from_parts(23, 22)
    
    # Inner parenthesis term B: 7/18
    tb = FractionOps.from_parts(7, 18)
    
    # Calculate inner parenthesis: (23/22 - 7/18)
    paren_result = FractionOps.sub(ta, tb)
    
    # Full expression: t1 + t2 - paren_result
    step_add = FractionOps.add(t1, t2)
    final_value = FractionOps.sub(step_add, paren_result)
    
    # Prepare the correct_answer according to the contract
    exact_val = FractionOps.to_exact(final_value)  # This ensures irreducible form
    
    numerator = int(exact_val.numerator if hasattr(exact_val, 'numerator') else float(exact_val))
    denominator = int(exact_val.denominator if hasattr(exact_val, 'denominator') else 1.0)
    
    # Handle case where to_exact returns a string like "p/q" or an integer
    if isinstance(final_value, str):
        parts = final_value.split('/')
        numerator = int(parts[0])
        denominator = int(parts[1])
    elif hasattr(final_value, 'numerator'):
        numerator = final_value.numerator
        denominator = final_value.denominator
    
    # Generate canonical LaTeX. 
    # If it's an integer (denom 1), usually just the number or \frac{n}{1}. 
    # The API to_latex handles this. We pass the Fraction object if possible, else parse string.
    
    latex_val = ""
    if isinstance(final_value, str):
        # It is already a canonical fraction string "p/q" or integer
        # If it's an int representation (e.g., just number), we might need to format as \frac{n}{1} 
        # but usually math problems expect p/q. Let's assume standard Fraction object behavior first.
        if '/' in final_value:
            latex_val = f"\\frac{{{final_value.split('/')[0]}}}{{{final_value.split('/')[1]}}}"
        else:
             latex_val = str(final_value) # Fallback, though unlikely for this domain task unless integer result
    elif hasattr(final_value, 'numerator'):
         latex_str = FractionOps.to_latex(final_value, mixed=False)
         if latex_str.startswith("\\frac"):
            latex_val = latex_str
         else:
             # If it returns just a number string (e.g. "2"), wrap in fraction? 
             # The prompt says "irreducible fraction". Integers are fractions with denom 1.
             # to_latex usually outputs \frac{n}{d} for non-ints and n for ints or similar.
             # Let's rely on the API output directly if it matches schema, otherwise construct manually.
             latex_val = f"\\frac{{{final_value.numerator}}}{{{final_value.denominator}}}"

    return {
        "question_text": expr_str.replace("/", "\\/").replace("+", "\\ + ").replace("-", "- \\left(").replace(")", "\\right)"), 
        # Actually, the instruction says: use as question_text. The frozen_params has a string expression.
        # I should output the raw LaTeX representation of that string for display? Or just the text provided?
        # "use as question_text" implies using the description or formatted version.
        # Let's format it nicely with LaTeX delimiters if possible, but simple is safer based on API constraints.
        # Re-reading: "question_text: the provided stem string (do not rebuild from scratch unless required)."
        # The frozen_params has a raw mathjax-like string or plain text? 
        # It says: expression: "9/22 + 11/18 - (23/22 - 7/18)" in the example block.
        # But the task description had LaTeX blocks. I will use the formatted version from frozen_params if available, 
        # but here only raw string is given in kwargs simulation. Let's assume we need to render it nicely or just return the input string processed?
        # The prompt says "use as question_text". I'll construct a clean text representation or LaTeX.
        # Given the domain API doesn't have a renderer for arbitrary strings, and `to_latex` works on Fractions.
        # Let's create the latex version of the expression manually to be safe? 
        # Or just return the string from frozen_params if it was meant to be raw text.
        # The task description had: \[ ... \]. I will construct a clean LaTeX question_text.
        
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": latex_val
        },
        "oracle_payload": kwargs.get("frozen_params", {})
    }