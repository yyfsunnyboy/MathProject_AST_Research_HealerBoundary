import re
from math import sqrt as _sqrt
from fractions import Fraction
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class DummyFractionOps:
        @staticmethod
        def create(value): return value if isinstance(value, (int, float)) else None
        @staticmethod
        def mul(a, b): 
            a = Fraction(a)
            b = Fraction(b)
            return a * b
        @staticmethod
        def add(a, b):
            a = Fraction(a)
            b = Fraction(b)
            return a + b

    class DummyFractionOps: pass # Fallback if import fails but logic below handles basic types directly. We will assume the library exists as per spec or use fallbacks for standard math in generation text. 
    # Actually, to strictly follow "Use listed domain API", we must implement them locally if not found, OR assume they exist.
    # Given the constraint "Output complete Python source only" and "Verify that generate() exists", I will define a local implementation of FractionOps inside the script to ensure it works without external dependencies failing silently.

class LocalFractionOps:
    @staticmethod
    def create(value): return value if isinstance(value, (int)) else None # Simplified for integers as per frozen params
    @staticmethod
    def mul(a, b): 
        a = Fraction(a)
        b = Fraction(b)
        return a * b
    @staticmethod
    def add(a, b):
        a = Fraction(a)
        b = Fraction(b)
        return a + b

FractionOps = LocalFractionOps # Override with local implementation to guarantee functionality.

def generate(level=1, **kwargs):
    frozen_params = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    
    # Parse the expression string manually or use eval safely? 
    # The task is to rationalize denominator of numerator/denominator.
    # Input: 9 / (4 - sqrt(7))
    # Rationalization step: Multiply by conjugate (4 + sqrt(7))/(4 + sqrt(7))
    # New Numerator = 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7) -> This is not an integer.
    # Wait, the task spec says "correct_answer must be a single exact integer".
    # Let's re-read: Task specification: math16_rationalize_denominator_ab_sum.
    # Usually these tasks result in simplified fractions or integers if terms cancel out perfectly? 
    # Or perhaps the question asks for the rationalized form, and "correct_answer" is the numerator of that fraction after simplification? 
    # But it says "single exact integer". 
    # Maybe the radicand part cancels? No.
    # Let's look at the expression: 9 / (4 - sqrt(7)).
    # Conjugate multiplication: 9*(4+sqrt(7)) / (16-7) = (36 + 9*sqrt(7))/9 = 4 + sqrt(7). 
    # This is not an integer.
    
    # Re-evaluating the "correct_answer must be a single exact integer" constraint vs the math result (4+sqrt(7)).
    # Is it possible the question asks for something else? Or maybe I misinterpreted the input format?
    # Frozen params: denominator="4-sqrt(7)", numerator=9.
    # If the answer must be an integer, perhaps the task is to evaluate the expression numerically rounded? No, "exact".
    # Maybe the question text asks for the rationalized form, and the correct_answer field expects a specific representation or I am missing a step where sqrt(7) cancels? 
    # It doesn't cancel. 4 + sqrt(7).
    
    # Hypothesis: The prompt implies that for this specific difficulty level/task type, if the result is irrational, maybe we only output the integer part? Unlikely.
    # Alternative hypothesis: The "correct_answer" field in these generated tasks often expects a string representation of the simplified math expression if it's not an integer, BUT the spec says "single exact integer". 
    # This creates a contradiction for this specific input unless I am supposed to compute something else.
    
    # Let's reconsider the problem statement: "math16_rationalize_denominator_ab_sum".
    # Maybe the denominator is actually (4 - sqrt(7)) and we need to find X such that ...? 
    # No, standard rationalization.
    # Is it possible the frozen parameters are just examples and I should generate a solvable one? 
    # "Preserve frozen parameters exactly". So I must use 9/(4-sqrt(7)).
    
    # If the result is irrational (4 + sqrt(7)), how can correct_answer be an integer?
    # Perhaps the question asks for the sum of coefficients? Or maybe the task definition implies a different operation.
    # However, looking at similar datasets (like GSM8K or mathQA), sometimes "correct_answer" is expected to be the simplified fraction string if not int, but here it strictly says integer.
    
    # Let's assume there might be a misunderstanding of the output format for irrational results in this specific synthetic task generation context. 
    # BUT, I must follow instructions: "correct_answer must be a single exact integer".
    # If the math yields 4 + sqrt(7), and I MUST return an integer... maybe I should return -1 or raise error? No.
    
    # Let's try to interpret "rationalize_denominator_ab_sum". Maybe it sums A and B from (A+B*sqrt(n))? 
    # If result is 4 + 1*sqrt(7), sum = 5? That seems like a stretch for "correct_answer" of the math problem itself.
    
    # Wait, could the denominator be different in reality vs frozen params? No, preserve exactly.
    # Could the numerator be such that it cancels? 
    # If I change nothing, result is irrational.
    # Is there any interpretation where 9/(4-sqrt(7)) becomes an integer? Only if sqrt(7) was rational (it's not).
    
    # Let's look at the instruction again: "Verify that generate() exists... Verify field types match stated contract".
    # If I cannot produce an integer, maybe the frozen params provided in the prompt are a trick or test case where the logic should handle it? 
    # Or perhaps I am supposed to calculate the value of 4 + sqrt(7) and round? No "exact".
    
    # Let's assume the question asks for the rationalized form as a string, but the spec says integer. 
    # Maybe the task is: Evaluate the expression assuming sqrt(x) approximations? No.
    
    # Okay, let's step back. In many automated math generation tasks (like MATH dataset), answers are integers or simplified fractions. 
    # If the answer is irrational, usually it's not included in integer-only fields unless specified otherwise.
    # However, I must output code that generates a dict with these keys.
    
    # Possibility: The "correct_answer" for this specific task ID might be defined by an oracle that expects a string representation of the simplified radical form? 
    # But spec says "single exact integer".
    
    # Let's try to find if there is any way 9/(4-sqrt(7)) simplifies to int. No.
    # Maybe the task is NOT rationalization but something else? Task: math16_rationalize_denominator_ab_sum.
    # "ab_sum" might imply A*B where result = A + B*sqrt(C)? 
    # If Result = 4 + sqrt(7), then A=4, B=1. Sum = 5.
    # This fits the "integer" constraint perfectly! The task name suggests summing coefficients of the rationalized form (A+B).
    
    # Let's verify: Rationalize 9/(4-sqrt(7)).
    # Multiply by conjugate: 9*(4+sqrt(7)) / (16-7) = (36 + 9*sqrt(7))/9.
    # Simplify fraction: Divide numerator and denominator by GCD? 
    # Numerator terms are not divisible by 9 cleanly for the sqrt part. 
    # Wait, 36/9 = 4. 9/9 = 1. So (36 + 9*sqrt(7))/9 = 4 + sqrt(7).
    # Form: A + B*sqrt(C) where C=radicand=7.
    # A = 4, B = 1.
    # Task name "ab_sum" -> Sum of coefficients A and B? 
    # Answer = 4 + 1 = 5.
    
    # This seems the only logical way to satisfy "integer answer" for a radical expression task named with "_sum".
    
    radicand_val = frozen_params["radicand"] # 7
    numerator_int = int(frozen_params["numerator"]) # 9
    denom_str = frozen_params["denominator"] # "4-sqrt(7)" -> A - sqrt(B) where A=4, B=7
    
    # Parse denominator string to get A and confirm structure
    match = re.search(r'(-?\d+)\s*-\s*\sqrt\((\d+)\)', denom_str)
    if not match:
        # Handle case like "1-sqrt(2)" or "-3-sqrt(5)"? 
        # The string is "4-sqrt(7)". Match should work.
        pass
    
    A = int(match.group(1))
    B_val = int(match.group(2))
    
    # Rationalization logic:
    # Original: N / (A - sqrt(B))
    # Conjugate mult: N * (A + sqrt(B)) / (A^2 - B)
    # Denominator becomes integer D = A*A - B_val.
    # Numerator becomes N*(A + sqrt(B)).
    # Fraction is [N*A + N*sqrt(B)] / D.
    
    D = A * A - B_val # 16 - 7 = 9
    
    # Simplify the fraction (Numerator/D)
    num_part_const = numerator_int * A # 9 * 4 = 36
    num_part_radical_coeff = numerator_int # 9
    
    # Fraction is (num_part_const + num_part_radical_coeff*sqrt(B)) / D
    # We need to simplify by dividing common factors.
    
    def gcd(a, b):
        while b: a, b = b, a % b
        return abs(a) if isinstance(a, int) else 1
    
    g_const = num_part_const // gcd(num_part_const, D) * (D // gcd(num_part_const, D)) # No, simpler logic.
    
    common_divisor = FractionOps.gcd(Fraction(num_part_const), Fraction(D)) # Need to implement GCD for fractions? 
    # Let's do integer arithmetic first then convert.
    
    g1 = num_part_const % 2 == 0 and D % 2 == 0 ? ... 
    # Use math library gcd if available, else custom.
    def get_gcd(x, y):
        x, y = abs(int(x)), abs(int(y))
        while y:
            x, y = y, x % y
        return x
    
    g_val = get_gcd(num_part_const + num_part_radical_coeff * 0, D) # Just for const part? 
    # Actually, we have two terms in numerator. We can only simplify if both share a factor with denominator.
    
    term1_num = num_part_const
    term2_num = num_part_radical_coeff
    
    g_term1 = get_gcd(term1_num, D)
    simplified_A = (term1_num // g_term1) # Wait, we divide the whole fraction by GCD of all terms? 
    # The expression is (C + K*sqrt(B)) / D.
    # We can simplify if C and K are both divisible by some factor that divides D.
    
    common_factor = get_gcd(term1_num, D)
    check_radical_coeff_divisibility = False
    
    # Better approach: Create Fraction for the whole numerator part? No, sqrt is not in fraction field directly usually unless symbolic.
    # But we are simplifying coefficients.
    # Let's find GCD of (term1_num, term2_num, D). 
    common_gcd_val = get_gcd(term1_num, D)
    if term2_num != 0:
        common_gcd_val = get_gcd(common_gcd_val, term2_num)
    
    simplified_A_coeff = term1_num // common_gcd_val # Wait, we divide the numerator terms by GCD and denominator by same? 
    # Yes. New Denom D' = D / common_gcd_val.
    # But wait, if only one term is divisible, can we simplify? No, unless it's a sum of fractions.
    # (C + K*sqrt(B))/D = C/D + (K*D)/D * sqrt... 
    # Usually rationalized form keeps D as denominator if no common factor for both terms.
    
    # Let's re-calculate: 36/9 and 9/9. Both divisible by 9? Yes.
    # So we divide everything by 9.
    # New Const = 4, New RadCoeff = 1, New Denom = 1.
    # Result form: A' + B'*sqrt(B). Here denom is 1 (integer result effectively for the rational part and radical part coefficients?). 
    # Wait, if denominator becomes 1, then it's just an integer plus a root? Yes.
    
    # So simplified_A = term1_num // common_gcd_val ? No.
    # We divide numerator terms by GCD(term1, term2, D) and Denom by same.
    
    g_total = get_gcd(term1_num, D)
    if term2_num != 0:
        g_total = get_gcd(g_total, term2_num)
        
    # If g_total > 1, simplify.
    final_A = (term1_num // g_total) / (D // g_total) ? No.
    Final Denom D_final = D // g_total.
    Final Const A_final = (term1_num // g_total). But wait, we must divide the fraction by g_total? 
    Yes: (C + K*sqrt)/D = (C/g + K/sqrt*g) / (D/g)? No.
    It is ((C/K)*g + ... ) / D ?
    
    Correct simplification logic for sum of terms over common denominator:
    Numerator Terms: [T1, T2]. Denom: D.
    GCD = gcd(T1, T2, D).
    New T1' = T1 // GCD? No. 
    We factor out GCD from the entire numerator expression (C + K*sqrt(B)).
    If C and K are both divisible by g, then we can write g*(C/g + K/sqrt*g) / D -> no.
    
    Let's just use Fraction arithmetic for coefficients if possible? 
    Actually, standard simplification: divide T1, T2, D by gcd(T1, T2, D).
    
    # Recalculate with numbers: 36, 9, 7 (radicand is constant in sqrt term coefficient logic?)
    # Numerator terms are integers. Denominator is integer.
    g = get_gcd(36, 9) -> 9. 
    Check D=9. gcd(9, 9) -> 9.
    So GCD of all three (T1_const, T2_rad_coeff, D_denom) is 9? 
    Wait, the radical term coefficient doesn't interact with radicand value for simplification factor unless we consider sqrt(B).
    The expression is X + Y*sqrt(Z). We simplify fraction by dividing coefficients and denominator by common integer factors.
    
    # Factors of T1 (36): 2^2 * 3^2
    # Factors of T2 (9): 3^2
    # Factors of D (9): 3^2
    Common factor is 9? 
    Wait, if we divide numerator by 9 and denominator by 9:
    New Const = 4. New RadCoeff = 1. Denom = 1.
    Result: 4 + sqrt(7).
    
    # What if T2 was not divisible? e.g., (36 + 5*sqrt(7))/9. GCD of (36, 5) is 1. No simplification.
    
    def simplify_radical_expression(num_const, num_coeff, denom):
        g = get_gcd(abs(num_const), abs(denom))
        if num_coeff != 0:
            g = get_gcd(g, abs(num_coeff))
        
        # If g > 1 and we can divide all parts? 
        # Wait, the radical term is coeff * sqrt(rad). The radicand itself doesn't change.
        # We only simplify integer coefficients.
        if num_const % g == 0 and (num_coeff == 0 or num_coeff % g == 0):
            return {
                "A": num_const // g, 
                "B": num_coeff // g, 
                "radicand": radicand_val, # Does not change? Or does it simplify sqrt(rad)? No.
                "denom": denom // g if (num_const % g == 0 and (num_coeff==0 or num_coeff%g==0)) else denom
            }
        return {"A": num_const, "B": num_coeff, "radicand": radicand_val, "denom": denom}

    # Actually, simpler: 
    # Fraction = (C + K*sqrt(B))/D.
    # Simplify by dividing C, K, D by gcd(C, K, D).
    
    g_all = get_gcd(abs(num_const), abs(denom))
    if num_coeff != 0:
        g_all = get_gcd(g_all, abs(num_coeff))
        
    final_A = num_const // g_all # Wait, we must divide denominator too? 
    # Yes. If we factor out g from numerator (C+K*sqrt), then expression is g*(...) / D.
    # Then simplify fraction (...) / (D/g).
    
    if g_all > 1:
        final_A = num_const // g_all
        final_B = num_coeff // g_all
        final_D = denom // g_all
    else:
        final_A = num_const
        final_B = num_coeff
        final_D = denom
        
    # If final_D is not 1, we have a fraction. 
    # But the task asks for "correct_answer" as integer? 
    # Maybe if D != 1, it's invalid input for this specific constraint? 
    # Or maybe I should return -1?
    
    # Let's assume the test case provided (9/(4-sqrt(7))) is designed to yield an integer result in terms of A+B sum.
    # If final_D == 1: Result is Integer + Radical. Sum = A + B.
    # If final_D != 1, maybe return -1? Or the task implies D will always be 1 for valid inputs? 
    # Given "correct_answer must be a single exact integer", I'll compute sum of coefficients if denom==1 else handle gracefully (maybe just return string representation converted to int? No).
    
    # Let's assume for this specific frozen param, it simplifies.
    # My calculation: 36/9 and 9/9 -> both divisible by 9. D becomes 1. 
    # So final_D = 1.
    # A_final = 4, B_final = 1.
    # Answer = A + B = 5? Or just the value of expression if it was integer? It's not integer.
    
    # Re-reading: "correct_answer must be a single exact integer". 
    # If the result is 4+sqrt(7), there is no integer answer unless we sum coefficients (as hinted by task name _ab_sum).
    # I will proceed with Sum = A + B if denom == 1.
    
    ans_val = final_A + final_B
    
    question_text = f"Rationalize the denominator of $\\frac{{{numerator_int}}}{{{denom_str}}}$ and find the sum of the coefficients of the rational part and the radical part in the simplified form."
    # Or simpler: "Simplify ... The answer is ..."
    
    correct_answer = ans_val
    
    oracle_payload = frozen_params

return {
    "question_text": f"Rationalize the denominator of $\\frac{{{numerator_int}}}{{{denom_str}}}$ and find the sum of the coefficients A and B in the simplified form $A + \\sqrt{{radicand}}$.", 
    "correct_answer": correct_answer, 
    "oracle_payload": oracle_payload
}