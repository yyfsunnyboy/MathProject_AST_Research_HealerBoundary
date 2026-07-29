def generate(level=1, **kwargs):
    import re
    
    denominator_str = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    # The expression is (numerator) / (denominator).
    # To rationalize the denominator of a/b where b = x - sqrt(y), we multiply by conjugate x + sqrt(y).
    # Here, x=4, y=7. Conjugate is 4+sqrt(7).
    # Numerator becomes: num * (x + sqrt(y)) = 9*(4 + sqrt(7)) = 36 + 9*sqrt(7)
    # Denominator becomes: (x - sqrt(y))*(x + sqrt(y)) = x^2 - y = 16 - 7 = 9.
    # The rationalized fraction is (36 + 9*sqrt(7)) / 9.
    # Simplifying by dividing numerator and denominator by their GCD (which includes the integer part).
    # We need to check if there's a common factor for both terms in the new numerator relative to the new denominator.
    # New Numerator: 36 + 9*sqrt(7) = 9*(4 + sqrt(7))
    # New Denominator: 9
    # Resulting Fraction: (9 * (4 + sqrt(7))) / 9 = 4 + sqrt(7).
    
    # The question asks for the rationalized denominator form, which usually implies writing it as a sum of an integer and a radical.
    # So the answer is 4+sqrt(7). However, the task specification says "correct_answer must be a single exact integer".
    # Let's re-read carefully: "math16_rationalize_denominator_ab_sum" with frozen params {"denominator": "4-sqrt(7)", ...}.
    # Usually rationalizing 9/(4-sqrt(7)) results in (36+9sqrt(7))/9 = 4 + sqrt(7). This is not an integer.
    
    # Is it possible the task implies extracting a specific component or there's a trick?
    # Or perhaps I need to rationalize differently? No, standard algebraic manipulation yields 4+sqrt(7).
    # Let's reconsider the "single exact integer" constraint. 
    # Maybe the input is different in a way that makes it an integer?
    # If denominator was sqrt(something), result might be irrational unless numerator cancels out perfectly which isn't possible here with simple integers.
    
    # Wait, could the question text ask for something else derived from this?
    # Or maybe I should output 4 + int(sqrt(7))? No, that's not standard math notation in these tasks usually.
    # Let's look at similar problems (e.g., rationalizing a/b where b is quadratic). 
    # If the result was an integer, then sqrt(7) term must vanish or be absorbed. It doesn't here.
    
    # Hypothesis: The prompt constraint "correct_answer must be a single exact integer" might be a generic instruction for this specific task type that assumes inputs are chosen such that it works, OR I am misinterpreting the math16_rationalize_denominator_ab_sum logic.
    # Let's re-calculate: 
    # Expression: 9 / (4 - sqrt(7))
    # Multiply by (4 + sqrt(7))/(4 + sqrt(7)):
    # Num: 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7)
    # Denom: 16 - 7 = 9
    # Result: (36/9) + (9/9)*sqrt(7) = 4 + sqrt(7).
    
    # Is it possible the "numerator" provided in frozen params is actually part of a larger expression where cancellation happens? 
    # No, numerator=9.
    
    # Let's consider if the task expects the answer to be formatted as `a+b` but constrained to integer implies maybe I should return 4 + int(math.sqrt(7)) which is invalid mathematically for exactness unless sqrt(7) was a perfect square (it isn't).
    
    # Alternative interpretation: Maybe the "oracle_payload" contains hints? No, it's just params.
    # Could the question text be asking to rationalize and then evaluate something specific? 
    # Or maybe I should assume there is an error in my derivation or the problem setup implies a different operation?
    
    # Let's try another angle: Maybe the denominator was `sqrt(4) - sqrt(something)`? No, it says "4-sqrt(7)".
    
    # What if the question asks for the integer part after rationalization? Or maybe the result is actually an integer due to a specific property I'm missing? 
    # Wait, what if the numerator was 9*sqrt(7)? Then (63 + 81)/... no.
    
    # Let's assume there might be a typo in my understanding of "single exact integer" for this specific frozen set, OR the expected answer is indeed an integer because I am missing a step like squaring? 
    # No, rationalize denominator usually means removing sqrt from bottom. The result 4+sqrt(7) has no sqrt at bottom (it's in numerator).
    
    # Is it possible the question asks for `a` where answer is `a + b*sqrt(c)` and we only return `a`? 
    # Or maybe the "correct_answer" constraint here forces me to find an integer solution, implying my calculation of 4+sqrt(7) might be wrong or the problem expects a different interpretation.
    
    # Let's reconsider the math16_rationalize_denominator_ab_sum task definition from typical datasets (like GSM8K style synthetic data). 
    # Often these tasks generate questions where the answer IS an integer. 
    # Example: Rationalize 3/(sqrt(4)-something) -> result is int?
    # If denominator was `2 - sqrt(something)` and numerator adjusted...
    
    # Given I cannot change frozen params, I must work with them.
    # Params: num=9, den="4-sqrt(7)". Result 4+sqrt(7). 
    # Constraint: correct_answer is single exact integer.
    # This implies either:
    # 1. The result IS an integer and my math is wrong (impossible for sqrt(7)).
    # 2. The question asks to extract the rational part? i.e., "What is the rational number in the sum?" -> 4.
    # 3. There's a specific formatting or context where `sqrt(7)` cancels out completely which requires different inputs, but I must use these.
    
    # Let's assume option 2: The question asks for the integer component of the rationalized expression. 
    # Question text could be "What is the rational part of the simplified fraction?" or similar.
    # But standard phrasing would just ask to simplify. If it simplifies to A + B*sqrt(C), and answer must be int... maybe C=1? No, radicand=7.
    
    # Let's try one more check: Is `4-sqrt(7)` a typo for something that yields an integer? 
    # e.g. if den was 3 - sqrt(something) where num matches to cancel the radical in denominator after multiplication by conjugate? No, rationalization always leaves radical in numerator unless it's a perfect square difference which leads to int denom but irrational num (unless num has matching factor).
    
    # Wait! If the result is `4 + sqrt(7)` and we are forced to return an integer... 
    # Maybe the question asks for `(numerator * conjugate) / denominator` evaluated modulo something? No.
    
    # Let's look at the constraint again: "correct_answer must be a single exact integer".
    # If I strictly follow math, 4+sqrt(7) is not an integer. 
    # However, in some synthetic datasets generated by scripts, there might be cases where they expect `int(result)` or similar if it's close? No, that violates "exact".
    
    # Is it possible the numerator provided (9) allows factoring out sqrt(7)? 
    # 36 + 9*sqrt(7). Factor out 9: 9*(4+sqrt(7)). Denom is 9. Result 4+sqrt(7). Still irrational.
    
    # Could the "numerator" be interpreted differently? No, it's an integer.
    
    # Let's assume the question text asks for `a` in `a + b*sqrt(c)`. 
    # Then answer is 4. This satisfies "single exact integer".
    # I will construct the question to ask for this specific part or ensure the math leads there if possible (but it doesn't lead elsewhere).
    
    # Actually, looking at similar problems online (e.g., from datasets like 'math16'), sometimes they have cases where the answer is an integer. 
    # Example: Rationalize 8/(sqrt(4)-2)? No sqrt in denom then?
    # Maybe I should check if `9` and `(4-sqrt(7))` interact differently? 
    # What if the operation was NOT rationalization but something else? Task name says "rationalize_denominator".
    
    # Okay, let's proceed with the assumption that the question asks for the integer part of the result. This is a common pattern when constraints force an integer output from irrational inputs in synthetic tasks (asking for 'a' in `a + b*sqrt(c)`).
    
    rational_part = 4
    
    frozen_params = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    
    question_text = r"Rationalize the denominator of the fraction $\frac{9}{4-\sqrt{7}}$. Express your answer in the form $a + b\sqrt{n}$ where $n$ is square-free. What is the value of $a$?"
    
    # Wait, if I ask for 'a', then correct_answer is 4. 
    # But usually these tasks want the full expression or a specific number derived from it. 
    # If the constraint says "correct_answer must be a single exact integer", and my math gives an irrational... asking for 'a' is the only logical path to satisfy constraints without changing frozen params.
    
    correct_answer = 4
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }