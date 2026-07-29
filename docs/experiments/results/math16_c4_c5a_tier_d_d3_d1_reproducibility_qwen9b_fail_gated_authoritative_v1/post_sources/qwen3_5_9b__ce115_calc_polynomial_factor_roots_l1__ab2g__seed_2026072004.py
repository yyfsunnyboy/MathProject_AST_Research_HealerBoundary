def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Calculate roots using exact arithmetic (fractions) to avoid floats
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    
    if discriminant < 0:
        raise ValueError("No real roots for the given coefficients.")
    
    sqrt_discriminant = int(discriminant ** 0.5)
    root1_num = (-b + sqrt_discriminant) // (2 * a)
    root1_denom = 2 * a
    
    # Handle simplification of fractions manually if needed, but for this specific case:
    # roots are integers here because discriminant is perfect square and divisible.
    # Let's verify divisibility to ensure exact integer representation or simple fraction string.
    
    def simplify_fraction(numerator, denominator):
        common = 1
        min_abs = abs(min(abs(numerator), abs(denominator)))
        for i in range(2, int(min_abs ** 0.5) + 1):
            if numerator % i == 0 and denominator % i == 0:
                while numerator % i == 0 and denominator % i == 0:
                    common = i * common # simplified logic below is better
        import math
        gcd_val = abs(math.gcd(numerator, denominator))
        return (numerator // gcd_val) / (denominator // gcd_val), gcd_val

    root1_num_simplified = -b + sqrt_discriminant
    root2_num_simplified = -b - sqrt_discriminant
    
    # Construct roots as exact values. Since inputs are integers and discriminant is perfect square,
    # we check if they divide evenly by 2a.
    
    def get_root_value(num_val):
        denom = 2 * a
        gcd_num_denom = abs(int(__import__('math').gcd(num_val, denom)))
        simplified_num = num_val // gcd_num_denom
        simplified_denom = denom // gcd_num_denom
        
        if simplified_denom == 1:
            return str(simplified_num)
        else:
            # Return as a fraction string for exactness in LaTeX context usually preferred or float if integer? 
            # Task says "Exact arithmetic; no floats". So use Fraction representation.
            return f"{simplified_num}/{simplified_denom}"

    root1_str = get_root_value(root1_num_simplified)
    root2_str = get_root_value(root2_num_simplified)
    
    roots_list = sorted([root1_str, root2_str]) # Ascending order
    
    factorization_latex = f"(x - {roots_list[0]})(x - {roots_list[1]})" if a == 1 else f"{a}(x - {roots_list[0]})(x - {roots_list[1]})"
    
    roots_latex = f"${roots_list[0]}, ${roots_list[1]}"

    return {
        "question_text": r"Solve the quadratic equation $ax^2 + bx + c = 0$ for coefficients $a=1, b=4, c=-12$. Find the exact real roots and write them in ascending order.",
        "correct_answer": {
            "roots": [root1_str, root2_str], # List of strings representing exact values
            "factorization_latex": factorization_latex,
            "roots_latex": f"${roots_list[0]}, ${roots_list[1]}"
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }