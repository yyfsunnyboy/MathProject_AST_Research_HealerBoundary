import json
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate LCM using the formula: lcm(a,b) = (a*b)/gcd(a,b)
    # Since we need numbers that are multiples of both, they must be multiples of their LCM.
    # The smallest positive integer satisfying "divisible by divisor_val" and "multiple of multiple_val" is LCM(divisor_val, multiple_val).
    
    from core.prompts.domain_function_library import IntegerOps
    
    def gcd(a: int, b: int) -> int:
        while b != 0:
            a, b = b, a % b
        return a

    common_divisor = gcd(divisor_val, multiple_val)
    
    # LCM calculation using domain API for safety where possible, but standard math is robust here.
    # lcm(a,b) = abs(a*b) // gcd(a,b)
    import math
    
    lcm_value = (divisor_val * multiple_val) // common_divisor
    
    count = 1

    question_text = r"""Find the smallest positive integer $x$ such that:
$x$ is a divisor of $\text{LCM}(216, 18)$? No.
Re-reading task specification logic for 'divisor_of' and 'multiple_of':
The term "divisor_of" implies we are looking for numbers divisible by the given value (often phrased as multiples in such contexts to find an intersection).
However, strictly: 
If a number $x$ is a divisor of 216, then $x | 216$.
If a number $y$ is a multiple of 18, then $18 | y$.

Wait, the task title is "divisor_multiple_intersection". Usually this means finding numbers that are:
1. Divisors of A (A % x == 0)
2. Multiples of B (x % B == 0)

Let's re-evaluate based on standard math problem patterns for such titles.
Pattern A: Find $x$ where $x | \text{divisor\_of}$ AND $\text{multiple\_of} | x$.
This is finding the intersection of divisors of 216 and multiples of 18.

Let's check if there are any numbers that divide 216 AND are divisible by 18.
Multiples of 18: 18, 36, 54, ...
Divisors of 216: Factors of $2^3 \cdot 3^3$.
Is 18 a divisor of 216? Yes ($216 / 18 = 12$).
So the intersection is non-empty. The set includes $\{18, 54, ...\}$ (multiples of LCM(18, factors)).
Actually, if $x$ must divide 216 and be a multiple of 18:
$x = k \cdot 18$.
$k \cdot 18 | 216 \implies k \cdot 18 / 216$ is integer $\implies k/12$ is integer.
So $k$ must be a multiple of 12.
Thus $x = (12m) \cdot 18 = m \cdot 216$.
The only positive divisor of 216 that is also a multiple of 216 is 216 itself.

Let's try the other interpretation often found in these generated tasks: "Find numbers divisible by both".
i.e., $x$ such that $\text{divisor\_of} | x$ AND $\text{multiple\_of} | x$. (This would be LCM).
But the keys are named 'divisor_of' and 'multiple_of'.
If I say "Find a number which is a divisor of 216", it means $x \in \text{Divisors}(216)$.
If I say "Find a number which is a multiple of 18", it means $x \in \text{Multiples}(18)$.

Let's assume the question asks for the count of such numbers within a certain range? No, no range specified.
Usually these tasks ask for the smallest positive integer or the set size if bounded. Without bounds, "count" is infinite unless it implies specific constraints like "positive divisors".
Wait, maybe the task implies: How many integers $x$ exist such that $x$ divides 216 AND $x$ is a multiple of 18?
As derived above ($x = m \cdot 216$), and since $x$ must divide 216 (so $x \leq 216$ for positive integers), the only solution is $m=1$, so $x=216$. Count = 1.

Let's double check with the other interpretation: "Find numbers divisible by both".
If it meant LCM, the count would be infinite without a bound. The presence of 'count' in correct_answer strongly suggests a finite set or a specific single value (like smallest). Given the phrasing "divisor_of" and "multiple_of", the intersection logic $x | A \land B | x$ yields exactly one positive integer if we assume standard divisor definitions ($1..A$) unless specified otherwise.
Actually, divisors of 216 are finite. Multiples of 18 are infinite. Their intersection is $\{ k \cdot 18 \mid k \in \mathbb{Z}^+, (k \cdot 18) | 216 \}$.
$(k \cdot 18)$ divides $216$ means $(k \cdot 18)/216 = k/12$ is an integer. So $k$ must be a multiple of 12 ($12, 24, ...$).
Then the numbers are $12\cdot18=216$, $24\cdot18=432$.
But for these to be divisors of 216, they must be $\leq 216$.
So only 216 works. Count = 1.

This seems the most logical interpretation yielding a finite count of 1.

    # Calculate LCM just in case logic varies slightly (LCM is useful for intersection of multiples)
    lcm_val = IntegerOps.safe_eval(f"lcm({divisor_val}, {multiple_val})") if hasattr(IntegerOps, 'safe_eval') else None
    
    # Re-evaluating based on strict key names:
    # divisor_of 216 -> x divides 216 (x is a factor)
    # multiple_of 18 -> 18 divides x (x is a multiple)
    
    # We need count of positive integers satisfying both.
    # As analyzed, only 216 satisfies this in the range [1, 216].
    # If the domain implies "positive divisors", then yes, count is 1.
    
    correct_answer = {"count": int(count)}

    oracle_payload = json.dumps(frozen_params)

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }