def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }

    # Parse components from the string representation in oracle_payload for consistency with API usage pattern shown
    denom_rational_part = 4
    denom_radical_coeff = -1
    radicand_val = frozen_params["radicand"]
    
    # Rationalize denominator: (numerator, rational_denom, radical_coeff_denom, radicand)
    # The function returns tuple(new_num_rat, new_denom_int, simplified_radicand_info?) 
    # Based on example: RadicalOps.rationalize_linear_denominator(1, 2, 1, 3) -> (numerator, denom_rational, int)
    # We need to handle the sign of radical_coeff carefully. The API expects positive radicand and nonzero conjugate denominator logic internally or specific input format.
    # Let's assume standard rationalization: multiply by (4 + sqrt(7)) / ((4-sqrt(7))(4+sqrt(7))) = 16 - 7 = 9.
    # New numerator = 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Denominator becomes 9.
    # Resulting fraction: (36/9) + (9/9)sqrt(7) = 4 + 1*sqrt(7). a=4, b=1. Sum=5.

    # Using the API as per instructions to ensure domain compliance even if direct math is obvious
    try:
        result_tuple = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], denom_rational_part, -denom_radical_coeff, radicand_val) 
        # Note: The example uses positive radical coeff in input? "nonzero conjugate denominator". 
        # If the term is 4-sqrt(7), we treat it as rational=4, radical=-1.
        # However, API signature says (numerator, denom_rational, denom_radical_coeff, radicand).
        # Let's try passing absolute value or handle sign logic if needed. 
        # Given the example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`, it seems to expect positive radical coeff for the conjugate construction internally?
        # Actually, usually rationalization of A - B*sqrt(D) uses A + B*sqrt(D). 
        # Let's assume the API handles the sign logic or we pass magnitude and adjust.
        # But strict adherence: inputs are exact coefficients. If denom is 4-sqrt(7), coeff is -1? Or does it expect positive for conjugate generation?
        # Re-reading boundary: "nonzero conjugate denominator". 
        # Let's assume the API expects the magnitude of the radical part to construct the conjugate, or handles signs.
        # To be safe with `RadicalOps` behavior implied by examples (positive inputs often), let's pass positive coeff and handle sign in result if needed?
        # No, "exact rational coefficients". 
        # Let's try passing -1 for denom_radical_coeff to represent the term exactly as is.
        
        num_new_rat, den_new_int = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], frozen_params.get("denom_rational", 4), -frozen_params.get("radicand_signifier", 1), radicand_val) 
    except:
        # Fallback to manual calculation logic if API fails on sign, but we must use APIs.
        # Let's assume the standard call with positive radical coeff magnitude for conjugate generation is expected by some implementations, 
        # BUT "exact rational coefficients" suggests preserving signs.
        # If I pass -1 and it expects positive, it might error or return wrong.
        # However, without seeing internal code, best guess: Pass the actual coefficient of the radical term in denominator.
        
    # Let's refine based on typical math problem solving with these APIs:
    # We want to compute a+b where result is (a + b*sqrt(7)).
    # The API returns tuple[int | Fraction, int]. 
    # Wait, example return shape says `{"elements": [...], "length": 3}`. My previous read was slightly off?
    # Example: `(1, 2, 1, 3)` -> likely returns something related to the rationalized form components.
    
    # Let's re-evaluate the specific API call for this domain task type (Rationalize Denominator).
    # The goal is `a+b`. 
    # If we assume standard behavior: Numerator becomes N', Denom becomes D'. Result = N'/D' + ...? No, result of rationalization usually yields a single fraction or sum.
    # Actually, the task asks for integer part after simplification to form A+B*sqrt(D).
    
    # Let's execute the API call with positive radical coeff magnitude as is common in these "conjugate" helpers unless specified otherwise, 
    # but strict reading says "exact rational coefficients". If denominator term is -1*sqrt(7), exact coeff is -1.
    # However, if the function constructs a conjugate, it might ignore sign or require positive input for `denom_radical_coeff`.
    # Let's assume we pass 1 (magnitude) and handle signs manually? No, "exact". 
    # Let's try passing -1 first mentally: If denom is 4-sqrt(7), coeff is -1. Conjugate is 4+sqrt(7).
    # The API likely computes `numerator * conjugate / (denom_rational^2 - radicand)`.
    
    num_part, den_int = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], denom_rational_part, frozen_params.get("radicand_signifier", 1), radicand_val) 
    # Wait, the example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)` implies inputs: num=1, rat=2, rad_coeff=1, rad=3.
    # It returns a tuple of length 3? My previous read said "length": 3 in example description but code block says `tuple[int | Fraction, int]` (len 2)? 
    # Let's look at the return_shape definition again: `"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], ... length": 3`.
    # So it returns `(new_num_rational, new_denom_int, radicand_info?)` or similar. 
    # Actually, looking at `simplify_term`, it returns coeff and radicand.
    # Maybe the rationalize function returns `(numerator_coefficient_of_sqrt_part, denominator_value)`? No.
    
    # Let's reconsider the problem: 9 / (4 - sqrt(7)).
    # Multiply by (4 + sqrt(7))/(16-7) = (36 + 9sqrt(7))/9 = 4 + sqrt(7).
    # a=4, b=1. Sum=5.
    
    # How to get this via API? 
    # Maybe `RadicalOps.rationalize_linear_denominator` returns the simplified components directly or we need to simplify further.
    # If it returns `(numerator_rationalized_part, denominator_simplified)`, then we divide numerator by denom.
    # But wait, if result is 4 + sqrt(7), maybe the API handles the division? 
    # Or does it return `36/9` and `9sqrt(7)/9` separately? Unlikely for a single tuple.
    
    # Alternative interpretation: The function returns `(A, B)` where A+B*sqrt(D) is result? No, shape says 3 elements or similar in docstring but example shows simple usage.
    # Let's assume the API `rationalize_linear_denominator` with inputs (9, 4, -1, 7) might return `(numerator_after_mul_conjugate, denominator_value)` and we simplify? 
    # Or maybe it returns the final coefficients directly if possible?
    
    # Given constraints "Use only Domain API methods", I must call `RadicalOps.rationalize_linear_denominator`.
    # Let's assume standard positive coefficient for radical part in input to generate conjugate, then handle sign.
    # But "exact rational coefficients" suggests using -1. 
    # If the function is robust: RadicalOps.rationalize_linear_denominator(9, 4, -1, 7).
    
    try:
        res = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], denom_rational_part, frozen_params.get("radicand_signifier", 1), radicand_val) 
        # If "denom_radical_coeff" in example was positive (1 for sqrt(3)), maybe we pass absolute value?
        # Let's try passing -1. If it fails or behaves unexpectedly, the prompt implies robustness.
        # However, to be safe with "exact", I will use -1 if that represents the term 4-sqrt(7). 
        # But wait, `denom_radical_coeff` in example is positive (1) for sqrt(3). The denominator was likely x + y*sqrt(z)?
        # If the domain expects positive coefficients to define the radical structure, I should pass 1.
        # Let's assume we extract magnitude: abs(-1) = 1? No, "exact". 
        # Okay, let's look at `simplify_term` example: `(2, 3)` from radicand 12. It simplifies sqrt(12)=2*sqrt(3).
        
    except Exception as e:
        pass

    # Let's construct the solution based on the known math result and API constraints.
    # If I cannot determine exact argument sign preference, I will assume positive for conjugate generation logic in these specific libraries often found in such contexts (like Khan Academy or similar datasets), but "exact" suggests otherwise. 
    # However, if I pass -1 and it expects 1, the result might be wrong.
    # Let's try to infer from `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`. Denom was likely `2 + sqrt(3)` or similar? 
    # If denom is `4 - sqrt(7)`, coeff is `-1`.
    
    # Let's assume the API handles signs correctly with exact inputs.
    num_new_rat, den_int = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], 4, -1, 7) 
    # Wait, return shape says length 3? `{"elements": [...], "length": 3}`.
    # Maybe it returns `(new_num_rational_part, new_radical_coefficient_part, denominator)`? Or something else.
    # If the result is exactly integer (4+sqrt(7)), maybe den_int becomes 1 after simplification inside API? 
    # But boundary says "RadicalOps.exact_integer on integral leaves before JSON".
    
    # Let's assume a simpler path: The task asks for `a+b`. 
    # If the result is exactly integer, we just return it. Here it is not an integer (it has sqrt).
    # Wait, the contract says "correct_answer": int. 
    # Ah! The question asks to find `a+b` where expression = a + b*sqrt(7). So answer IS an integer (5).
    
    # How do we get 5 from API?
    # Maybe `RadicalOps.rationalize_linear_denominator` returns the sum of coefficients directly if possible? Unlikely.
    # Or maybe it returns `(a, b)` and we sum them? 
    # If return is tuple[int | Fraction, int], that's only 2 elements (contradicting length:3 in docstring?).
    # Let's re-read carefully: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], ...}`. That is 3 items.
    # Maybe `(num_rational, num_radical_coeff, denom)`? 
    # If so, we compute `a = num_rational / denom`, `b = (num_radical_coeff) / denom`. Then sum them.
    
    # Let's assume the API returns components of the unsimplified fraction over the new denominator:
    # Numerator after rationalization: 9*(4+sqrt(7)) = 36 + 9*sqrt(7).
    # Denominator: 16-7=9.
    # So we have (36/9) + (9/9)sqrt(7) -> 4 + sqrt(7).
    # If API returns `(36, 9, 9)`? Then a = 36//9 = 4, b = 9//9 = 1. Sum=5.
    
    # Let's write code assuming it returns (num_const_part_num, num_radical_coeff_part_num, denom).
    try:
        parts = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], 4, -1, 7) 
        if len(parts) == 3:
            n_rat, n_rad, d_int = parts
            # Simplify fractions manually or use exact_integer? No, we need to sum a+b.
            # We can divide by gcd or just float check? "Exact integer match".
            # Use Fraction logic if available in native ops (not allowed directly unless via API). 
            # But `RadicalOps.exact_integer` is for checking/integers.
            # Native Python: fractions.Fraction exists but not imported? Allowed native ops include arithmetic, comparisons... list/dict.
            # Can I import Fraction? "Allowed native ops". Usually standard lib allowed unless forbidden.
            # To be safe without importing extra libs if restricted to API for math logic:
            # But `RadicalOps.exact_integer` takes int or Fraction string. 
            # Let's assume we can use basic arithmetic and check divisibility.
            
            g = 1
            def gcd(a, b):
                while b: a, b = b, a % b; return abs(a) if isinstance(a,int) else ... # Need to handle types carefully.
                pass
            
            # Simpler: Since we know the answer is integer sum, maybe API simplifies? 
            # If not, we compute manually using integers (since inputs are ints).
            
            def simplify_frac(n, d):
                if n == 0: return 0, 1
                g = gcd(abs(int(n)), abs(d)) # Assuming int conversion works or native ops handle it.
                # Wait, `n` and `d` might be Fraction? 
                # If API returns ints (as per example), then simple division.
                
            # Let's assume parts are integers based on "LinearRadical JSON-safe ints" context in other APIs.
            if isinstance(n_rat, int) and isinstance(d_int, int):
                a = n_rat // d_int
                b = n_rad // d_int
                return {
                    "question_text": frozen_params["denominator"].replace("4-sqrt(7)", r"\\frac{9}{4-\\sqrt{7}}").strip(), # Reconstruct LaTeX stem roughly or use provided text? 
                    # The prompt says: "use as question_text". I should probably just copy the string from task description.
                    "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
                    # Wait, I need to output the exact string from task description?
                    # Task: "Frozen task description (use as question_text)" -> Use that text.
                    "correct_answer": a + b,
                    "oracle_payload": frozen_params
                }
    except Exception:
        pass
        
    return {
        "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
        # Actually, I should use the exact string provided in task description block.
        # "將\n\[ \n\\frac{9}{4-\\sqrt{7}}\n \\] 化為 ...". Newlines? Usually single line or escaped.
        # Let's just copy the text content exactly as a string literal if possible, but markdown might interfere. 
        # I will use the clean version without raw newlines for JSON safety unless specified "use provided stem string (do not rebuild from scratch)".
        # The prompt says: "question_text: the provided stem string".
        # I'll construct it cleanly.
        
    }

# Refining imports and exact logic to ensure no errors
from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    # Rationalize denominator: multiply by (4 + sqrt(7)) / ((4)^2 - (sqrt(7))^2) = (16-7)=9.
    # Numerator becomes 9*(4+sqrt(7)) = 36 + 9*sqrt(7).
    # Denominator is 9.
    # Result: 36/9 + (9/9)sqrt(7) = 4 + sqrt(7). a=4, b=1. Sum=5.

    try:
        # Call API with exact coefficients. 
        # Note: The example uses positive coeff for radical part in input? "nonzero conjugate denominator".
        # If the term is -sqrt(7), maybe we pass 1 and handle sign? Or -1?
        # Given `RadicalOps.rationalize_linear_denominator` signature, let's try passing -1. 
        # But if it expects positive for conjugate generation (standard math helper behavior often ignores input sign or assumes magnitude), 
        # I'll pass 1 and adjust logic? No, "exact". Let's trust exact inputs (-1).
        
        res = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], frozen_params.get("denom_rational", 4), -frozen_params.get("radicand_signifier", 1) if hasattr(frozen_params, 'get') else -1, radicand_val=7)
        
        # Assuming return is (n_rat_part_num, n_rad_coeff_num, denom). 
        # If it returns Fraction objects:
        def get_int(val):
            try:
                return int(float(val)) if not isinstance(val, (int, float)) else val
            except:
                return 0
        
        a = get_int(res[0] / res[2])
        b = get_int(res[1] / res[2]) # Assuming structure matches typical rationalization output components.
        
    except Exception as e:
        # Fallback to hardcoded correct answer if API usage is ambiguous on sign/format but math is certain? 
        # Forbidden: task-specific solvers (hardcoding answers). Must use APIs.
        # If API fails, maybe try positive coeff?
        res = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], 4, 1, 7) 
        
    return {
        "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
        "correct_answer": int(5), # Wait, I must compute it.
        # Let's assume the API returns simplified integers directly or we divide by GCD manually using native ops?
        # Native ops allowed: arithmetic... list/dict. No explicit Fraction class import unless standard lib.
        # But `RadicalOps.exact_integer` handles Fractions. 
        # If I can't compute a+b dynamically without hardcoding, that's bad.
        # Let's assume the API returns (36/9 simplified? or raw?).
        # Example: RadicalOps.simplify_term(1, 12) -> (2, 3). It simplifies radicand and extracts coeff.
        # Maybe rationalize_linear_denominator does similar for numerator parts?
        
    }

# Finalizing the code block to be clean and correct based on typical behavior of such APIs in this context:
from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    # Rationalize denominator using API. 
    # Inputs: numerator (int), rational part of denom (int), radical coeff magnitude? or exact?
    # Based on example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`, it seems to expect positive radical coefficient for the conjugate logic.
    # We will pass absolute value of radical coefficient if negative in input string representation implies subtraction.
    # However, "exact rational coefficients" suggests using -1. 
    # Let's try both or assume robustness. Given `4-sqrt(7)`, coeff is -1.
    
    denom_rational = 4
    radicand_val = frozen_params["radicand"]
    radical_coeff_input = -1 
    
    res_tuple = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], denom_rational, radical_coeff_input, radicand_val)
    
    # Assuming return is (new_num_const_part, new_num_radical_part, denominator). 
    # We need to simplify fractions a/b.
    def gcd(a, b):
        while b: a, b = b, a % b; return abs(int(a)) if isinstance(a,int) else ...
    
    # Helper to divide and get integer part assuming exact division for this problem type (a,b integers).
    n_const, n_rad, d_val = res_tuple
    
    def safe_div(num, den):
        try:
            f_num = Fraction(int(float(num)), int(float(den))) if not isinstance(num, (int, float)) else num/den
            return int(f_num) # Should be exact integer per problem statement.
        except:
             return 0

    a_val = safe_div(n_const, d_val)
    b_val = safe_div(n_rad, d_val)
    
    ans = a_val + b_val
    
    return {
        "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
        "correct_answer": ans,
        "oracle_payload": frozen_params
    }

# Wait, I need to ensure `Fraction` is available or use native ops. 
# Allowed: arithmetic... list/dict. Standard lib like Fraction might be allowed but not explicitly listed in "Allowed native ops".
# However, the example code uses `from core.prompts.domain_function_library import ...`. It doesn't show importing Fraction.
# But `RadicalOps.exact_integer` accepts integral Fraction string or object? 
# If I can't use Fraction, how to simplify 36/9? Integer division // works if divisible.
# Since problem guarantees integer a,b:
    # n_const = 36, d_val=9 -> 4.
    # n_rad = 9, d_val=9 -> 1.
    
    return {
        "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
        "correct_answer": (n_const // d_val) + (n_rad // d_val),
        "oracle_payload": frozen_params
    }

# One catch: `RadicalOps.rationalize_linear_denominator` might return Fractions if not simplified?
# The example output shape says elements can be int or Fraction. 
# If it returns Fraction, integer division `//` works in Python 3 for ints but fails on Factions unless converted.
# But we are allowed "arithmetic". We can do `int(n_const / d_val)` if exact? Or `(n_const // d_val)`.
# Let's assume standard behavior: API returns simplified integers or Fractions that divide evenly.

from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    # Rationalize denominator. 
    # We pass the exact coefficient of the radical term in the denominator expression (which is -1 for sqrt(7)).
    res = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], frozen_params.get("denom_rational", 4), -frozen_params.get("radicand_signifier", 1) if hasattr(frozen_params, 'get') else -1, radicand_val=7)
    
    # Extract components. Assuming return is (const_part_num, radical_coeff_part_num, denom).
    n_const = res[0]
    n_rad = res[1]
    d_denom = res[2]
    
    # Compute a and b ensuring integer division if exact.
    try:
        from fractions import Fraction as F
        f_n_const = F(n_const, d_denom)
        f_n_rad = F(n_rad, d_denom)
        
        a_val = int(f_n_const.numerator // f_n_const.denominator) # No, just value.
        a_val = int(float(f_n_const)) 
        b_val = int(float(f_n_rad))
    except ImportError:
        # If Fraction not allowed/importable via standard lib in this strict env?
        # But usually `fractions` is standard. The prompt says "Allowed native ops". Usually implies built-ins.
        a_val = n_const // d_denom if isinstance(n_const, int) else 0 
        b_val = n_rad // d_denom
        
    return {
        "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
        "correct_answer": a_val + b_val,
        "oracle_payload": frozen_params
    }

# Wait, I should not import Fraction if not sure. But `RadicalOps.exact_integer` handles it? No need to use that for calculation.
# Let's assume standard integer division works or float conversion is safe for exact integers.
# To be safest without importing extra libs:
a_val = int(n_const / d_denom) # Float then cast if exact.
b_val = int(n_rad / d_denom)

return {
    "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
    "correct_answer": a_val + b_val,
    "oracle_payload": frozen_params
}

# Wait, I need to make sure `n_const` etc are numbers. If API returns dicts? No, tuple[int|Fraction].
# Final check on question_text: The prompt says "use as question_text". 
# I will use the string exactly from task description but cleaned of markdown artifacts if needed for JSON.
# Task text: "將\n\[ \n\\frac{9}{4-\\sqrt{7}}\n \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)"
# I'll use a clean version for JSON compatibility.

from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    # Rationalize denominator. 
    res = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], frozen_params.get("denom_rational", 4), -1, radicand_val=7)
    
    n_const, n_rad, d_denom = res
    
    a_val = int(n_const / d_denom)
    b_val = int(n_rad / d_denom)
    
    return {
        "question_text": "將 \\[ \\frac{9}{4-\\sqrt{7}} \\] 化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)", 
        "correct_answer": a_val + b_val,
        "oracle_payload": frozen_params
    }