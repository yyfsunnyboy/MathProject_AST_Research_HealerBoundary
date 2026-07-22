from functools import partial
import json
from typing import Dict, Any, Union

# Mocking the required external module structure as per instructions
class _MockFraction:
    def __init__(self, num=0, den=1):
        self.num = num
        self.den = den
    
    @property
    def value(self) -> str:
        if self.den == 1:
            return f"{self.num}"
        common = abs(self.gcd())
        s_num = (self.num // common) * (-1)**(1 if self.num < 0 else 0) # Simplify sign logic manually for string rep
        simplified_num = self.num // common
        simplified_den = self.den // common
        
        # Handle negative denominator convention: move minus to numerator
        if simplified_den < 0:
            simplified_num *= -1
            simplified_den *= -1
            
        return f"{simplified_num}/{simplified_den}"

    def gcd(self):
        import math
        return abs(math.gcd(self.num, self.den))

class FractionOps:
    @staticmethod
    def create(value_str: str) -> _MockFraction:
        # Parse string like "2.79" or "-0.21" into exact fraction logic manually to avoid float issues in mock
        if '/' in value_str:
            parts = value_str.split('/')
            num, den = int(parts[0]), 1 if len(parts) == 1 else int(parts[1]) # Simplified parsing for demo
            return _MockFraction(num, den)
        
        sign = -1 if value_str.startswith('-') else 1
        val_part = abs(float(value_str))
        s_num, s_den = FractionOps._to_fraction(val_part)
        num = sign * s_num
        
        # Simplify immediately to ensure irreducible p/q string in create? 
        # The spec says correct_answer must be irreducible. Let's simplify here for robustness.
        common = abs(num.gcd()) if isinstance(num, _MockFraction) else 1
        simplified_num = num // common
        simplified_den = den // common
        
        return _MockFraction(simplified_num, simplified_den)

    @staticmethod
    def mul(a: Union[str, '_MockFraction'], b: Union[str, '_MockFraction']) -> str:
        # Convert inputs to Fraction objects if strings
        fa = a if isinstance(a, _MockFraction) else FractionOps.create(str(a))
        fb = b if isinstance(b, _MockFraction) else FractionOps.create(str(b))
        
        res_num = fa.num * fb.num
        res_den = fa.den * fb.den
        
        # Simplify result for canonical representation in oracle_payload? 
        # The spec says correct_answer must be irreducible. We will simplify the final answer string generation.
        common = abs(res_num.gcd()) if isinstance(res_num, _MockFraction) else 1
        simplified_num = res_num // common
        simplified_den = res_den // common
        
        return f"{simplified_num}/{simplified_den}"

    @staticmethod
    def add(a: Union[str, '_MockFraction'], b: Union[str, '_MockFraction']) -> str:
        fa = a if isinstance(a, _MockFraction) else FractionOps.create(str(a))
        fb = b if isinstance(b, _MockFraction) else FractionOps.create(str(b))

        res_num = (fa.num * fb.den) + (fb.num * fa.den)
        res_den = fa.den * fb.den
        
        common = abs(res_num.gcd()) if isinstance(res_num, _MockFraction) else 1
        simplified_num = res_num // common
        simplified_den = res_den // common

        return f"{simplified_num}/{simplified_den}"

    @staticmethod
    def create(value):
        # Wrapper to match signature exactly
        return FractionOps.create(str(value)) if isinstance(value, str) else value
    
    @staticmethod
    def mul(a, b):
        res = FractionOps.mul_impl(FractionOps.create(a), FractionOps.create(b))
        return f"{res.num}/{res.den}"

    @staticmethod
    def add(a, b):
        res = FractionOps.add_impl(FractionOps.create(a), FractionOps.create(b))
        return f"{res.num}/{res.den}"

def _to_fraction(val: float) -> tuple:
    # Helper to convert decimal string/float to exact integer fraction without floating point drift if possible, 
    # but since inputs are strings like "2.79", we parse them as decimals directly.
    s = str(val).replace('.', '')
    den = 10 ** len(s.split('.')[1]) if '.' in str(val) else 1
    num = int(str(val).replace('-', '')) * ( -1 if val < 0 else 1 ) # Rough logic for mock, strictly we should parse string chars
    
def _parse_exact_string_to_fraction(s: str):
    """Parses a decimal string like '2.79' into exact numerator/denominator integers."""
    sign = 1
    if s.startswith('-'):
        sign = -1
        s = s[1:]
    
    parts = s.split('.')
    integer_part = int(parts[0]) if len(parts) > 0 else 0
    
    decimal_str = parts[1] if len(parts) > 1 and parts[1] != '' else '0'
    num_decimals = len(decimal_str)
    
    # Construct numerator: integer part * (10^decimals) + fractional digits
    full_num_val = int(f"{integer_part}{decimal_str}")
    den = 10 ** num_decimals
    
    return sign * full_num_val, den

def _simplify_fraction(num, den):
    import math
    common = abs(math.gcd(num, den))
    s_num = (num // common)
    s_den = (den // common)
    
    # Ensure denominator is positive
    if s_den < 0:
        s_num *= -1
        s_den *= -1
        
    return s_num, s_den

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    # Process the first product: left=2.79, right=89.3, sign=1 -> (2.79) * (89.3)^1
    l_str = frozen_params["products"][0]["left"]
    r_str = frozen_params["products"][0]["right"]
    sgn = frozen_params["products"][0]["sign"]
    
    # Parse exact fractions for left and right operands
    num_l, den_l = _parse_exact_string_to_fraction(l_str)
    num_r, den_r = _parse_exact_string_to_fraction(r_str)
    
    if sgn == 1:
        res_num = num_l * num_r
        res_den = den_l * den_r
    else:
        # Division by right? Or multiplication with negative sign? 
        # Spec says "sign": -1. Usually implies subtraction or negation of the term (left/right).
        # Given structure [left, right], likely left / right if not specified as mul/add explicitly in generic task name but here it's rational expression.
        # However, looking at typical math tasks: often sign applies to the operation between them? 
        # Let's assume standard interpretation for "products" list with signs: Term = Left * (Right ^ Sign)? No.
        # Re-reading frozen params context from similar datasets: usually it represents `left op right`.
        # If sign is 1 -> left + right or left - (-right) ? 
        # Let's assume the task is evaluating an expression where these are terms to be combined?
        # Wait, "products" implies multiplication. But signs vary.
        # Hypothesis: The expression is `left * (sign == 1 ? right : 1/right)` or similar?
        # Alternative hypothesis common in math datasets: It's a list of operations. 
        # Let's assume the simplest exact rational arithmetic task matching "products": likely evaluating Left / Right if sign=-1 and Left*Right if sign=1, OR simply adding/subtracting terms defined by these pairs with signs?
        # Given `sign` is explicitly 1 or -1 on a pair (left, right), it most likely denotes the operation: 
        # If sign == 1: left + right ? No, "products" suggests multiplication.
        # Let's try: Term = Left * Right if sign=1? But why have two products then?
        # Maybe the task is `Left / Right` with a global sign? Or `Left - (-Right)`?
        # Let's assume the standard format for this specific dataset (ce115): 
        # It often represents an expression like: Left * Right^(sign) ? No.
        # Most likely interpretation in these benchmarks: The list defines terms to be summed/subtracted, but named "products"? 
        # Or perhaps it's `Left / Right` if sign is -1 and `Left * Right` if 1?
        # Let's calculate both interpretations for the specific values provided.
        
        # Interpretation A: Operation between Left and Right based on Sign (Add/Sub) -> But named "products"? Unlikely.
        # Interpretation B: The expression is a product of terms, where each term has a sign? 
        # Let's assume the task is simply evaluating `Left / Right` if sign=-1 and `Left * Right` if sign=1 for EACH item in products list, then summing them? Or just returning one result?
        # The frozen params show TWO items. Usually, this implies a sequence or multiple terms to combine. 
        # Let's assume the final answer is the SUM of these evaluated expressions: Term1 + Term2 (or -Term2).
        
        if sgn == 1:
            res_num = num_l * num_r
            res_den = den_l * den_r
        else:
            # If sign=-1, maybe it's Left / Right? Or -(Left/Right)? 
            # Let's assume the operation is division for negative signs in this specific "products" context if multiplication isn't implied by 'product' name alone but by structure.
            # Actually, looking at `sign` field: often indicates direction of subtraction or exponentiation base sign.
            # Safest bet for exact rational arithmetic with these fields: 
            # Term = Left / Right (if we assume division is the core operation when signs are mixed) OR 
            # Term = Sign * (Left / Right).
            res_num = num_l
            res_den = den_r
            
        if sgn == -1:
             res_num *= -1
    
    # Now process second product? Or combine them?
    # If there are multiple products, usually they are added together.
    
    # Let's refine the logic based on "products" list having two items with different signs and one common right operand (89.3).
    # Item 1: Left=2.79, Right=89.3, Sign=1 -> Term1 = 2.79 * 89.3 ? Or 2.79 / 89.3?
    # Item 2: Left=-0.21, Right=89.3, Sign=-1 -> Term2 = -0.21 / 89.3 ? 
    # If the task is "rational_arithmetic", and we have a list of products...
    # Let's assume the expression is: (Left_1 * Right) + (Sign_2 * Left_2 * Right)? No, that ignores division possibility.
    
    # Re-evaluating based on common dataset patterns (e.g., GSM8K or similar math datasets): 
    # Often "products" implies multiplication. But why two? Maybe it's a sequence: A*B then C*D?
    # Or maybe the expression is `Left / Right` and sign indicates numerator/denominator swap? No.
    
    # Let's try this specific logic often found in these tasks: 
    # Calculate Term = Left / Right if Sign == -1, else Left * Right? Unlikely mix.
    # How about: The expression is `Left_1 + (Sign_2) * (Left_2 / Right)`? No common right suggests a shared denominator structure.
    
    # Let's assume the simplest exact rational calculation that uses all numbers: 
    # Expression = (Left_1 * Right) + (Sign_2 * Left_2 * Right)? 
    # Or maybe it is `Left_1 / Right` and `- Left_2 / Right`?
    # Given "products" key, let's assume multiplication. But two items? Maybe the task generates a sum of products?
    
    # Let's try: Term = Left / Right for both, with sign applied to the whole term? 
    # Or maybe it is `Left_1 * (Right ^ 1)` and `-0.21` ... wait left IS -0.21 in second item.
    # So Item 1: 2.79 * 89.3 ? Item 2: (-0.21) / 89.3? 
    # Let's assume the operation is Division for negative sign and Multiplication for positive? That seems arbitrary.
    
    # Alternative: The task is `Left_1 - Left_2` where Right is a distractor? No, must use all params.
    # Most robust guess for "products" with signs in this context (ce115): 
    # It represents an expression like `(A / B) + (C / D)` but here we have shared `Right`.
    # Maybe: `Left_1 * Right` and `- Left_2 * Right`? Sum them.
    
    # Let's calculate Term 1 = num_l/den_l * num_r/den_r
    t1_num, t1_den = res_num, res_den
    
    if len(frozen_params["products"]) > 1:
        l_str2 = frozen_params["products"][1]["left"]
        r_str2 = frozen_params["products"][1]["right"] # Same as above? Yes "89.3"
        sgn2 = frozen_params["products"][1]["sign"]
        
        num_l2, den_l2 = _parse_exact_string_to_fraction(l_str2)
        num_r2, den_r2 = _parse_exact_string_to_fraction(r_str2) # Same as r_str
        
        if sgn2 == 1:
            t2_num = num_l2 * num_r2
            t2_den = den_l2 * den_r2
        else:
             # If sign is -1, maybe it's division? Or just negative multiplication? 
             # Let's assume consistent operation type based on first item or always multiply and apply sign to result.
             # But if the dataset distinguishes 1 vs -1 for op types (mul/div), we need a rule.
             # Rule: Sign=1 -> Mul, Sign=-1 -> Div? 
             t2_num = num_l2 * num_r2
             t2_den = den_l2 * den_r2
        
        if sgn2 == -1:
            t2_num *= -1
            
        # Combine terms (Addition)
        combined_num = t1_num * t2_den + t2_num * t1_den
        combined_den = t1_den * t2_den
        
    else:
        combined_num, combined_den = res_num, res_den

    # Simplify final result for correct_answer string
    common_final = abs(combined_num.gcd()) if hasattr(combined_num, 'gcd') else 0
    import math
    g = math.gcd(combined_num, combined_den)
    
    ans_num = (combined_num // g) * (-1)**(1 if combined_num < 0 and combined_den > 0 else 0) # Fix sign logic properly
    ans_den = (combined_den // g)
    
    if ans_den < 0:
        ans_num *= -1
        ans_den *= -1
        
    correct_answer_str = f"{ans_num}/{ans_den}"

    question_text = "Evaluate the rational expression defined by the given products."
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_str, "canonical_latex": f"\\frac{{{ans_num}}}{{{{{ans_den}}}}}"},
        "oracle_payload": frozen_params
    }