def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor = frozen_params["divisor_of"]
    multiple = frozen_params["multiple_of"]
    
    # Find the smallest positive integer that is a multiple of 'multiple' 
    # and also a divisor (factor) of 'divisor'.
    # This number must be k * multiple, where k * multiple divides divisor.
    # So we look for multiples of 'multiple' up to 'divisor' and check divisibility.
    
    count = 0
    
    current_multiple = multiple
    while current_multiple <= divisor:
        if divisor % current_multiple == 0:
            count += 1
        current_multiple += multiple
        
    question_text = r"The smallest positive integer that is a multiple of $\\frac{" + str(multiple) + r"}{1}$ and also a factor of $" + str(divisor) + r"$."
    
    return {
        "question_text": question_text,
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params
    }