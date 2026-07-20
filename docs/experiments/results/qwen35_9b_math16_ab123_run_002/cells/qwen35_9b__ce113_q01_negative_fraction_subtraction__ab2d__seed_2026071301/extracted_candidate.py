def generate(level=1, **kwargs):
    # Frozen sampled parameters must be preserved exactly in oracle_payload
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Extract expression from kwargs if provided to override or use default logic based on task spec
    expr_str = kwargs.get("expression", frozen_params["expression"])
    
    # 1. Parse operands using Domain API: FractionOps.create
    try:
        op_a_tuple, _ = FractionOps.create(expr_str.split()[0]) 
        op_b_tuple, _ = FractionOps.create("-".join([x for x in expr_str.replace(" - ", " ").split() if x.startswith('-') or '/' in x])) # Simplified parsing logic for robustness
        
        # Robust re-parse using split logic specific to the example string
        parts = [p.strip() for p in expr_str.split()]
        term1, op_sym, term2 = None, " - ", None
        if len(parts) == 3:
            term1 = parts[0]
            # Handle negative second fraction like "-(-1/4)" or just "-1/4" depending on spacing in original string logic. 
            # The example is "3/7 - (-1/4)". Splitting by space gives ['3/7', '-', '(-1/4)'].
            if op_sym == '-':
                term2 = parts[2].strip('()') # Remove parentheses for FractionOps.create
                
        else:
             # Fallback parsing if spacing varies slightly, though spec implies fixed format usually.
             # For this specific task "3/7 - (-1/4)", strict splitting handles it.
             pass

        term_a = op_a_tuple
        term_b_str = parts[2].strip('()') 
        term_b = FractionOps.create(term_b_str) if len(parts)==3 else None
        
        # Re-evaluating parsing for "3/7 - (-1/4)" specifically:
        # It parses as Term A (3/7), Operator (-), Term B ((-1/4)) -> strip parens -> -1/4.
        
    except Exception:
        return {"error": "Parse failed"}

    # 2. Perform Subtraction using Domain API: FractionOps.sub
    try:
        result_tuple, _ = FractionOps.sub(term_a, term_b)
    except ValueError as e:
         return {"error": str(e)}

    # 3. Generate Latex using Domain API: FractionOps.to_latex
    latex_result_str = FractionOps.to_latex(result_tuple)
    
    # Construct the question_text with formal LaTeX delimiters
    term_a_parsed, _ = expr_str.split()[0].split('/') if '/' in expr_str else (1, 1) 
    # Reconstructing clean text for display: "3/7 - (-1/4)" is already a string. We need to format it nicely or keep as LaTeX math mode?
    # Spec says question_text must use formal LaTeX delimiters. Let's assume the expression variable contains raw fractions which we wrap in $...$ 
    # Or better, convert the parsed parts back into clean latex for display if needed, but usually keeping the input string inside $$ is safe unless strictly formatted numbers are required.
    # Given "3/7", it renders as 3/7 textually. Let's assume standard mathjax rendering where \frac{a}{b} is preferred or just a/b depending on context. 
    # However, to be precise with LaTeX delimiters: $ ... $
    
    question_text = f"Calculate the result of {expr_str.replace('/', '\\\\frac{{}}'.replace(' - ', ' - ').replace('(','').replace(')','')}." 
    
    # Correction for better looking latex in text if needed, but sticking to raw expression inside $$ is standard unless specified otherwise.
    # Let's assume we just wrap the provided expression string which might contain plain numbers or simple fractions. 
    # If it contains "3/7", LaTeX renders 3 over 7? No, usually \frac{3}{7}. The prompt asks for canonical_latex in correct_answer separately.
    # For question_text: let's just format the specific expression given into a nice latex string if possible or keep as is within delimiters. 
    # Safest bet for "question_text": wrap the input expression string inside $ signs, ensuring it looks like math mode.
    
    final_question = f"${expr_str}$"

    correct_answer_dict = {
        "numerator": result_tuple[0],
        "denominator": result_tuple[1],
        "canonical_latex": latex_result_str # This is the irreducible fraction in LaTeX format (e.g., \frac{13}{28})
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": final_question,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }