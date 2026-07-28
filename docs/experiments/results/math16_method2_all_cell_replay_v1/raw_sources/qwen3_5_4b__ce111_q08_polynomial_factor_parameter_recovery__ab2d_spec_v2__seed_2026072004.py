# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters defined exactly as specified in task specification.
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    # Native Python arithmetic to solve for a and c from (3x + a)(bx + c) = 39x^2 + 5x - 14.
    # Expansion: 3b x^2 + (3c + ab)x + ac = 0
    # Equations:
    # 1) 3 * b = 39 => b = 13
    # 2) a * c = -14
    # 3) 3*c + 13*a = 5
    
    # Calculate b directly from the leading coefficient.
    b_coefficient = quadratic_coefficients[0] // template_left_x_coefficient
    
    # We need integer solutions for a and c such that:
    # ac = -14
    # 3c + 13a = 5
    
    # Iterate through divisors of -14 to find valid integers.
    possible_a_values = []
    
    # Check all factors of |ac| which is 14.
    abs_ac = abs(quadratic_coefficients[2])
    for i in range(1, int(abs_ac**0.5) + 1):
        if abs_ac % i == 0:
            divisors = [i, -i]
            other_divisor = abs_ac // i
            others = [-other_divisor, other_divisor]
            
            for a in divisors:
                for c in others:
                    # Verify the middle term condition: 3*c + b*a == quadratic_coefficients[1]
                    if (template_left_x_coefficient * c) + (b_coefficient * a) == quadratic_coefficients[1]:
                        possible_a_values.append(a)
    
    # The problem implies unique factorization over integers. 
    # Given the constraints and typical polynomial problems, there should be one valid pair.
    if len(possible_a_values) > 0:
        selected_a = possible_a_values[0]
        
        # Calculate c based on ac = -14 (or re-verify with equation)
        calculated_c = quadratic_coefficients[2] // selected_a
        
        # Verify the second condition again to be absolutely sure.
        if (template_left_x_coefficient * calculated_c) + (b_coefficient * selected_a) != quadratic_coefficients[1]:
            raise ValueError("No valid integer factors found for given coefficients.")
        
        correct_answer = selected_a + 2 * calculated_c
        
    else:
        # Fallback or error state if logic fails, though math guarantees a solution here.
        correct_answer = "error"

    # Construct the question text using formal LaTeX delimiters as requested.
    # We construct it manually to avoid external API dependencies per instructions ("Do not use domain APIs").
    latex_left_factor = f"(\\{template_left_x_coefficient}x + {selected_a})"
    
    # Calculate b for display in the expanded form if needed, or just state coefficients.
    # The task asks for question_text using formal LaTeX delimiters.
    # We will format it as: Factorize 39x^2 + 5x - 14 into (3x+a)(bx+c).
    
    latex_right_factor = f"({b_coefficient}x + {calculated_c})"
    
    question_text = r"\text{Factor the polynomial } $39x^2 + 5x - 14$ \text{ into two linear factors of the form } $(\mathbf{\underline{{}}}\, x + a)(bx + c)$."

    # Prepare oracle_payload exactly as frozen sampled parameters.
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