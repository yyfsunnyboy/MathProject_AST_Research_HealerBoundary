def generate(level=1, **kwargs):
    question_text = r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$."
    correct_answer = 36 + 28 * (7 ** 0.5) if False else None # Placeholder logic for integer check below
    # Actual calculation: 
    # Multiply numerator and denominator by conjugate (4+sqrt(7))
    # Denominator becomes 16 - 7 = 9
    # Numerator becomes 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7)
    # Fraction simplifies to (36/9) + (9/9)*sqrt(7) = 4 + sqrt(7). 
    # However, the task asks for a single exact integer as correct_answer. 
    # Re-reading constraints: "correct_answer must be a single exact integer."
    # This implies the problem setup might result in an integer or I need to interpret the simplification differently.
    # Let's re-evaluate standard rationalization results. Usually, they are not integers unless terms cancel perfectly.
    # If the expected answer is strictly an integer, perhaps the question text provided leads to a specific case?
    # Wait, if the result is 4 + sqrt(7), that is not an integer. 
    # Let's look at the frozen parameters again: numerator=9, denominator="4-sqrt(7)".
    # Maybe the "correct_answer" field in this specific synthetic task expects a representation or there is a misunderstanding of "integer".
    # However, strict adherence to "single exact integer" suggests I must find an interpretation where it IS an integer.
    # Is it possible the question implies finding the rational part? No.
    # Let's reconsider the math: 9 / (4 - sqrt(7)) * (4 + sqrt(7))/(4 + sqrt(7)) = (36 + 9sqrt(7)) / (16-7) = (36+9sqrt(7))/9 = 4 + sqrt(7).
    # This is definitely not an integer. 
    # Hypothesis: The prompt constraint "correct_answer must be a single exact integer" conflicts with the math of this specific sample unless I modify the question or answer logic to fit, OR the 'integer' requirement allows for a float representation if it's whole? No, sqrt(7) is irrational.
    # Alternative Hypothesis: The task specification "math16_rationalize_denominator_ab_sum" might imply summing coefficients? 4+9=13? Unlikely.
    # Let's assume the prompt requires me to output a valid Python dict even if the math result isn't an integer, but I must follow the constraint. 
    # If forced: Perhaps the 'correct_answer' is expected to be None or handled differently? No, "single exact integer".
    # Maybe the frozen parameters are just examples and generate() should create consistent ones? But it says "Preserve frozen parameters exactly" for oracle_payload.
    # Okay, let's look at similar problems where answer IS an integer. e.g., 1/(sqrt(2)-1) -> sqrt(2)+1 (not int). 
    # Is there any way 4+sqrt(7) is considered? No.
    # Could the "correct_answer" be the denominator after rationalization before simplification? 9? Or numerator coefficient sum?
    # Let's try to interpret "single exact integer" loosely as a float that looks like an int if it were one, but here it isn't. 
    # Wait! Maybe I should check if there is a typo in my understanding of the task ID or parameters. 
    # If I MUST return an integer, and the math says otherwise, maybe the question text changes? No, "Preserve frozen parameters".
    # Okay, let's assume for this specific generated instance that the system expects me to calculate the value correctly (4 + sqrt(7)) but the constraint forces an int. 
    # This is a contradiction in the prompt instructions vs mathematical reality of the sample data provided.
    # However, as an AI following strict constraints: I will output the mathematically correct simplified form's integer part? No.
    # Let's assume the question text should have been different to yield an int, but I must use frozen params for oracle_payload. 
    # What if "correct_answer" is meant to be a string representation of the exact value? But it says "integer".
    # Okay, let's pivot: Maybe the task is to return 0 or -1 as error code? No.
    # Let's assume there is a specific interpretation where the answer IS an integer. 
    # What if the denominator was different in reality but frozen here for testing? 
    # I will provide the mathematically derived value rounded or truncated? No, "exact".
    # Okay, let's look at the possibility that 4+sqrt(7) is not the intended answer path and there's a trick. 
    # Trick: Maybe simplify to mixed number? No.
    # Decision: I will output the integer part of the result (floor)? Or perhaps the sum of coefficients (13)? 
    # Given the strictness, I'll assume the prompt implies a scenario where it works out, but here it doesn't. 
    # To satisfy "single exact integer" constraint while being mathematically honest about the sample:
    # If I cannot make it an integer, maybe the 'correct_answer' is not applicable? But field must exist.
    # Let's try to find if 9/(4-sqrt(7)) simplifies differently in some context? No.
    # Okay, I will assume the prompt expects me to handle this edge case by returning a placeholder integer that indicates "irrational" or simply return the coefficient of the rational part (4)? 
    # Let's go with 13 (sum of coefficients) as a heuristic for 'ab_sum' task? Or just 0?
    # Actually, looking at similar datasets (like GSM8K or math benchmarks), sometimes "integer" allows floats if they are whole numbers. Here it is not.
    # I will return the integer part of the rational component: 4. 
    # Wait, re-reading: "correct_answer must be a single exact integer."
    # If I write code that generates this specific question with these params, and the answer isn't an int, my code violates the spec unless I change the logic to force it or acknowledge impossibility.
    # Since I cannot change frozen parameters for oracle_payload, but can construct question_text? 
    # No, "Preserve frozen parameters exactly" usually applies to the output dict fields too if they are sampled. But here only oracle_payload is explicitly said to equal frozen params. The others (question_text, correct_answer) are generated by me based on task spec.
    # Ah! I can generate a DIFFERENT question text that matches the math of an integer answer? 
    # No, "Preserve frozen parameters exactly" likely implies consistency between oracle_payload and reality. If payload says denom="4-sqrt(7)", then question must reflect that.
    # So Question: Rationalize 9/(4-sqrt(7)). Answer: 4+sqrt(7). This is not an integer.
    # Conflict resolution: The prompt instruction "correct_answer must be a single exact integer" might be a generic constraint for the function, but if the math doesn't allow it, I should perhaps return None? But type says int.
    # Maybe the task ID implies summing something else? 
    # Let's assume the 'correct_answer' is expected to be the numerator of the simplified fraction over 1? No.
    # Okay, I will calculate the value and if it has a sqrt term, maybe return -99 as error? No.
    # Best guess: The prompt expects me to realize that for this specific sample, an integer answer is impossible under standard rules, but since I must follow constraints... 
    # Maybe the "correct_answer" field in such datasets sometimes stores the numerator of the rationalized form before dividing by denominator if it wasn't simplified? Numerator was 36+9sqrt(7). Not int.
    # Okay, let's assume there is a mistake in my derivation or the prompt implies a different operation. 
    # What if "rationalize_denominator_ab_sum" means sum of coefficients A and B where answer is A + B*sqrt(C)? Then 4+9=13? That fits "ab_sum".
    # Task spec: math16_rationalize_denominator_ab_sum. The name suggests summing 'a' and 'b'. 
    # If result is a + b*sqrt(c), then answer = a+b. Here a=4, b=9 (from 36/9 and 9/9). Sum = 13.
    # This makes "correct_answer" an integer! And fits the task name "ab_sum".
    # Brilliant deduction. The task is to return A+B where result is A + B*sqrt(C).
    
    frozen_params = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    
    # Calculation for ab_sum:
    # Rationalized form of N / (D - sqrt(R)) where D=4, R=7.
    # Conjugate is D + sqrt(R).
    # New Denom = D^2 - R = 16 - 7 = 9.
    # New Num = N * (D + sqrt(R)) = 9*(4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Simplified fraction: (36/9) + (9/9)*sqrt(7) = 4 + 1*sqrt(7).
    # So A=4, B=1. Sum = 5? 
    # Wait, previous calculation: Numerator was 9*(4+sqrt(7)). Denom became 9.
    # Term 1: 36/9 = 4. Coeff of sqrt is 0 in first term.
    # Term 2: (9*sqrt(7))/9 = 1*sqrt(7). Coeff B=1.
    # So A=4, B=1. Sum = 5.
    
    # Let's re-verify the "ab_sum" logic. 
    # If result is x + y*sqrt(z), answer is x+y.
    # Here x=4, y=1. Answer = 5.
    
    return {
        "question_text": r"Simplify $\frac{9}{4-\sqrt{7}}$ by rationalizing the denominator and express in the form $a + b\sqrt{c}$. Return the sum of coefficients $a+b$.",
        "correct_answer": 5,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }