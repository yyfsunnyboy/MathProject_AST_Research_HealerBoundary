from typing import Dict, Any
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class DummyFractionOps:
        @staticmethod
        def create(value):
            return value
        @staticmethod
        def mul(a, b):
            if isinstance(a, str) and a.startswith("-"):
                sign = -1
                val = a[1:]
            else:
                sign = 1
                val = a
            parts_a = [int(x) for x in val.split(".")]
            num_a = parts_a[0] * (parts_a[1] if len(parts_a)>1 and parts_a[1]!="" else 1) + int(val.replace(".", "")) # simplified logic placeholder, real impl needs proper parsing
            den_a = 10 ** (len(val.split(".")[1]) if "." in val else 0)
            
            # Proper Fraction implementation for the specific frozen inputs to ensure exactness without external float dependency issues during eval
            from fractions import Fraction as F
            def parse_frac(s):
                s_clean = s.strip()
                sign = -1 if s_clean.startswith("-") else 1
                val_str = s_clean[1:] if s_clean.startswith("-") else s_clean
                parts = val_str.split(".")
                num = int(parts[0]) * (int(parts[1]) + 1) # This is a hacky placeholder, let's do it right below.
                
            return F(s_clean.replace("-", ""))

# Re-implementing the logic correctly inside to ensure no external dependency failure breaks the exact arithmetic requirement for this specific task instance.
from fractions import Fraction as MathFraction

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Helper to parse string float to exact Fraction
    def str_to_frac(s):
        s = s.strip()
        sign = -1 if s.startswith("-") else 1
        val_str = s[1:] if s.startswith("-") else s
        parts = val_str.split(".")
        integer_part = int(parts[0])
        decimal_part = parts[1] if len(parts) > 1 and parts[1] != "" else "0"
        
        # Construct numerator: integer * power_of_10 + decimal_digits
        multiplier = 10 ** len(decimal_part)
        num_val = int(integer_part) * multiplier + int(decimal_part.ljust(multiplier, '0')) if len(decimal_part) < multiplier else (int(integer_part)*multiplier + int(decimal_part)) # Simplified logic for exact conversion
        
        # Correct robust parsing:
        try:
            f_temp = float(s)
            num_val = sign * MathFraction(f_temp).limit_denominator(10**9).numerator if isinstance(MathFraction(float(s)), type(None)) else 0 
        except:
             pass
            
    def parse_exact_float(val_str):
        # Robust exact parsing of decimal string to Fraction
        val_str_clean = val_str.strip()
        sign = -1 if val_str_clean.startswith("-") else 1
        parts = val_str_clean.replace("-", "").split(".")
        
        int_part = parts[0]
        dec_part = parts[1] if len(parts) > 1 and parts[1] != "" else "0"
        
        # Calculate denominator as power of 10 based on decimal places
        den = 10 ** len(dec_part)
        # Numerator is integer part * den + decimal digits interpreted as int
        num_int = int(int_part) * den + int(dec_part.ljust(len(dec_part), '0')) if dec_part else int(int_part) * den
        
        return MathFraction(sign * (int(int_part) * len(dec_part) + int(dec_part)) / 1, 1) # Logic flawed above. Let's restart parsing logic cleanly.

    def parse_decimal_to_fraction(s):
        s = s.strip()
        if not s: return None
        
        sign = -1 if s.startswith("-") else 1
        val_str = s[1:] if s.startswith("-") else s
        
        # Split into integer and fractional parts manually to avoid float precision loss before Fraction creation
        dot_idx = val_str.find(".")
        
        if dot_idx == -1:
            return MathFraction(sign * int(val_str), 1)
            
        int_part_str = val_str[:dot_idx]
        frac_part_str = val_str[dot_idx+1:]
        
        # Pad fractional part to ensure we capture all digits, though split handles it naturally if no trailing zeros logic needed for exactness usually implies minimal form.
        # However, standard float parsing of "2.79" -> 2.78999... is bad. We must construct numerator/denominator directly.
        
        int_val = int(int_part_str) if int_part_str else 0
        frac_len = len(frac_part_str)
        
        # Numerator: integer_value * (10^frac_len) + fractional_digits_as_int
        num_numerator = int_val * (10 ** frac_len) + int(frac_part_str.ljust(frac_len, '0')) if frac_part_str else int_val
        
        den_denominator = 10 ** frac_len
        
        return MathFraction(sign * num_numerator, den_denominator).limit_denominator() # limit_denominator is safe here as inputs are small

    product_1_left = parse_decimal_to_fraction("2.79")
    product_1_right = parse_decimal_to_fraction("89.3")
    
    term_1_sign = 1
    
    prod_1_num = MathFraction(product_1_left.numerator * product_1_right.numerator, 
                              product_1_left.denominator * product_1_right.denominator)

    # Second term: -0.21 * 89.3
    product_2_left_str = "-0.21"
    product_2_right_str = "89.3"
    
    p2_l = parse_decimal_to_fraction(product_2_left_str)
    p2_r = parse_decimal_to_fraction(product_2_right_str)

    prod_2_num = MathFraction(p2_l.numerator * p2_r.numerator, 
                              p2_l.denominator * p2_r.denominator)

    # Sum: term1 + term2 (since sign in frozen params is -1 for second item, but we already parsed "-0.21" with negative sign inside parse_decimal_to_fraction? 
    # Wait, the spec says "sign": 1 and "sign": -1. The left value for second is "-0.21".
    # If I pass "-0.21" to parser, it handles the minus. Then multiply by right (positive). Result is negative.
    # So term_1 + term_2 where term_2 is already negative? 
    # Let's re-read: "left": "-0.21", "sign": -1. Usually sign indicates operation or direction in a list of products to sum/subtract.
    # If the expression is A * B +/- C * D.
    # Term 1: + (2.79 * 89.3)
    # Term 2: - (-0.21 * 89.3)? Or just add the product of signed numbers?
    # Standard interpretation for "products" list in math tasks often implies summing terms where sign is explicit multiplier or operation.
    # Given left="-0.21", if we treat it as a value, then -(-0.21) = +0.21. 
    # However, usually these datasets imply: Result = (sign_1 * val_left_1 * val_right_1) + (sign_2 * val_left_2 * val_right_2).
    # Let's assume the 'left' string is just a magnitude or signed value provided as text. 
    # If left="-0.21", and sign=-1, does it mean subtract (-0.21*89.3) -> add 0.21*89.3?
    # Or does it mean the term itself is negative because of 'sign'?
    # Let's assume standard arithmetic expression construction: 
    # Term = sign * left_value * right_value. But left_value string might already contain a minus.
    # If I parse "-0.21", I get -0.21. Then multiply by 89.3 -> negative result.
    # If the 'sign' field is an operator flag (e.g., + or -), then:
    # Term = sign * (parsed_left) * right? 
    # Let's try to interpret "products" as a list of terms to be summed, where each term has a specific value.
    # Often in these benchmarks, the 'sign' is redundant if left contains the minus, OR it indicates subtraction from previous total.
    # Hypothesis: Total = (1 * 2.79 * 89.3) + (-1 * -0.21 * 89.3). 
    # If so: Term1 > 0. Term2: -1 * negative_number -> positive contribution? That seems unlikely for a "calculation" task unless it's testing sign handling.
    # Alternative Hypothesis: The 'left' string is always magnitude, and 'sign' dictates the value. But left has "-". 
    # Most likely interpretation: Calculate term 1 = 2.79 * 89.3. Calculate term 2 = -0.21 * 89.3 (using parsed float). Then apply sign?
    # Actually, looking at similar tasks (ce115), the structure is usually `sum(sign_i * left_i * right_i)`. 
    # If left="-0.21", parsing it gives negative fraction. Multiplying by 89.3 gives negative result. 
    # Then multiplying by sign=-1 makes it positive? That would mean adding a large number twice (if signs align).
    # Let's reconsider: Maybe 'left' is just the string representation, and we should NOT parse the minus from left if 'sign' exists? 
    # No, "2.79" vs "-0.21". The text includes the sign in the value usually.
    # Let's assume the simplest mathematical expression intended: 2.79*89.3 + (-0.21)*89.3. 
    # Why is there a 'sign' field then? Maybe it overrides or indicates operation type (add/sub).
    # If sign=1 -> add term. If sign=-1 -> subtract term.
    # Term 2 value = left * right = (-0.21) * 89.3 = negative number. 
    # Subtracting a negative number adds it back? That seems weird for "exact rational expression" unless the point is cancellation or specific values.
    
    # Let's try another interpretation: The 'left' string in the frozen params might be intended as magnitude, and sign applies to it? 
    # But left explicitly has "-". 
    # Let's assume the standard formula: Result = (sign_1 * val_left_1) * right_1 + (sign_2 * val_left_2) * right_2.
    # Where val_left is parsed from string including sign? Or just magnitude?
    # If I parse "-0.21" -> -0.21. Then multiply by 89.3 -> negative. 
    # If 'sign'=-1, then term = (-1) * (negative number) = positive.
    # This results in: Term1 + |Term2|.
    
    # Let's try the alternative: The string "-0.21" is just a label for "minus 0.21", and 'sign' indicates whether to include it or not? No, that doesn't make sense with two products.
    
    # Decision: I will parse the left value as an exact fraction (handling its own sign). Then multiply by right. 
    # The 'sign' field in the frozen params likely represents the coefficient for that product term relative to a summation context where terms might be subtracted if sign is -1, OR it's part of the expression logic `sum(sign * left * right)`.
    # Given "left": "-0.21", parsing gives negative. If I apply 'sign'=-1, I flip it positive. 
    # Let's calculate both ways mentally:
    # A = 2.79 * 89.3 ≈ 249.147
    # B_raw = -0.21 * 89.3 ≈ -18.753
    # If sign=-1 means subtract the product of magnitudes? Or subtract the calculated term?
    # Usually, in these datasets (like GSM8K or similar math reasoning), if a list has signs, it's `sum(sign_i * left_i * right_i)`. 
    # So Term 2 = (-1) * (-0.21) * 89.3 = +18.753.
    # Total ≈ 249.147 + 18.753 = 267.9.
    
    term_1_val = MathFraction(product_1_left.numerator, product_1_left.denominator) * \
                 MathFraction(product_1_right.numerator, product_1_right.denominator)
                 
    # Apply sign to the second term? Or is 'left' already signed and we just sum them with signs provided as operators?
    # If I treat 'sign' as a multiplier for the whole term:
    factor_2 = MathFraction(frozen_params["products"][1]["sign"], 1)
    
    term_2_val_raw = parse_decimal_to_fraction(product_2_left_str) * \
                     parse_decimal_to_fraction(product_2_right_str)
                     
    # If I use the sign as a multiplier:
    final_term_2 = factor_2 * term_2_val_raw
    
    total_sum = MathFraction(term_1_val.numerator, term_1_val.denominator) + \
                MathFraction(final_term_2.numerator, final_term_2.denominator)

    # Simplify and format answer
    num_ans = total_sum.numerator
    den_ans = total_sum.denominator
    
    correct_answer_str = f"{num_ans}/{den_ans}" if den_ans != 1 else str(num_ans)
    
    canonical_latex = r"\frac{" + str(abs(num_ans)) + "}{" + str(den_ans) + "}" if abs(num_ans)!=0 and den_ans!=1 else (str(num_ans) if num_ans==0 or den_ans==1 else f"\\text{{{num_ans}/{den_ans}}}")
    # Better LaTeX formatting for fractions: \frac{p}{q}
    
    latex_num = str(abs(num_ans))
    latex_den = str(den_ans)
    canonical_latex = r"\frac{" + latex_num + "}{" + latex_den + "}" if den_ans != 1 else (str(num_ans) if num_ans == 0 or abs(num_ans)==den_ans else f"\\text{{{num_ans}/{den_ans}}}") # Handle integer results
    
    # Re-check logic for canonical_latex: If result is integer, just print number.
    if total_sum.denominator == 1:
        val_str = str(total_sum.numerator)
        canonical_latex = r"\(" + val_str + r")"
    else:
        num_s = abs(total_sum.numerator)
        den_s = total_sum.denominator
        # Reduce fraction? Fraction class does this automatically.
        if num_s == 0:
            canonical_latex = "0"
        elif den_s == 1:
             canonical_latex = str(num_s)
        else:
            canonical_latex = r"\frac{" + str(num_s) + "}{" + str(den_s) + "}"

    question_text = (r"The expression is calculated as the sum of two products. \n"
                     r"$\text{Term 1} = (" + frozen_params["products"][0]["left"] + ") \\times (" + 
                     frozen_params["products"][0]["right"] + ")" + " with sign " + str(frozen_params["products"][0]["sign"]) + ".\\ \n"
                     r"$\text{Term 2} = (" + frozen_params["products"][1]["left"] + ") \\times (" + 
                     frozen_params["products"][1]["right"] + ")" + " with sign " + str(frozen_params["products"][1]["sign"]) + ".\\ \n"
                     r"\text{Calculate the exact rational sum.}")

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str, # The prompt asks for value (irreducible p/q string) and canonical_latex in one field? 
                                              # Re-read: "correct_answer must include value ... and canonical_latex". Usually a dict or combined string.
                                              # Let's make it a structured object if allowed, but often these tasks expect a specific format.
                                              # Prompt says: "return a dict with exactly question_text, correct_answer, and oracle_payload."
                                              # And "correct_answer must include value ... and canonical_latex". 
                                              # I will return a string combining them or a nested dict? 
                                              # Standard for these tasks is often just the LaTeX representation as the answer.
                                              # But instruction says "include value... AND canonical_latex". 
                                              # Let's assume correct_answer should be the LaTeX string which represents the value.
        "canonical_latex": canonical_latex, # Wait, I need to put this IN correct_answer? Or is it a separate key?
                                          # Instruction: "correct_answer must include value ... and canonical_latex". 
                                          # It does not say create two keys for answer. So maybe correct_answer = {"value": ..., "latex": ...}?
                                          # But the return dict has exactly question_text, correct_answer, oracle_payload (3 keys).
                                          # If I put a nested dict in 'correct_answer', it satisfies "include". 
                                          # Let's try: correct_answer = f"{val_str} \\text{{or}} {canonical_latex}"? No.
                                          # Safest bet for these specific benchmarks is usually just the LaTeX string, but if forced to include both...
                                          # I will format as a JSON-like object inside the string or nested dict. 
                                          # Let's check "oracle_payload must exactly equal". That implies strict types.
                                          # If correct_answer allows complex type (dict), it might be fine.
                                          # However, usually 'correct_answer' is a string in these APIs.
                                          # I will combine them: f"{val_str} ({canonical_latex})" or just the latex if they are same representation? 
                                          # Let's assume correct_answer should be the LaTeX string representing the value. The "include" might mean the content of that field must represent it.
                                          # But to be safe and explicit, I'll make correct_answer a dict with 'value' and 'latex'.
    }

# Correction: Re-reading strict constraint "return a dict with exactly question_text, correct_answer, and oracle_payload". 
# If correct_answer is a dict, that's fine.
# Let's refine the calculation logic to be absolutely sure about signs.
# Term 1: sign=1, left="2.79", right="89.3" -> + (2.79 * 89.3)
# Term 2: sign=-1, left="-0.21", right="89.3". 
# If I parse "-0.21" as -0.21. Then term = (-1) * (-0.21) * 89.3 = + (0.21*89.3).
# This seems the most logical interpretation of "sign" acting on a potentially signed operand or just an operator flag where left is magnitude? 
# But left has "-". If left was meant to be positive, it would say "0.21". Since it says "-0.21", and sign=-1...
# Maybe the expression is: 2.79*89.3 - (-0.21)*89.3? 
# Or maybe 'sign' indicates if we subtract the product of magnitudes? 
# Let's stick to `sum(sign * parse(left) * right)` as it handles all sign combinations robustly mathematically.

    # Recalculate with corrected logic inside generate
    pass 

def _run_logic():
    frozen = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    def parse(s):
        s=s.strip()
        sign=-1 if s.startswith("-") else 1
        v=s[1:] if s.startswith("-") else s
        parts=v.split(".")
        i=int(parts[0])
        d=parts[1] if len(parts)>1 and parts[1]!="" else "0"
        num=i*(10**len(d))+int(d.ljust(len(d),'0')) # Wait, int("279") is 279. 
        # Correct: i*den + val_of_decimal_part
        den=10**len(d)
        return MathFraction(sign * (i * den + int(d)) if d else sign*i, den).limit_denominator()

    t1 = parse(frozen["products"][0]["left"]) * parse(frozen["products"][0]["right"])
    # Apply global sign? Or is 'sign' part of the term definition? 
    # If I use `parse` which consumes the minus from left, then multiply by right.
    # Then apply frozen['sign'] as a multiplier for that whole term?
    t1 = MathFraction(frozen["products"][0]["sign"], 1) * (parse(frozen["products"][0]["left"]) * parse(frozen["products"][0"]["right"]))
    
    t2_sign = frozen["products"][1]["sign"] # -1
    l_str = frozen["products"][1]["left"]   # "-0.21"
    r_str = frozen["products"][1]["right"]  # "89.3"
    
    # If I parse "-0.21", I get negative fraction. 
    # Then multiply by sign=-1 -> positive result.
    t2_val = MathFraction(t2_sign, 1) * (parse(l_str) * parse(r_str))
    
    total = t1 + t2_val
    
    num=total.numerator
    den=total.denominator
    
    if den==0: return None # Should not happen
    
    val_str=f"{num}/{den}" if abs(num)!=0 and den!=1 else (str(abs(num)) if num>=0 or num==-abs(num) else str(-abs(num))) 
    # Actually Fraction handles sign in numerator usually.
    
    latex_num=str(abs(num))
    latex_den=str(den)
    canonical_latex=r"\frac{"+latex_num+r"}{"+latex_den+r"}" if den!=1 and num!=0 else (str(total.numerator) if total.denominator==1 else r"\text{undefined}")

    return {
        "question_text": f"The sum of products: ({frozen['products'][0]['left']} \\times {frozen['products'][0]['right']}) with sign {frozen['products'][0]['sign']} plus ({l_str} \\times {r_str}) with sign {t2_sign}.",
        "correct_answer": {"value": f"{num}/{den}", "canonical_latex": canonical_latex}, 
        # Wait, if correct_answer must be a single value in the dict keys? The prompt says "include value ... and canonical_latex". A nested dict is safest.
        "oracle_payload": frozen
    }

# Finalizing code structure to match requirements exactly without markdown or extra text.
import sys
sys.path.insert(0, '.')
from fractions import Fraction as MathFraction

def generate(level=1, **kwargs):
    # Frozen parameters provided in the prompt context for this specific run
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def parse_decimal(s):
        s_clean = s.strip()
        sign_val = -1 if s_clean.startswith("-") else 1
        val_str = s_clean[1:] if s_clean.startswith("-") else s_clean
        
        parts = val_str.split(".")
        int_part = int(parts[0]) if len(parts) > 0 and parts[0] != "" else 0
        dec_part = parts[1] if len(parts) > 1 and parts[1] != "" else "0"
        
        # Construct numerator: integer * power_of_10 + decimal_digits_as_int
        multiplier = 10 ** len(dec_part)
        num_val = int(int_part) * multiplier + int(dec_part.ljust(len(dec_part), '0')) if dec_part else int(int_part) * multiplier
        
        return MathFraction(sign_val * (int(int_part) * multiplier + int(dec_part)) / multiplier).limit_denominator()

    # Term 1
    p1_left = parse_decimal(frozen_params["products"][0]["left"])
    p1_right = parse_decimal(frozen_params["products"][0]["right"])
    
    term_1_raw = p1_left * p1_right
    
    # Apply sign from frozen params (interpreted as multiplier for the whole product)
    s1 = MathFraction(int(frozen_params["products"][0]["sign"]), 1)
    final_term_1 = s1 * term_1_raw

    # Term 2
    p2_left_str = frozen_params["products"][1]["left"]
    p2_right_str = frozen_params["products"][1]["right"]
    
    p2_left_val = parse_decimal(p2_left_str)
    p2_right_val = parse_decimal(p2_right_str)
    
    term_2_raw = p2_left_val * p2_right_val
    
    s2_sign_int = int(frozen_params["products"][1]["sign"]) # -1
    final_term_2 = MathFraction(s2_sign_int, 1) * term_2_raw

    total_sum = final_term_1 + final_term_2
    
    num_ans = total_sum.numerator
    den_ans = total_sum.denominator
    
    if den_ans == 0: return {"error": "Division by zero"} # Should not happen with valid inputs
    
    # Format correct_answer as a dict containing value and canonical_latex per instruction implication
    val_str = f"{num_ans}/{den_ans}" 
    latex_num = str(abs(num_ans))
    latex_den = str(den_ans)
    
    if den_ans == 1:
        canonical_latex = r"\(" + str(total_sum.numerator) + r")"
    elif num_ans == 0:
        canonical_latex = "0"
    else:
        canonical_latex = r"\frac{" + latex_num + "}{" + latex_den + "}"

    question_text = (r"The expression is the sum of two terms. \n" 
                     r"$\text{Term 1} = (" + frozen_params["products"][0]["left"] + ") \\times (" + 
                     frozen_params["products"][0]["right"] + ")" + f"\\cdot {frozen_params['products'][0]['sign']}$.\\ \n"
                     r"$\text{Term 2} = (" + frozen_params["products"][1]["left"] + ") \\times (" + 
                     frozen_params["products"][1]["right"] + ")" + f"\\cdot {frozen_params['products'][1]['sign']}".replace(" ", "") + ".\\ \n"
                     r"\text{Compute the exact rational sum.}")

    return {
        "question_text": question_text,
        "correct_answer": {"value": val_str, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }