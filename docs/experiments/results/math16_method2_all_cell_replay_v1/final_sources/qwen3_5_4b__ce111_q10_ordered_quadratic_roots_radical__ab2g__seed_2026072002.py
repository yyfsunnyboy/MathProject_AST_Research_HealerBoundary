def generate(level=1, **kwargs):
    import re
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "equation": "(x-2)^2=3", 
        "order": "a>b", 
        "target": "2a+b"
    }
    
    # Parse the equation to extract coefficients for ax^2 + bx + c = 0 form
    # Equation: (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    # a=1, b=-4, c=1
    
    equation_str = frozen_params["equation"]
    
    # Construct the question text using formal LaTeX delimiters
    question_text = r"\text{Solve for } x \text{ in the quadratic equation: " + r"$(x-2)^2=3$".replace("$", "\\$") + r"."
    
    # Calculate roots manually to ensure correctness and handle signs properly
    # Equation: x^2 - 4x + 1 = 0
    a, b_val, c = 1, -4, 1
    
    discriminant = b_val**2 - 4*a*c # (-4)^2 - 4*1*1 = 16 - 4 = 12
    sqrt_discriminant = int(discriminant ** 0.5) # sqrt(12) is not integer, but we need exact form
    
    # Since discriminant (12) is positive and a perfect square? No, 12 is not a perfect square.
    # Wait, the task says "radical_coefficient". Usually implies surds like sqrt(k).
    # Let's re-evaluate: x = [4 +/- sqrt(16-4)] / 2 = [4 +/- sqrt(12)]/2 = [4 +/- 2*sqrt(3)]/2 = 2 +/- sqrt(3)
    
    # Roots are 2 + sqrt(3) and 2 - sqrt(3).
    # The problem asks for "ordered quadratic roots radical" with order a > b.
    # Here, root1 = 2 + sqrt(3), root2 = 2 - sqrt(3).
    # Since sqrt(3) is positive (~1.732), 2+sqrt(3) > 2-sqrt(3).
    
    # Format the roots in terms of rational part, radical coefficient (usually +/-1 for simplest form), and radicand.
    # Root 1: Rational=2, Coeff=1, Radicand=3 -> "2 + \sqrt{3}"
    # Root 2: Rational=2, Coeff=-1, Radicand=3 -> "2 - \sqrt{3}" (or coeff is negative)
    
    rational_part = 2
    
    # We need to format the answer as a list of strings or similar structure that includes these components.
    # The spec says: correct_answer must include result with rational, radical_coefficient, radicand, and canonical_latex.
    # Let's construct the latex string for each root.
    
    # Root 1 (larger): 2 + sqrt(3) -> coeff is positive (+1 implicitly or explicit), let's use explicit signs if needed by format
    # Standard form often writes a +/- b*sqrt(c). 
    # Here: x = \frac{4 \pm \sqrt{12}}{2} = 2 \pm \sqrt{3}.
    
    latex_root_1 = r"2 + \sqrt{3}"
    latex_root_2 = r"2 - \sqrt{3}"
    
    # Construct the full correct answer string containing both roots in ordered form (a > b)
    correct_answer_str = f"{latex_root_1} \\text{ and } {latex_root_2}"
    
    # Structure for internal verification: 
    # We need to ensure we can parse this back or verify components.
    # Let's define a helper structure if needed, but the return value is just strings/dicts as per "dict with exactly...".
    # The spec says correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand, and canonical_latex.
    
    root_data_1 = {
        "rational": 2, 
        "radical_coefficient": 1, 
        "radicand": 3, 
        "canonical_latex": r"\\sqrt{3}" # Or the whole term? Usually just the radical part or the full expression. Given context of roots, likely full term representation is safer in latex string.
    }
    
    root_data_2 = {
        "rational": 2, 
        "radical_coefficient": -1, 
        "radicand": 3, 
        "canonical_latex": r"-\\sqrt{3}" # Or just the term subtracted? Let's assume full expression components.
    }
    
    # Re-reading spec: correct_answer must include result with rational, radical_coefficient... and canonical_latex.
    # It implies a structured object or string that represents these clearly. 
    # Given "Structured comparison is required", returning a list of dicts might be better than just one latex string if the grader checks components.
    # However, usually correct_answer in such tasks is the final answer text (e.g., LaTeX). 
    # But to satisfy "include result with...", we can embed metadata or return a structured object representing the solution set.
    # Let's assume the expected output format for 'correct_answer' is a list of dictionaries describing each root, OR a single string that contains these elements clearly labeled if it's text-based. 
    # Given "canonical_latex" is requested as part of the components, returning a structured object per root seems most robust for programmatic checking without relying on regex magic in the grader unless specified otherwise.
    # But often 'correct_answer' expects the final string representation used in LaTeX rendering.
    # Let's look at "oracle_payload must exactly equal". That is fixed strings/dicts.
    
    # To be safe and strictly follow "include result with...", I will return a list of dictionaries where each dict has the required fields, alongside or instead of just text? 
    # Actually, standard practice for these specific generated tasks often expects:
    # correct_answer = [ { ... }, { ... } ] OR a string like "2 + \\sqrt{3}, 2 - \\sqrt{3}".
    # Let's provide the structured data as it allows verifying rational/coeff/radicand explicitly.
    
    solution_set = []
    
    # Root 1: 2 + sqrt(3)
    sol_1 = {
        "rational": 2, 
        "radical_coefficient": 1, 
        "radicand": 3, 
        "canonical_latex": r"\\sqrt{3}" if we consider the variable part or full term? 
        # Let's assume canonical_latex refers to the radical expression itself: \\pm\\sqrt{k}
    }
    
    # Actually, looking at similar tasks, 'correct_answer' is often a string. 
    # But "include result with rational..." suggests properties of that answer.
    # I will return a list of dictionaries for clarity and structural comparison capability.
    
    solution_set.append({
        "rational": 2, 
        "radical_coefficient": 1, 
        "radicand": 3, 
        "canonical_latex": r"\\sqrt{3}" # The radical part added to rational? Or the whole term? Let's assume the variable component.
    })
    
    solution_set.append({
        "rational": 2, 
        "radical_coefficient": -1, 
        "radicand": 3, 
        "canonical_latex": r"-\\sqrt{3}" # The radical part subtracted? Or the whole term.
    })
    
    # Wait, if I return a list of dicts, does it satisfy "correct_answer must include result with ... canonical_latex"? Yes.
    # But maybe 'correct_answer' should be the LaTeX string itself and the fields are just for my internal logic or part of the dict? 
    # The spec says: correct_answer MUST include... AND oracle_payload is separate.
    
    # Let's try to make it a single structured object representing the set, or simply ensure the text contains these clearly if it must be string.
    # Given "Structured comparison", returning a list of dicts is safer than parsing LaTeX strings which vary by renderer.
    
    correct_answer = solution_set
    
    oracle_payload = frozen_params.copy()
    
    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": oracle_payload
    }