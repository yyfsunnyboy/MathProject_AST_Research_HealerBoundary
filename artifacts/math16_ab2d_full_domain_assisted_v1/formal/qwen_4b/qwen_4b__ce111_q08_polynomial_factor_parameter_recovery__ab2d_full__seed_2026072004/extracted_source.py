from core.prompts.domain_function_library import PolynomialOps, Fraction


def generate(level=1, **kwargs):
    # Parse coefficients from string expression if needed, but here we have frozen_params with list[int]
    coeffs = [39, 5, -14]
    
    # Step 1: Factor the quadratic exactly. 
    # The polynomial is ax^2 + bx + c -> a=39, b=5, c=-14
    factors = PolynomialOps.factor_quadratic_exact(39, 5, -14)
    
    # factors[0] and factors[1] are dicts with keys 'x_coefficient' (int or str p/q) and 'constant'.
    # We need to find the factor that matches the template: (3x + a).
    # The template specifies left x_coefficient = 3.
    
    f0_xc, f0_const = factors[0]['x_coefficient'], factors[0]['constant']
    f1_xc, f1_const = factors[1]['x_coefficient'], factors[1]['constant']
    
    # Check which factor has x_coefficient equal to 3. 
    # Note: The API returns int or 'p/q'. We compare directly.
    if str(f0_xc) == "3" and f0_const != None:
        a = f0_const
        b_val = f1_xc
        c_val = f1_const
    elif str(f1_xc) == "3" and f1_const != None:
        # Swap so left factor is (3x + a)
        a = f1_const
        b_val = f0_xc
        c_val = f0_const
    else:
        # Fallback or error case, though problem guarantees integer roots/factors.
        # If one coefficient was 'p/q', we might need to handle it, but template says 3x+a with a int.
        # Let's assume the factorization yields integers as per example and task description.
        raise ValueError("Could not identify (3x + a) factor from exact factors.")

    # Step 2: We have identified a, b_val, c_val corresponding to (3x+a)(bx+c).
    
    # Step 3: Compute a + 2*c using native arithmetic.
    result = int(a) + 2 * int(c_val) if isinstance(result, Fraction) else int(result)

    # Assemble correct_answer exactly according to the Answer contract.
    oracle_payload = {
        "factor_order_policy": kwargs.get("factor_order_policy", "strict_source_template"),
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    return {
        "question_text": "已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。",
        "correct_answer": result,
        "oracle_payload": oracle_payload
    }
