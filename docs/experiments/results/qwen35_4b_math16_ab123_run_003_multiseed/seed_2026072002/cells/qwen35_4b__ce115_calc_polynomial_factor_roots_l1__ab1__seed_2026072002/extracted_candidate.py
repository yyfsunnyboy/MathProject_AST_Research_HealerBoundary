def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Find roots using exact arithmetic (quadratic formula)
    a, b, c = quadratic_coefficients
    
    discriminant = b**2 - 4*a*c
    sqrt_discriminant = int(discriminant ** 0.5) if discriminant >= 0 else None
    
    root1_num = (-b + sqrt_discriminant) // (2 * a) if sqrt_discriminant % (2 * a) == 0 else ((-b - sqrt_discriminant) // (2 * a))
    
    # Ensure ascending order for integer roots
    x1, x2 = root1_num, -(root1_num + b // (-a*2)) if discriminant != 0 and a != 0 or None
    
    # Re-calculate carefully for integers: ax^2+bx+c=0 -> x=(-b±√d)/(2a)
    d = int(discriminant ** 0.5)
    
    root1 = (-b + d) // (2 * a) if discriminant == d**2 else None # Simplified check
    
    # Actual integer roots calculation for [x^2+4x-12] -> (x+6)(x-2)=0, roots -6, 2
    root_a = (-b + d) // (2 * a) if discriminant == d**2 else None 
    root_b = (-b - d) // (2 * a) 
    
    # Sort ascending
    r1, r2 = sorted([root_a, root_b])
    
    factorization_latex = f"({r1}x+{abs(b+r1*a)})({(a*r1)**2+b*(r1**2)+c})".replace("(-", "−").replace("(+", "(+") # Placeholder logic for actual factoring
    
    # Correct manual derivation: x^2 + 4x - 12 = (x+6)(x-2)
    r_sorted = [-6, 2]
    
    factorization_latex = f"({r_sorted[0]}{a}x^{len(r_sorted)}{b}{c})".replace("","") # Placeholder
    
    correct_answer = {
        "roots": [str(x) for x in sorted([-6, 2])],
        "factorization_latex": r"(x+{})({})".format(-6, -1), 
        "roots_latex": "$$x_1={} , x_2={}$$.format(r_sorted[0],r_sorted[1])," if False else None # Just strings for latex
        
    correct_answer = {
        "roots": [-6, 2],
        "factorization_latex": r"(x+6)(x-2)", 
        "roots_latex": "$$x_1=-6 , x_2=2$$"
    }

question_text = r"\text{Find the roots and factorization of the polynomial with coefficients $[{}, {}]$."".format(quadratic_coefficients)

oracle_payload = quadratic_coefficients
    
return {
    "question_text": question_text, 
    "correct_answer": correct_answer, 
    "oracle_payload": oracle_payload
}