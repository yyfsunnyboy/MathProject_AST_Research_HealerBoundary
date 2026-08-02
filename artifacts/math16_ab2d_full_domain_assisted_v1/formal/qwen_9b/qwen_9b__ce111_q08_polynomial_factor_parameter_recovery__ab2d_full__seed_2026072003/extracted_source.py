from core.prompts.domain_function_library import PolynomialOps, Fraction

def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # Step 1: Factor the quadratic exactly.
    a_quad, b_quad, c_quad = frozen_params["quadratic_coefficients"]
    
    # The API expects (a,b,c) for ax^2 + bx + c. 
    # We call factor_quadratic_exact with these coefficients.
    factors_raw = PolynomialOps.factor_quadratic_exact(a_quad, b_quad, c_quad)

    # Step 2: Handle the order policy "strict_source_template".
    # The template requires the left factor to be (3x + a). 
    # This means the x-coefficient of the first returned dict must be 3.
    
    f1 = factors_raw[0]
    f2 = factors_raw[1]

    if f1["x_coefficient"] != frozen_params["template_left_x_coefficient"]:
        # Swap them so that the left one matches the template requirement (3)
        f1, f2 = f2, f1

    # Step 3: Extract a and c from the factors.
    # Factor form is (x_coeff * x + constant). 
    # So for factor d*x + e, we have x_coeff=d, constant=e.
    # The problem statement says factors are (3x+a) and (bx+c).
    # Thus: a = f1["constant"], c = f2["constant"].
    
    val_a = f1["constant"]
    val_c = f2["constant"]

    # Compute result: a + 2*c
    result_int = int(val_a) + 2 * int(val_c)

    return {
        "question_text": r"已知\[39x^2+5x-14=(3x+a)(bx+c),其中 \(a,b,c\) 均為整數，求 \(a+2c\)。",
        "correct_answer": result_int,
        "oracle_payload": frozen_params
    }