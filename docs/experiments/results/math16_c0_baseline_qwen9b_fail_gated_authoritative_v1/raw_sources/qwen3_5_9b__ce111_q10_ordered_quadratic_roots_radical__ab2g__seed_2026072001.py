def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Parse the equation to extract roots and coefficients for (ax + b)^2 = c form logic
    # Equation: (x - 2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    # Roots of x^2 - 4x + 1 = 0 are [2 +/- sqrt(3)]
    # Let roots be r1, r2. Sum S = r1+r2 = 4, Product P = r1*r2 = 1.
    # The problem asks for ordered quadratic roots radical form where a > b implies we map the standard root representation to (a + sqrt(b)) or similar? 
    # Re-reading typical "ordered_quadratic_roots_radical" tasks: usually they define roots as x = p +/- q*sqrt(r).
    # Here roots are 2 + sqrt(3) and 2 - sqrt(3).
    # Standard form often used in these datasets for (x-h)^2=k is h +/- sqrt(k).
    # So root1 = 2, coeff=1, radicand=3. Root2 = 2, coeff=-1? No, usually it's expressed as a + b*sqrt(c) where b can be negative or handled by order.
    # However, the target is "2a+b". This suggests roots are represented as (a +/- sqrt(b))? Or maybe coefficients of x in expanded form?
    # Let's assume the standard representation for these specific generated math tasks:
    # Roots are derived from solving ax^2+bx+c=0. Here 1x^2 -4x +1 =0.
    # Discriminant D = b^2-4ac = 16-4 = 12. sqrt(D) = 2*sqrt(3).
    # Roots: (4 +/- 2*sqrt(3)) / 2 = 2 +/- sqrt(3).
    # Representation usually expected: 
    # Root A: a + b*sqrt(c) -> 2 + 1*sqrt(3) ? Or just the value?
    # The prompt asks for "radical_coefficient", "radicand". This implies form: rational_part + radical_coefficient * sqrt(radicand).
    # For root > : 2 + 1*sqrt(3). a=2, b=1 (coeff), c=3.
    # But wait, the target is "2a+b". If roots are r1, r2. 
    # Let's look at the specific constraint: order="a>b". This likely refers to the variable names in the answer string or the values of coefficients?
    # Actually, looking at similar tasks (ce111_q10...), "order" often dictates how roots are labeled if they were variables a and b. 
    # But here we return specific fields: rational, radical_coefficient, radicand, canonical_latex.
    # Let's assume the root is represented as `rational + radical_coefficient * sqrt(radicand)`.
    # Root 1 (larger): 2 + 1*sqrt(3). Rational=2, Coeff=1, Radicand=3.
    # Root 2 (smaller): 2 - 1*sqrt(3). Rational=2, Coeff=-1, Radicand=3? Or is the minus handled in latex?
    # Usually canonical_latex handles signs inside sqrt or outside. 
    # If radicand must be square-free integer: 3 is fine.
    
    # Let's construct the data for the larger root (since order might imply sorting, but target "2a+b" suggests a specific combination).
    # Actually, often these tasks define two roots r1 and r2. 
    # If the task implies finding coefficients such that x = rational + radical_coefficient * sqrt(radicand), then:
    # Larger root: 2 + sqrt(3) -> rational=2, coef=1, radicand=3.
    # Smaller root: 2 - sqrt(3). How is this represented? 
    # Option A: rational=2, coef=-1, radicand=3.
    # Option B: The task might only ask for the positive radical form and handle order via text?
    # Given "order": "a>b", it implies we have two entities a and b (the roots?). 
    # But the return dict has single fields `rational`, etc. This suggests returning info about ONE root or the pair in a specific way?
    # Re-reading: "correct_answer must include result with rational, radical_coefficient...". Singular.
    # Maybe it returns the larger one? Or maybe the structure is different.
    # Let's assume we return the properties of the roots that satisfy the equation. 
    # If the system expects a single object for the answer, perhaps it combines them or picks the primary one (larger).
    # However, "2a+b" target suggests an algebraic expression involving coefficients 'a' and 'b'.
    # Hypothesis: The roots are defined as x = u +/- v*sqrt(w). 
    # Maybe `rational` is u. `radical_coefficient` is v? `radicand` is w?
    # If so, for 2 + sqrt(3): rational=2, coef=1, radicand=3.
    # For 2 - sqrt(3): rational=2, coef=-1 (or handled as subtraction in latex), radicand=3.
    # But the return dict has singular keys. 
    # Let's assume the task wants the representation of the roots where we list them or just the parameters for the positive radical part?
    # Wait, "correct_answer" usually contains the final string to display.
    # If I must output a single rational/coef/radicand set, maybe it refers to the form `a + b*sqrt(c)` and returns that tuple-like info?
    # Let's assume we return the data for the larger root (standard convention) or perhaps the question implies finding 'a' and 'b' in x = a +/- sqrt(b)? No, "radical_coefficient" exists.
    
    # Alternative interpretation: The roots are `r1` and `r2`. 
    # Maybe `correct_answer` is a string like "(2+sqrt(3)), (2-sqrt(3))".
    # But the spec says: "must include result with rational, radical_coefficient...". This sounds like an object structure inside correct_answer? Or keys in correct_answer dict?
    # Spec: "correct_answer must include result with ... canonical_latex". 
    # It does not say `correct_answer` is a string. But usually it's the answer text.
    # Let's assume `correct_answer` is a dictionary containing these fields for clarity, or maybe just the latex?
    # Re-reading: "return a dict with exactly question_text, correct_answer, and oracle_payload".
    # If `correct_answer` must include those specific keys (rational, etc), then `correct_answer` itself might be an object/dict. 
    # OR, maybe `correct_answer` is the latex string, but the spec says "must include result with...". This implies nested structure?
    # Let's assume `correct_answer` is a dict containing: {rational, radical_coefficient, radicand, canonical_latex}.
    
    # Calculation for (x-2)^2 = 3 -> x^2 - 4x + 1 = 0.
    # Roots: 2 +/- sqrt(3).
    # Rational part: 2. Radical coefficient magnitude: 1. Radicand: 3.
    # Since order is "a>b", maybe we define a and b as the roots? 
    # But target is "2a+b". If a = larger root, b = smaller root.
    # Target value calculation (for oracle check or internal logic): Not needed for output generation unless `correct_answer` needs to be numeric.
    # The prompt asks for `canonical_latex`.
    
    # Let's construct the canonical latex for the roots. 
    # Usually: "2 + \sqrt{3}, 2 - \sqrt{3}" or similar.
    # But if we must provide rational, coef, radicand fields in correct_answer dict:
    
    root_rational = 2
    radical_coefficient_mag = 1
    radicand = 3
    
    # Handling the sign for canonical latex usually puts it inside sqrt as +/-? 
    # Or "radical_coefficient" handles the sign. If coef is -1, latex might be "-\sqrt{3}".
    # Let's assume we return info for the positive case primarily or both if possible in a list? 
    # Given singular keys, I will provide data for the larger root (positive radical term) as 'a' and smaller as implied context?
    # Actually, looking at "target": "2a+b", this implies variables. 
    # Maybe `correct_answer` should be the latex string of the expression 2a+b evaluated? No, that's overthinking.
    # Most likely: The task is to identify the parameters a,b,c in x = rational + radical_coefficient * sqrt(radicand).
    # Since there are two roots, and order="a>b", maybe we return the set for 'a' (larger) and assume 'b' logic? 
    # But `correct_answer` fields are singular. I will provide the parameters for the larger root (2 + 1*sqrt(3)).
    
    canonical_latex = "2+\\sqrt{3}" 
    
    # Wait, if order is a>b, maybe we need to represent both? 
    # If correct_answer must be a dict with those keys, I'll put the values for the larger root.
    # However, often these tasks expect the full solution set in latex.
    # Let's try to make `correct_answer` an object containing the breakdown of the roots if possible, or just the main one.
    # Given "Structured comparison is required", having a dict with specific keys allows checking types/values easily.
    
    answer_dict = {
        "rational": root_rational,
        "radical_coefficient": radical_coefficient_mag, 
        "radicand": radicand,
        "canonical_latex": f"{root_rational}+\\sqrt{{{radicand}}}" # Simplified for now. If we need both, maybe comma separated?
    }
    
    # Refining canonical_latex to include the negative root if required by context of "roots" (plural). 
    # But fields are singular. I will stick to the positive radical form as representative or combine in latex string but keep scalar fields for the primary component 'a'.
    # Let's assume the question asks for the roots, and we represent them generally. 
    # If I must choose one set of scalars, it's usually the coefficients common to both (rational=2, radicand=3) and coef magnitude 1?
    # But `radical_coefficient` can be negative. 
    # Let's assume the task wants the form for the larger root 'a'.
    
    question_text = r"Given the equation $(x-2)^2=3$, find the ordered quadratic roots in radical form where $a > b$. Express each root as a rational number plus or minus an integer coefficient times the square root of a positive non-square radicand. Let the larger root be represented by parameters corresponding to 'a' and the smaller by 'b'. Determine the values for the representation of the larger root."
    
    # Actually, simpler question text based on standard format:
    question_text = r"Solve $(x-2)^2=3$ for $x$. Express roots in form $\text{rational} \pm \text{radical\_coefficient}\sqrt{\text{radicand}}$. Order such that root corresponding to '+' is 'a' and '-' is 'b'. Return parameters for the larger root."
    
    # Let's make it concise and formal.
    question_text = r"Solve $(x-2)^2=3$ for $x$. Express roots in radical form with integer coefficients where radicand is square-free. Order roots such that $a > b$. Provide the parameters (rational, radical\_coefficient, radicand) and canonical LaTeX representation."
    
    # Wait, if I return only one root's params, does it match "roots" plural? 
    # Maybe `correct_answer` should contain a list or just the latex string for both?
    # Spec: "must include result with rational...". This implies these fields exist. If there are two roots, maybe we average? No.
    # Likely, the task expects the parameters of the form $a + b\sqrt{c}$ where 'b' is positive (magnitude) and sign handled in latex? 
    # Or `radical_coefficient` takes negative value for smaller root? But fields are singular.
    # I will assume we return the properties common to both or specifically for the larger one as per "order a>b" implying focus on 'a'.
    
    final_canonical_latex = r"2+\sqrt{3}" 
    # If needed, could be "2\pm\sqrt{3}". But fields suggest specific coef. I'll use +1 for magnitude and handle sign in latex if necessary? 
    # Let's assume `radical_coefficient` is the integer multiplier (can be negative).
    # For larger root: 2 + 1*sqrt(3). Coef = 1.
    
    return {
        "question_text": question_text,
        "correct_answer": answer_dict, 
        "oracle_payload": frozen_params
    }