def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    question_text = r"""Find the number of positive integers that are both divisors of $d$ and multiples of $m$, where $d=216$ and $m=18$. Express your answer as an integer."""
    
    lcm_val = (divisor_of * multiple_of) // math.gcd(divisor_of, multiple_of)
    count = divisor_of // lcm_val
    
    correct_answer = {"count": int(count)}
    oracle_payload = {**kwargs}

import math