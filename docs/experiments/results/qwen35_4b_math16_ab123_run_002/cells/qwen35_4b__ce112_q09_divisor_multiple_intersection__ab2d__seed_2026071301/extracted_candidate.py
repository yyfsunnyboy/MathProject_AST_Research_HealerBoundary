def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate LCM using the domain API for safe evaluation of mathematical expression
    from core.prompts.domain_function_library import IntegerOps
    
    lcm_result = IntegerOps.safe_eval(f"lcm({divisor_val}, {multiple_val})")
    
    question_text = f"""Find the number of integers $x$ such that:
1. $x$ is a multiple of $\{multiple\_val}$, and
2. $x$ divides $\{divisor\_val}$.

What is the count of such positive integers?"""
    
    # The count of numbers dividing N that are multiples of M where M|N is simply gcd(N,M) / M * (M/M)? 
    # Actually: x must be a multiple of m and divisor of d.
    # So x = k*m for some integer k, and k*m | d => k*18 | 216.
    # Also we need the set to be non-empty. The problem implies finding how many such numbers exist <= d? 
    # Or is it asking for the count of common divisors/multiples?
    # "divisor_of": means x divides D. "multiple_of": means M divides x.
    # So we need x such that m|x and x|d. This implies m<=x<=d and x is a multiple of m which also divides d.
    # The values are multiples of 18: 18, 36, ... up to max(x) where x divides 216.
    # Since x must divide 216 and be divisible by 18, let x = 18*k. 
    # Then (18*k) | 216 => k * 18 <= 216/k? No. a|b means b/a is int.
    # So 216 / (18k) must be integer.
    # Also x > 0 usually implied in such count problems unless specified non-negative integers including zero. 
    # Given "divisor_of" and "multiple_of", typically positive integers are considered for divisibility properties involving counting.
    # Let's assume positive integers.
    
    # Values of k: 18k divides 216 => 216/(18k) is integer => 12/k is integer.
    # So k must be a divisor of 12.
    # Divisors of 12 (positive): 1, 2, 3, 4, 6, 12. Count = 6.
    
    count_result = IntegerOps.safe_eval(f"len([k for k in range(1, {divisor_val // multiple_val} + 1) if ({divisor_val} / ({multiple_val} * k)) % 1 == 0])")
    
    correct_answer = {"count": int(count_result)}
    
    return {
        "question_text": question_text.replace(" ", r"\ "), # Replace spaces with backslash for LaTeX compatibility as requested by formal delimiters requirement context usually implying standard latex formatting in text. 
                                                              # Actually, the prompt says "use formal LaTeX delimiters where math appears".
                                                              # The template above has $\{...\}$. I will ensure proper escaping or just use \text{} if needed but simple $...$ is fine inside string.
        # Re-writing question_text to be safe with standard latex rendering in Python strings for the text field:
    }

# Correction on Question Text generation logic to strictly follow "formal LaTeX delimiters where math appears" within the string value provided as a single line or properly escaped.
def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    from core.prompts.domain_function_library import IntegerOps
    
    # Calculate count: x is mult of m and divides d.
    # x = k*m, 1 <= k*m <= d (implied positive), and d % (k*m) == 0.
    # This reduces to finding divisors of (d/m). 
    # Here d=216, m=18. d/m = 12. Divisors of 12 are {1, 2, 3, 4, 6, 12}. Count is 6.
    
    quotient_val = divisor_val // multiple_val
    
    count_result = IntegerOps.safe_eval(f"sum(1 for k in range(1, {quotient_val} + 1) if {divisor_val} % ({multiple_val} * k) == 0)")
    
    question_text = r"""Find the number of positive integers $x$ such that:
- $x$ is a multiple of $\{ \text{{\textbackslash integer}}{ \text{\textbackslash integer}{multiple\_val}}}$.
- $x$ divides $\{ \text{\textbackslash integer}{divisor_val} }$.

What is the count?"""
    # Since I cannot dynamically inject raw integers into LaTeX easily without template strings which might break if not handled, 
    # and to ensure "formal LaTeX delimiters where math appears", let's construct it carefully.
    
    final_q = f"Find the number of positive integers $x$ such that:\n- $x$ is a multiple of $\{multiple\_val}$.\n- $x$ divides $\{divisor\_val}$.\n\nWhat is the count?"
    
    correct_answer = {"count": int(count_result)}
    
    return {
        "question_text": final_q,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }