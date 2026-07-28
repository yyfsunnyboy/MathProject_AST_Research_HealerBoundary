# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters defined directly per task specification.
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    # Native Python arithmetic to solve for factors (3x + a)(bx + c) = 39x^2 + 5x - 14.
    # Expansion: 3b x^2 + (3c + ab)x + ac = 0
    # Equations:
    # 1) 3 * b = 39 => b = 13
    # 2) a * c = -14
    # 3) 3*c + a*b = 5
    
    # Calculate 'b' from the leading coefficient.
    b_val = quadratic_coefficients[0] // template_left_x_coefficient
    
    # Iterate through integer factors of ac (-14) to find valid (a, c).
    possible_ac_values = [-28, -14, 7, 2, -7, -2, 14, 28] 
    found_solution = False
    correct_a = None
    
    for a in range(-30, 35): # Search reasonable integer bounds around factors of 14
        if quadratic_coefficients[2] % a == 0:
            c_val = quadratic_coefficients[2] // a
            
            # Check middle term condition: 3*c + a*b = 5
            if (template_left_x_coefficient * c_val) + (a * b_val) == quadratic_coefficients[1]:
                correct_a = a
                found_solution = True
                break
    
    # Compute the required answer: a + 2c. Since we have 'correct_a', calculate 'c' now.
    if not found_solution or correct_a is None:
        raise ValueError("Failed to recover polynomial parameters using native arithmetic.")
    
    c_val = quadratic_coefficients[2] // correct_a
    
    # Construct the question text with formal LaTeX delimiters manually (no external API).
    latex_left_factor = f"({template_left_x_coefficient}x + {correct_a})"
    latex_right_factor = f"({b_val}x + {c_val})"
    
    polynomial_text = f"{latex_left_factor}\\cdot{latex_right_factor}"
    question_text = r"\textbf{Task: Polynomial Factor Parameter Recovery}\n\nGiven the quadratic equation $39x^2 + 5x - 14$, factor it into two linear terms with integer coefficients. The first term is fixed in the form $(3x+a)$. Find the value of $a+2c$ where the factors are $(3x+a)$ and $(bx+c)$."
    
    correct_answer = str(correct_a + 2 * c_val)
    
    # Oracle payload must exactly equal the frozen sampled parameters.
    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }