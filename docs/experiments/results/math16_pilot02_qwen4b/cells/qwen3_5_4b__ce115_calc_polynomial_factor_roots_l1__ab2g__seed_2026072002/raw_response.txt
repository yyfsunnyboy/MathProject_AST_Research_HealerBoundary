def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Solve x^2 + 4x - 12 = 0 using exact arithmetic (quadratic formula)
    a, b, c = quadratic_coefficients
    
    discriminant = b**2 - 4*a*c  # 16 - (-48) = 64
    sqrt_discriminant = int(discriminant ** 0.5) if discriminant >= 0 else None
    
    root1_num = -b + sqrt_discriminant
    root1_denom = 2 * a
    root1 = fraction(root1_num, root1_denom)
    
    root2_num = -b - sqrt_discriminant
    root2_denom = 2 * a
    root2 = fraction(root2_num, root2_denom)
    
    # Sort roots ascending (already sorted here: -4 < 3)
    if root1 > root2:
        roots_sorted = [root2, root1]
    else:
        roots_sorted = [root1, root2]
    
    factorization_latex = r"(x + {})(x - {})".format(root1.denominator // abs(root1.numerator), -(root2.numerator if root2.denominator == 1 and root2.numerator < 0 else str(int(-root2)))) # Simplified for integer roots
    
    # Since coefficients are integers, let's compute directly: (x-3)(x+4)
    factorization_latex = r"(x - 3)(x + 4)"
    
    roots_latex = f"{{-{int(root1.numerator)/root1.denom}}}, {{({int(root2.numerator)/root2.denom})}}" if root1 != root2 else "{{{}^2}}".format(int(root1.numerator/root1.denom))

def fraction(n, d):
    return (n, d)

# Re-implementing with proper integer arithmetic for the final output structure to ensure correctness without float usage in logic
    
quadratic_coefficients = [1, 4, -12]
a, b, c = quadratic_coefficients
discriminant = b**2 - 4*a*c # 64

# Roots are (-b +/- sqrt(d)) / (2a) -> (-4 +/- 8) / 2
# Root 1: (-4 + 8)/2 = 4/2 = 3? Wait, formula is -b. So -(-4) = 4. 
# Let's re-verify signs. x^2 + bx + c = 0. b=4. -b = -4.
# Root1: (-4 + 8)/2 = 2 (Wait, math check: 3*4+? No.)
# Equation: x^2 + 4x - 12 = 0. Factors of -12 that add to 4 are 6 and -2. So (x-(-2))(x-6) -> (x+2)(x-6). Roots: -2, 6.
# Let's re-calculate discriminant roots manually.
# x = [-b +/- sqrt(b^2-4ac)] / 2a
# b=4, a=1, c=-12
# disc = 16 - (4*1*-12) = 16 + 48 = 64. Sqrt(64)=8.
# x1 = (-4 + 8)/2 = 4/2 = 2? No. 
# Wait, factors of -12 summing to 4: 6 and -2. Sum is 4. Product is -12. Correct. Roots are 6 and -2.
# Why did my formula give different result?
# x^2 + bx + c = (x-r1)(x-r2) => r1+r2=-b, r1*r2=c.
# If roots are 6 and -2: sum=4 (-b), prod=-12. Correct.
# Formula calculation again: 
# x = [-(-4) +/- sqrt(64)] / (2*1)? NO. The standard form is ax^2+bx+c. Here b=4. So term is +4x.
# Standard formula for ax^2+bx+c=0 is (-b +/- ...).
# So x = [-4 +/- 8] / 2.
# Option 1: (-4 + 8) / 2 = 4/2 = 2. 
# Option 2: (-4 - 8) / 2 = -12/2 = -6.
# Let's check x=2 in x^2+4x-12: 4+8-12=0. Correct.
# Let's check x=-6 in x^2+4x-12: 36-24-12=0. Correct.
# So roots are -6 and 2. 
# My previous factorization attempt (x+2)(x-6) was wrong because sum is +4, but (-2)+(-6)=-8. 
# Factors must be (x-r). If r=2, term is -(x-2)= -x+2? No.
# Roots are 2 and -6. Factorization: (x-2)(x+6). Expansion: x^2 + 6x - 2x -12 = x^2 +4x -12. Correct.

roots_list = [-6, 2] # Ascending order
factor_latex_parts = ["(x - {}),".format(r) for r in roots_list if isinstance(r,int)] 
# Actually just construct string directly
    
correct_answer_dict = {
    "question_text": r"Find the factorization and roots of the polynomial $P(x) = x^2 + 4x - 12$.",
    "correct_answer": {
        "roots": [-6, 2],
        "factorization_latex": r"(x - 2)(x + 6)",
        "roots_latex": "-6, 2"
    },
    "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
}

return correct_answer_dict