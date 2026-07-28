def generate(level=1, **kwargs):
    import re
    
    # Frozen sampled parameters as per task specification
    frozen_params = {
        "equation": "(x-2)^2=3", 
        "order": "a>b", 
        "target": "2a+b"
    }
    
    oracle_payload = str(frozen_params)
    
    # Parse the equation to extract coefficients for a quadratic form ax^2 + bx + c = 0
    # Equation: (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    # Here, a=1, b=-4, c=1
    
    equation_str = frozen_params["equation"]
    
    # Construct the question text with formal LaTeX delimiters
    latex_equation = r"\left(x-2\right)^{2}=3"
    question_text = f"Solve for $x$ in the following quadratic equation:\n\n$$ {latex_equation} $$"
    
    # Solve (x-2)^2 = 3
    # x - 2 = ±√3
    # x = 2 ± √3
    
    # Identify components based on standard form ax^2 + bx + c = 0 where a=1, b=-4, c=1
    # Roots are (b ± sqrt(b^2-4ac)) / 2a
    # Discriminant D = (-4)^2 - 4(1)(1) = 16 - 4 = 12
    # √D = √12 = √(4*3) = 2√3
    
    # Roots: ( -4 ± 2√3 ) / 2 = -2 ± √3
    
    # The problem asks for "ordered quadratic roots radical" with order a>b.
    # Usually, this implies ordering the real parts or specific coefficients if it's an identity check.
    # However, looking at the target "2a+b": 
    # If we assume standard form ax^2+bx+c=0 derived from (x-2)^2=3 -> x^2 -4x +1 = 0.
    # a = 1, b = -4.
    # Target value: 2(1) + (-4) = -2.
    
    # Let's verify the roots structure required in correct_answer.
    # Roots are r1 = -2 + √3 and r2 = -2 - √3.
    # The prompt asks for "radical_coefficient (may be +1 or -1), radicand".
    # In x^2-4x+1=0, the discriminant part is 12. 
    # But often these tasks refer to the simplified radical form of the roots themselves if they are irrational.
    # Root: -2 ± √3. Here coefficient is +1 (for positive) or -1? Usually magnitude matters in canonical forms unless sign is explicit.
    # Let's assume the question asks for the representation of one root or the discriminant radical part.
    # Given "ordered", let's look at the roots: (-2+√3, -2-√3). 
    # If we order them numerically: -2-√3 < -2+√3 (since √3 > 0). So r1 = -2-√3, r2 = -2+√3.
    
    # Re-evaluating based on "radical_coefficient": 
    # If the answer expects the radical part of a root: ±√3. Coefficient is +1 or -1 depending on sign? 
    # Or perhaps it refers to √D / 2a = (±2√3)/2 = ±√3.
    
    # Let's construct the canonical latex for one of the roots, say the positive radical part if applicable, 
    # but usually "roots" implies both or a set. However, the output format suggests specific fields: rational, radical_coefficient, radicand.
    # This structure fits √k = c * √n where n is square-free. Here 3 is square free. Coefficient can be ±1? 
    # Let's assume the question asks for the simplified form of the irrational part or a specific root representation.
    # Given "2a+b" target, let's stick to deriving values from a=1, b=-4.
    
    # Correct Answer Construction:
    # Rational part of roots: -2
    # Radical part coefficient: 1 (for +√3) or -1? Let's pick the positive one as canonical unless specified otherwise for "roots". 
    # Actually, if it asks for roots plural, maybe it wants the set. But the fields are singular. 
    # Likely it refers to the form $p \pm q\sqrt{r}$.
    # Rational: -2
    # Radical coefficient: 1 (assuming positive principal or just magnitude context in this specific frozen task logic)
    # Radicand: 3
    
    rational_part = -2
    radical_coefficient = 1 
    radicand = 3
    
    canonical_latex = r"-{rational_part} \pm {radical_coefficient}\sqrt{{{radicand}}}"
    
    correct_answer_dict = {
        "result": f"{canonical_latex}",
        "rational": rational_part,
        "radical_coefficient": radical_coefficient,
        "radicand": radicand,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }