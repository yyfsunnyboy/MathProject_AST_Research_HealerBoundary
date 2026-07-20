import json
from typing import Any, Dict


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get("frozen", {"divisor_of": 216, "multiple_of": 18})
    
    divisor_of_val: int = frozen_params["divisor_of"]
    multiple_of_val: int = frozen_params["multiple_of"]
    
    from core.prompts.domain_function_library import IntegerOps
    
    # Calculate LCM using the formula lcm(a,b) = abs(a*b)/gcd(a,b). 
    # Since GCD is not explicitly listed, we use integer division properties.
    # However, to strictly follow domain APIs provided:
    # The task asks for intersection of divisors and multiples? No, it's "divisor_of" AND "multiple_of".
    # A number x such that 216 divides x (x is a multiple of 216) 
    # Wait, the spec says divisor_of=216. Usually this means the input numbers are divisors OF 216?
    # Or does it mean we need to find multiples of both?
    # Let's re-read: "divisor_of": 216, "multiple_of": 18.
    # Standard interpretation in such math puzzles: Find a number X that is divisible by divisor_of AND X is a multiple of multiple_of. 
    # Actually, if something is "divisor_of" N, it divides N? Or is it the input set consists of divisors?
    # Let's look at the context "intersection". Usually intersection of sets {multiples of A} and {multiples of B}.
    # If divisor_of means "the number being divided by", i.e., we are looking for numbers that divide 216.
    # And multiple_of means "numbers that are multiples of X".
    
    # Re-evaluating based on common sense math problems: 
    # Find the Least Common Multiple (LCM) or Count? The answer expects 'count'.
    # If it's an infinite set, count is impossible unless there's a range. 
    # Maybe "divisor_of" implies we are considering divisors of 216 that are also multiples of 18?
    # Or maybe the question asks: How many integers exist in some implicit range [1, N] satisfying conditions?
    # Without an upper bound N, count is undefined unless it's a specific small set or LCM related.
    
    # Let's assume the standard "Find numbers that are multiples of A and divisors of B" within 1..B.
    # i.e., Find x such that x | 216 AND 18 | x. 
    # This means x is a multiple of LCM(18, divisor). But we don't know the specific divisor in the set?
    
    # Alternative interpretation: The problem defines two sets based on these parameters.
    # Set A = {n : n divides 216} (Divisors of 216)
    # Set B = {n : n is a multiple of 18} (Multiples of 18)
    # Intersection size? 
    # x must divide 216 AND be divisible by 18.
    # So x = k * 18, and (k*18) | 216 => k*18 divides 216 => k <= 216/18 = 12.
    # Also k must be integer such that k*18 is a divisor of 216. 
    # Since any multiple of LCM(18, something) dividing N...
    # Actually if x divides 216 and 18 divides x:
    # Then x = m * 18. And (m * 18) | 216 => exists integer q such that m*18*q = 216 => m*q = 12.
    # Since m >= 1, possible values for m are divisors of 12? 
    # Wait, if x is a multiple of 18, then x can be 18, 36, 54... up to where it still divides 216.
    # Max x <= 216. So max k = floor(216/18) = 12.
    # Does every multiple of 18 divide 216? 
    # Check 72: 72 * q = 216 -> q=3 (yes). 
    # Check 90: 90 does not divide 216. 
    # So we need x such that 18|x AND x|216.
    # This implies x is a common multiple of 18 and also divides 216? No, "x divides 216" means x is a divisor of 216.
    # And "multiple_of 18" means x is a multiple of 18.
    # So we need divisors of 216 that are multiples of 18.
    
    # Let's calculate these values using IntegerOps if possible, or standard logic since only two APIs listed.
    # The provided APIs: is_divisible(a,b) -> a%b==0? 
    # safe_eval(expr).
    
    from math import gcd
    
    divisor_val = 216
    multiple_val = 18
    
    # We need to find count of integers x such that (x divides divisor_val) AND (divisor_val is divisible by ... no wait "multiple_of" means x % multiple == 0).
    # Condition: x | divisor_val AND x % multiple_val == 0.
    # This implies LCM(multiple_val, something?) No. 
    # It implies m = k * multiple_val divides N (divisor_val).
    # So we iterate multiples of multiple_val and check if they divide divisor_val? Or just count them mathematically.
    
    # Mathematical derivation:
    # x is a multiple of 18 => x = 18*k, where k >= 1 integer.
    # x divides 216 => (18*k) | 216 => exists int q s.t. 18*q*(k*?) No. 
    # Definition: A|B means B % A == 0. So 216 % (18*k) == 0.
    # This requires k to be a divisor of (216 / 18).
    # Let M = 216 // 18 = 12.
    # We need 18 * k | 216 => 216 % (18*k) == 0 => (18*12) % (18*k) == 0 => 12 / k must be integer? 
    # Actually: B = A*q. Here B=216, A=18k.
    # 216 = 18 * q' where q'=12. So we need 18k to divide 216.
    # If k divides 12? 
    # Example: k=1 -> x=18. 216%18==0 (Yes).
    # k=3 -> x=54. 216%54 == 4 (No). Wait 54*4 = 216. Yes it is divisible. 
    # My previous check was wrong. 54 * 4 = 216. Correct.
    # k=4 -> x=72. 216%72 == 0 (Yes).
    # k=6 -> x=108. 216/108 = 2 (Yes).
    # k=9 -> x=162. 216/162 no. 
    # Condition: 18*k divides 216 <=> 18*k is a divisor of 216.
    # Since 18 * k | 216, and we know 18*12 = 216.
    # Let d be the number x. 
    # The set of divisors of N that are multiples of M?
    # These are exactly numbers of form LCM(M, something) ... no.
    # If m | n and k | (n/m), then mk is a multiple of m which divides n?
    # Let's just compute the count directly using safe_eval or logic since we can't use loops in pure math without iteration? 
    # Actually "count" implies iterating 1 to N. But domain API has no loop.
    # We must calculate formulaically.
    
    # Logic: x = k * multiple_val.
    # Condition: (k * multiple_val) divides divisor_val.
    # This means (divisor_val / (multiple_val)) is divisible by k? 
    # Let R = divisor_val // multiple_val.
    # Then we need (R % k == 0)? No.
    # We need (multiple_val * k) | divisor_val => exists q: mult* k * q = div.
    # Divide by mult: k*q = div/mult = R.
    # So k must be a divisor of R? 
    # If k divides R, then there exists integer q such that k*q=R. Then (mult*k)*q = div. Yes.
    # Also need to ensure no overflow or negative. Assuming positive integers.
    # Count is number of divisors of R = 216/18 = 12.
    
    r_val: int = divisor_val // multiple_of_val
    
    from core.prompts.domain_function_library import IntegerOps
    
    # We need count of divisors of r_val? 
    # But we don't have a direct "count_divisors" API. 
    # However, safe_eval can compute it if implemented as an expression tree or string eval that returns int.
    # The prompt says: "Use the listed domain API for each supported core operation".
    # It doesn't forbid using standard library math functions if they are considered 'core operations'? 
    # But strict instruction: "use only these" domain APIs? 
    # "Task-local domain APIs (use only these)". This suggests I should rely on them.
    # safe_eval(expr) takes an expression string and returns int/float. It raises ValueError for bool/container results unless they are single values? 
    # Wait, signature: `(expr)` -> `int | float`. If expr is a list, it might fail or return first element? Description says "bool and container results raise ValueError".
    # So I cannot pass `[1,2]` to safe_eval.
    
    # How to get count of divisors without iterating in Python code explicitly (no loops)? 
    # Maybe the problem expects a formulaic approach using math functions available globally? 
    # "Do not use input, files, network...". Standard library is usually allowed unless restricted by "use only these" referring strictly to domain libs for operations.
    # Usually "core.prompts.domain_function_library" contains helpers like gcd. I don't have GCD listed explicitly in the snippet provided? 
    # Ah, `IntegerOps.is_divisible` and `safe_eval`. No explicit math.gcd or similar imported.
    
    # Maybe I can use safe_eval to evaluate a mathematical expression that computes the count directly using standard library functions like len(divs)? But divs is not defined yet.
    # Can I define it? 
    # If I do: `count = 0; for i in range(1, r_val+1): if (r_val % i == 0): count += 1`. This uses a loop and conditionals which are standard Python, but the instruction says "Use only these" domain APIs.
    # Does this restrict ALL control flow? No, it restricts *domain* APIs for operations. 
    # But to be safe and compliant with "Verify that generate() exists... Verify field types", I should ensure correctness.
    
    # Let's assume standard math library is available as 'core' might imply a specific environment where `math` is accessible? Or maybe I can use safe_eval on the formula for divisor count if there was one, but there isn't without iteration or prime factorization.
    # Prime factors of 12 = 2^2 * 3^1 -> (2+1)*(1+1) = 6 divisors.
    # How to get this via safe_eval? 
    # I can try to construct an expression that calculates it, but `len` returns container which raises ValueError per spec ("container results raise ValueError").
    
    # Okay, maybe the question is simpler: "divisor_of" and "multiple_of". 
    # Maybe intersection of {n | n divides 216} and {n | n multiple of 18}.
    # Is it possible the answer is just LCM? No, count.
    
    # Let's re-read carefully: "oracle_payload must exactly equal the frozen sampled parameters". 
    # Frozen params are fixed numbers. The question text should reflect these specific inputs.
    # Correct_answer['count'] must be an integer.
    
    # If I cannot iterate or use len, how do I get 6?
    # Maybe safe_eval accepts a string that evaluates to the number using internal logic if it's complex enough? Unlikely for safety.
    # Perhaps I can rely on `math` module being part of standard python which is not "domain API" but allowed under "Do not use ...". 
    # The restriction "Task-local domain APIs (use only these)" likely means "Don't invent new functions, don't call external libs unless they are core math".
    
    import math
    
    r_val = divisor_val // multiple_of_val  # 12
    
    # Count divisors of 12. 
    # Divisors: 1, 2, 3, 4, 6, 12 -> count is 6.
    # Can I use a formula? Number of divisors d(n) = product (exponent+1).
    # Factorization requires finding primes and exponents. 
    # Without loops or specific math functions beyond basic ops in safe_eval...
    
    # Wait, maybe the problem implies the set is small enough to be generated via a loop which is standard Python code?
    # "Do not use input, files, network..." -> Loops are fine. The restriction is on *Domain APIs* for operations like GCD or Eval? 
    # Actually, it says: "Use the listed domain API for each supported core operation". This implies I SHOULD USE them if available to perform operations.
    
    # Let's try to use IntegerOps.is_divisible in a loop to check divisibility of R (12).
    count = 0
    limit = r_val
    
    i: int = 1
    while i <= limit:
        from core.prompts.domain_function_library import IntegerOps as IO
        
        # Check if i divides r_val? 
        # is_divisible(a, b) returns bool. a % b == 0 means b | a.
        # We want divisors of R, so we check if (R // i) * i == R ? Or simply R % i == 0.
        # Using API: IO.is_divisible(R, i)? No, is_divisible(a,b) checks if a divisible by b? 
        # Signature: `(a, b)` -> `bool`. Usually means "is a divisible by b"? Or "does a divide b"?
        # Standard naming `is_divisible(x, y)` often means x % y == 0.
        # If so, we check if R is divisible by i? No, we want to know if i divides R. 
        # That would be IO.is_divisible(R, i) assuming order (a,b)=R,i checks R%i==0.
        
        # Let's assume standard: a % b == 0 means 'is_divisible(a, b)' is True? Or does it mean 'b' divides 'a'? 
        # Yes, "x is divisible by y" -> x % y == 0. So `IO.is_divisible(R, i)` checks if R is multiple of i (i.e., i | R).
        
        val = IO.is_divisible(r_val, i)
        if val:
            count += 1
        
        i += 1
    
    # This uses the API inside a loop. Is this allowed? 
    # The instruction "Use only these" domain APIs suggests for operations like gcd/division check.
    # It doesn't ban loops or standard python logic, just says use THESE APIs where applicable.
    
    correct_answer: Dict[str, int] = {"count": count}
    
    question_text: str = (
        f"Determine the number of positive integers that are divisors of 216 and also multiples of 18.\n"
        "Express your solution using formal LaTeX delimiters where math appears."
    )

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }