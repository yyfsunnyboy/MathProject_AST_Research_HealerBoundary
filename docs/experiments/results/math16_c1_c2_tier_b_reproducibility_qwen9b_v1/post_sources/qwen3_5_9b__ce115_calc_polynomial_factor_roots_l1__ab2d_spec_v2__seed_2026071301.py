# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}

    # Native Python arithmetic to factor x^2 + 4x - 12
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]

    # Calculate discriminant: D = b^2 - 4ac
    delta = (b ** 2) - (4 * a * c)

    # Since coefficients are integers and problem is level 1, roots should be rational/integer.
    sqrt_delta = int(delta ** 0.5) if delta >= 0 else None
    
    # Calculate roots: (-b +/- sqrt(D)) / (2a)
    root1_num = -b + sqrt_delta
    root2_num = -b - sqrt_delta
    denom = 2 * a

    # Ensure ascending order for the list of roots
    if float(root1_num / denom) > float(root2_num / denom):
        r_asc_0, r_asc_1 = int(root2_num // denom), int(root1_num // denom)
    else:
        r_asc_0, r_asc_1 = int(root1_num // denom), int(root2_num // denom)

    # Construct LaTeX strings for factorization and roots
    # Factor form: (x - root1)(x - root2). Note: Python integers are exact.
    f_r1_str = str(r_asc_0)
    f_r2_str = str(r_asc_1)
    
    # Format factors as "(x + A)" or "(x - B)". 
    # If factor is (x - r), then term inside is (-r). So we write x + (-r).
    sign1 = "+" if r_asc_0 >= 0 else "-"
    val1_str = str(abs(r_asc_0)) if r_asc_0 != 0 else "0" # Handle zero case explicitly though unlikely here
    
    # Actually, standard factorization (x - root)(x - other_root). 
    # Let's stick to the mathematical form: x^2 + bx + c = (x - p)(x - q)
    # where p and q are roots.
    
    term1_part = f"x{'' if r_asc_0 == 0 else ('+' if r_asc_0 > 0 else '-')} {abs(r_asc_0)}" \
                 .replace("+-", "-").replace("-+", "+") if abs(r_asc_0) != 0 or (r_asc_0==0 and b!=0) else "x"
    # Simpler approach for LaTeX factor string: "(x - r1)(x - r2)" where r are the roots.
    
    def format_factor(root):
        if root == 0:
            return "x"
        elif root > 0:
            return f"x-{root}"
        else:
            # root is negative, so x - (-k) = x + k
            return f"x+{abs(root)}"

    factor_latex_str = f"{format_factor(r_asc_1)}({format_factor(r_asc_2)})".replace("r_asc", "root") \
                       .replace("{format_factor(r_asc_1)", format_factor(r_asc_0)) \
                       .replace(format_factor(r_asc_1), "") # Cleanup logic above was messy. Let's restart string building cleanly.

    # Re-building factor latex cleanly:
    f_str = lambda r: "x" if r == 0 else ("x-" + str(-r) if r < 0 else "x+" + str(r)) \
        .replace("+-", "-").replace("-+", "+") # Wait, logic error in lambda above.
    
    def mk_factor_str(val):
        if val == 0: return "x"
        elif val > 0: return f"x-{val}"
        else: return f"x+{abs(val)}"

    factor_latex = f"{mk_factor_str(r_asc_1)}({mk_factor_str(r_asc_2)})".replace("r_asc", "") # Still messy variable names in string.
    
    # Correct clean build:
    term_a = mk_factor_str(r_asc_0)
    term_b = mk_factor_str(r_asc_1)
    factor_latex = f"{term_a}({term_b})"

    roots_list = [r_asc_0, r_asc_1]
    
    # Roots LaTeX: x_{root 1}, x_{root 2} or just the values? 
    # Usually "roots latex" implies a list like \{x_1, x_2\} or similar.
    # Spec says "roots_latex". Let's format as comma separated math mode numbers.
    roots_latex = f"x={r_asc_0},\\quad x={r_asc_1}"

    question_text = (f"Find the roots and factorization of the quadratic polynomial $x^2 + {b}x + {c}$.\n\n"
                     "Enter your answer as a list of two integers representing the roots in ascending order, followed by the factored form.")

    correct_answer_dict = {
        "roots": [r_asc_0, r_asc_1],
        "factorization_latex": factor_latex,
        "roots_latex": f"x={r_asc_0},\\quad x={r_asc_1}"
    }

    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }