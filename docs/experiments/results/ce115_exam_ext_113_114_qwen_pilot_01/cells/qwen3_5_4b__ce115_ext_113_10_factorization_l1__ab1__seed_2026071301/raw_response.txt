def generate(level=1, **kwargs):
    expression = "5*x*(5*x - 2) - 4*(5*x - 2)**2"
    
    # Factor out the common binomial (5x - 2)
    # The expression is of the form A*B - C*B^2 where B = (5x-2), A=10x, C=4
    # Factored form: (5*x - 2) * (10*x - 4*(5*x - 2))
    
    inner_factor = "10*x - 4*(5*x - 2)"
    outer_binomial = "(5*x - 2)"
    
    # Simplify the second factor: 10x - 20x + 8 = -10x + 8
    simplified_second_factor = "-10*x + 8"
    
    # We can also write this as (4*3) and (-5/2)x... but let's keep integers.
    # Let's factor out a common constant from the second term to make it monic or simpler?
    # -10x + 8 = 2 * (-5x + 4). 
    # So full expression: (5x-2) * 2 * (-5x+4)
    # Or we can just list the linear factors as requested. The prompt asks for "two {x_coefficient, constant} linear factors".
    # Usually this implies the monic form or integer coefficient form without extra scalar multipliers outside the pair if possible, 
    # but strictly speaking (5x-2) and (-10x+8) multiply to give 4*(5x)^2... wait.
    
    # Let's re-calculate:
    # Original: 5*x*(5*x - 2) - 4*(5*x - 2)**2
    # = (5*x - 2) * [ 5*x - 4*(5*x - 2) ]
    # = (5*x - 2) * [ 5*x - 20*x + 8 ]
    # = (5*x - 2) * [ -15*x + 8 ]
    
    factor_1_x_coeff, factor_1_const = 5, -2
    factor_2_x_coeff, factor_2_const = -15, 8
    
    correct_answer = {
        "factors": [
            {"x_coefficient": factor_1_x_coeff, "constant": factor_1_const},
            {"x_coefficient": factor_2_x_coeff, "constant": factor_2_const}
        ]
    }
    
    oracle_payload = expression
    
    return {
        "question_text": f"Factorize the following algebraic expression completely: {expression}",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }