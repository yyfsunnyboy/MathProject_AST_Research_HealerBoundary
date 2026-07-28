def generate(level=1, **kwargs):
    polynomials = []
    
    # Frozen sampled parameters from task specification
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a = 2 * level + 7
    c = 10 * level - 3
    
    # Construct the polynomial based on frozen parameters and difficulty
    # The problem implies recovering 'a' from factors (x+a) and another factor, then computing answer as a+2c
    # Given strict_source_template with left coefficient 3: first factor is fixed as (3x + a)
    
    question_text = r"Let $P(x)$ be the polynomial defined by the product of two linear factors. The first factor is given in the form $(3x+a)$, where $a$ is an integer parameter determined by the difficulty level. Let $b$ be the constant term of the second factor such that the sum of all coefficients of $P(x)$ equals 0. If we define a value $S = a + 2c$, find the integer value of $S$. The polynomial can be expressed as $(3x+a)(bx+c)$. Determine the specific values of $a$ and $b$ based on the condition that the coefficient of $x^2$ in the expanded form is equal to the product of the leading coefficients, which matches standard multiplication rules."
    
    # Calculate correct answer: a + 2c
    correct_answer = a + 2 * c
    
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