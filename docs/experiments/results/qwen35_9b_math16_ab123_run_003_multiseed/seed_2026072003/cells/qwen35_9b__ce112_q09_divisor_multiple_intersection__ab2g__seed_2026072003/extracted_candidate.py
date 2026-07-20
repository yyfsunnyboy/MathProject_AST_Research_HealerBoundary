def generate(level=1, **kwargs):
    import copy
    
    # Frozen sampled parameters as specified in the task
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate correct answer: count of numbers that are both a divisor of 'divisor_val' 
    # and a multiple of 'multiple_val'.
    # A number x must satisfy: x % multiple_val == 0 AND divisor_val % x == 0.
    # This implies x is a common element in the set of divisors of N and multiples of M.
    
    count = 0
    
    # Iterate through all possible candidates up to divisor_val (since it's a divisor, cannot exceed)
    for candidate in range(1, divisor_val + 1):
        if candidate % multiple_val == 0:
            if divisor_val % candidate == 0:
                count += 1
                
    question_text = r"""Find the number of positive integers that are both a divisor of $N$ and a multiple of $M$, where $N=\{n\}$ and $M=\{m\}$.

Given parameters:
- Divisor constraint ($N$): $\{div\_val\}$
- Multiple constraint ($M$): $\{mult\_val\}$

Calculate the count."""
    
    # Substitute values into LaTeX string safely
    question_text = question_text.replace("{div_val}", str(divisor_val))
    question_text = question_text.replace("{mult_val}", str(multiple_val))
    
    correct_answer = {"count": int(count)}
    oracle_payload = copy.deepcopy(frozen_params)
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }