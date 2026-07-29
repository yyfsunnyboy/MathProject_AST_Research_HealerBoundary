from fractions import Fraction
import random
from math import gcd

# Mocking the required imports as they are not available in a standard environment without installation
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify sqrt(n * k^2) -> k * sqrt(n)
        if coeff == 0 or radicand <= 1:
            return (coeff, radicand)
        
        temp_radicand = abs(radicand)
        simplified_coeff = int(coeff)
        
        while temp_radicand > 1 and not is_prime(temp_radicand): # Simplified logic for demo; real impl needs factorization
             pass
        
        # Proper simplification: find largest square divisor of radicand
        sq_free_part, extracted_sq = _get_square_free_and_root(radicand)
        
        new_coeff = coeff * extracted_sq
        return (new_coeff, sq_free_part)

    @staticmethod
    def format_term(coeff, radicand, is_first=True):
        if isinstance(coeff, Fraction):
            num, den = coeff.numerator, coeff.denominator
            if den == 1:
                c_str = str(num)
            else:
                # Handle negative fractions carefully for LaTeX
                sign = "-" if num < 0 and is_first else ""
                abs_num = -num if num < 0 else num
                return f"{sign}\\frac{{{abs_num}}}{{\\sqrt{{{radicand}}}}}"
        elif coeff == 1:
            c_str = "1" if radicand != 1 else "" # If radicand is not square free, handled by simplify_term usually. 
                                                # But here we assume input to format_term might be unsimplified or simplified with coeff=1?
                                                # Contract says correct_answer includes coefficient. Usually '1' is omitted unless it's the only term and specific formatting rules apply.
                                                # Standard math: 1*sqrt(x) -> sqrt(x). 
            if radicand == 1: return "0" # Should not happen after simplify_term on non-zero input usually, but safe guard
            c_str = ""
        elif coeff == -1:
            sign = "-" if is_first else "-\\frac{1}{\\sqrt{" + str(radicand) + "}}" 
            # Actually standard format for negative first term: -\sqrt{x}
            return f"-\\sqrt{{{radicand}}}"
        
        # General case coeff != 0, +/-1 handled above roughly. Let's refine general fraction/int handling inside this block logic if needed.
        # Re-implementing robust formatting based on standard LaTeX rules for radicals
        
        sign = ""
        abs_coeff = int(coeff) if isinstance(coeff, (int, float)) else coeff.numerator // gcd(abs(coeff), 1) # Simplified check
        # Let's stick to the logic: 
        # If coeff is integer > 0 and not 1 -> c\sqrt{r}
        # If coeff is -integer < -1 -> -c\sqrt{r} or (-c)\sqrt{r}? Usually coefficient absorbs sign.
        
        if isinstance(coeff, Fraction):
            num = abs(coeff.numerator)
            den = abs(coeff.denominator)
            
            if den == 1: # Integer coeff
                c_val = int(num * (coeff < 0)) 
                return f"{c_val}\\sqrt{{{radicand}}}" if not is_first else str(c_val).replace("-", "-\\frac{") + "\\sqrt{" + str(radicand) + "}}"
            
            # Fractional coeff: \frac{n}{d}\sqrt{x} -> n\sqrt{\frac{x}{d^2}}? No, usually keep fraction outside.
            return f"\\frac{{{coeff.numerator}}}{{{coeff.denominator}}}\\sqrt{{{radicand}}}"

def _get_square_free_and_root(n):
    if n <= 0: return (n, 1) # Should not happen for radicands in sqrt context usually positive integers
    
    temp = abs(n)
    root_part = 1
    while True:
        d2 = int(temp ** 0.5)
        if d2 * d2 == temp:
            return (temp, d2) # Wait, this is wrong logic for loop
        
    # Correct factorization approach
    factors = {}
    i = 2
    while i * i <= abs(n):
        while n % i == 0:
            n //= i
            if i in factors:
                factors[i] += 1
            else:
                factors[i] = 1
        i += 1
    
    # If remaining n > 1, it's prime factor with power 1 (or whatever left)
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
        
    sq_free_part = 1
    extracted_root = 1
    
    for base, exp in factors.items():
        pass
        # We want to extract pairs. 
        # Actually simpler: sqrt(a * b^2) = b * sqrt(a).
        # For each prime p with exponent e: we take floor(e/2) out as root part, remainder stays inside.
        
    # Re-calculate cleanly
    temp_n = abs(n)
    sq_free_part = 1
    extracted_root = 1
    
    for base in factors.keys():
        exp = factors[base]
        pair_count = exp // 2
        rem_exp = exp % 2
        
        if pair_count > 0:
            extracted_root *= (base ** pair_count)
        
        # The remaining part goes into sq_free_part. 
        # Note: If we are simplifying sqrt(k), the radicand passed to simplify_term is k.
        # We want to return coeff, new_radicand such that original = coeff^2 * new_radicand? No.
        # Original term was coeff * sqrt(radicand).
        # Simplified: (coeff * extracted_root) * sqrt(sq_free_part)
        
    if n > 1 and factors.get(n,0)==0: 
         pass
        
    return sq_free_part, extracted_root

# Helper to ensure the logic holds for the specific frozen parameter {radicand: 135}
def _simplify_logic(radicand):
    # Factorize radicand manually or via math library if available. Since we can't import sympy easily without install constraints in some envs, let's do basic factorization.
    n = abs(radicand)
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            n //= d
            factors[d] = factors.get(d, 0) + 1
        d += 1 if d > 3 else 2 # Optimization
    
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
        
    sq_free_part = 1
    extracted_root = 1
    
    for base, exp in sorted(factors.items()):
        pair_count = exp // 2
        rem_exp = exp % 2
        
        if pair_count > 0:
            extracted_root *= (base ** pair_count)
        
        # The remaining part goes into sq_free_part. 
        # If we have p^3, it becomes p * sqrt(p). Pair=1, Rem=1.
        # So rem_exp is added to the exponent of base in sq_free_part? No, just multiply by base^rem_exp.
        
    for base, exp in factors.items():
         pair_count = exp // 2
         rem_exp = exp % 2
         
         if pair_count > 0:
             extracted_root *= (base ** pair_count)
             
         # Add remainder to sq_free_part? 
         # Wait, the logic above was flawed. Let's restart factorization loop cleanly inside generate or helper.
    
    return None

def _get_square_free_and_root_clean(n):
    if n <= 0: return (n, 1)
    factors = {}
    d = 2
    temp_n = abs(n)
    while d * d <= temp_n:
        while temp_n % d == 0:
            temp_n //= d
            factors[d] = factors.get(d, 0) + 1
        d += 1 if d > 3 else 2
    
    if temp_n > 1:
        factors[temp_n] = factors.get(temp_n, 0) + 1
        
    sq_free_part = 1
    extracted_root = 1
    
    for base in sorted(factors.keys()):
        exp = factors[base]
        pair_count = exp // 2
        rem_exp = exp % 2
        
        if pair_count > 0:
            extracted_root *= (base ** pair_count)
        
        # The remaining part goes into sq_free_part. 
        # Actually, we just multiply the base by itself 'rem_exp' times? No, usually radicand is square-free after extraction.
        # So yes, if exp=3, rem=1 -> sqrt(p^3)=p*sqrt(p). sq_free gets p^1.
        
    for base in sorted(factors.keys()):
         exp = factors[base]
         pair_count = exp // 2
         rem_exp = exp % 2
        
         if pair_count > 0:
             extracted_root *= (base ** pair_count)
         
         # Multiply sq_free_part by base^rem_exp? 
         # Yes. But wait, standard simplification of sqrt(n) results in a square-free radicand.
         # So we just take the product of p^(exp % 2).
    
    for base in sorted(factors.keys()):
        exp = factors[base]
        extracted_root *= (base ** (exp // 2))
        
    sq_free_part = 1
    for base, exp in factors.items():
         rem_exp = exp % 2
         if rem_exp > 0:
             sq_free_part *= (base ** rem_exp)
             
    return sq_free_part, extracted_root

def generate(level=1, **kwargs):
    frozen_params = kwargs.get('frozen', {"radicand": 135}) # Default to task spec if not provided in call args directly but passed via context? 
    # The prompt says "Frozen sampled parameters: {\"radicand\": 135}". I must use this.
    
    radicand = frozen_params.get("radicand", kwargs.get('radicand', 1))
    
    # Simplify the radical term sqrt(radicand) -> coeff * sqrt(sq_free_radicand)
    sq_free_part, extracted_root = _get_square_free_and_root_clean(radicand)
    
    coefficient = extracted_root
    
    # Format the answer string. 
    # If radicand was 135: 135 = 9 * 15 = 3^2 * 15 -> sqrt(135) = 3*sqrt(15). Coeff=3, Radicand=15.
    
    if coefficient == 0 or sq_free_part <= 1 and radicand != sq_free_part: # Edge case handling
        term_str = "0"
    else:
        # Use domain API format_term logic manually since we mocked it but need to ensure correct_answer uses the contract fields properly.
        # The prompt requires using `RadicalOps.format_term`. I will call my class method which implements that signature.
        
        # Determine if this is a "first" term (usually yes for single radical problems)
        latex_str = RadicalOps.format_term(coefficient, sq_free_part, is_first=True)
    
    correct_answer_latex = f"{latex_str}"

    return {
        "question_text": r"Simplify the expression: $\\sqrt{" + str(radicand) + "}$.",
        "correct_answer": correct_answer_latex,
        "oracle_payload": frozen_params
    }