import math
from fractions import Fraction as F
# Mocking the required imports from 'core.prompts.domain_function_library' 
# since this is a standalone executable script that must work without external file dependencies for execution logic demonstration,
# but strictly adheres to the API contract requested.
class FakeFractionOps:
    @staticmethod
    def create(value): return F(str(value)) if isinstance(value, str) else value
    
    @staticmethod 
    def add(a, b): return a + b

    @staticmethod
    def to_latex(val, mixed=False):
        f = val.numerator / math.gcd(val.numerator, val.denominator), val.denominator # Simplified logic for mock
        
        if not isinstance(val, F): raise TypeError("Expected Fraction")
        
        num, den = val.numerator, val.denominator
        g = abs(math.gcd(num, den))
        n_red, d_red = num // g, den // g
        
        latex_parts = []
        sign_str = "-" if n_red < 0 else ""
        n_abs, d_abs = abs(n_red), d_red
        
        # Integer part check for mixed number logic (though problem is pure fraction usually)
        int_part = n_abs // d_abs
        rem_num = n_abs % d_abs
        
        parts = []
        
        if int_part > 0:
            parts.append(f"{int_part}")
            
        if rem_num != 0 or not mixed: # Always show numerator unless specifically asked otherwise in simple cases, but problem asks for irreducible fraction usually meaning improper allowed. 
            # The task says "irreducible fraction", standard is a/b even if |a|>=b. Mixed numbers are specific request 'mixed=True'.
            parts.append(f"\\frac{{{sign_str}{rem_num}}}{{d_abs}}")

        return "".join(parts)

# Re-implementing the API as described in prompt to ensure it works when imported or used directly, 
# but since we cannot import external files without a package structure, we define them here 
# and assume they are available if this code were pasted into an environment with that module.
# However, the instruction says "Use the listed domain API". To make this runnable as pure Python source:
import core.prompts.domain_function_library

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen", {"expression": "9/22 + 11/18 - (23/22 - 7/18)"})
    
    # Parse expression manually to build the fraction tree using FractionOps if needed, 
    # but since we have a hardcoded frozen parameter for this specific task instance:
    expr_str = "9/22 + 11/18 - (23/22 - 7/18)"
    
    from fractions import Fraction
    
    term1 = F("9") / F("22")
    term2 = F("11") / F("18")
    inner_paren = F("23") / F("22") - F("7") / F("18")
    
    # Calculate: (term1 + term2) - inner_paren
    part_a = core.prompts.domain_function_library.FractionOps.add(term1, term2)
    result_frac = core.prompts.domain_function_library.FractionOps.add(part_a, (-inner_paren))
    
    canonical_latex_str = core.prompts.domain_function_library.FractionOps.to_latex(result_frac, mixed=False)
    
    return {
        "question_text": f"Compute the exact value of $\\left( \\frac{9}{22} + \\frac{11}{18} \\right) - \\left( \\frac{23}{22} - \\frac{7}{18} \\right)$.",
        "correct_answer": {
            "numerator": result_frac.numerator,
            "denominator": result_frac.denominator,
            "canonical_latex": canonical_latex_str
        },
        "oracle_payload": frozen_params["expression"] # The spec says oracle_payload must exactly equal the frozen sampled parameters dict? 
    }

# Correction: The prompt says "oracle_payload must exactly equal the frozen sampled parameters".
# Frozen sampled parameters was a dict. So payload should be that dict or just re-assign it.
# Let's adjust return to match strictly.

def generate(level=1, **kwargs):
    # Re-importing inside function scope if not global? No, keep clean.
    from fractions import Fraction as F
    
    # Hardcoded frozen parameters for this specific task instance based on prompt context:
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    term1 = core.prompts.domain_function_library.FractionOps.create("9") / F(22) # create might not support int division directly in mock, let's use standard Fraction logic if available or fallback. 
    # Actually, the domain API `FractionOps.create` takes a value and returns a Fraction.
    
    try:
        t1 = core.prompts.domain_function_library.FractionOps.add(core.prompts.domain_function_library.FractionOps.create(9), F(22)) # This assumes create creates numerator? No signature (value). 
        # Let's assume standard usage for the API provided in prompt description implies creating a fraction from components or string.
        # Given strict constraints, I will calculate using standard Fraction and adapt to API if possible.
        # But since `core.prompts.domain_function_library` is external, and we must output source that *uses* it:
        
        t1 = core.prompts.domain_function_library.FractionOps.create("9/22")
        t2 = core.prompts.domain_function_library.FractionOps.create("11/18")
        i_paren_part1 = core.prompts.domain_function_library.FractionOps.add(core.prompts.domain_function_library.FractionOps.create("23/22"), (-core.prompts.domain_function_library.FractionOps.create("7/18"))) # Wait, subtraction.
        
        inner = core.prompts.domain_function_library.FractionOps.add(
            core.prompts.domain_function_library.FractionOps.create("23/22"), 
            core.prompts.domain_function_library.FractionOps.create("-7/18")
        )
        
        left_side = core.prompts.domain_function_library.FractionOps.add(t1, t2)
        final_result = core.prompts.domain_function_library.FractionOps.add(left_side, (-inner)) # Subtracting inner
        
    except Exception:
        from fractions import Fraction as F_std
        t1 = F("9/22")
        t2 = F("11/18")
        inner = (F("23/22") - F("7/18"))
        final_result = (t1 + t2) - inner

    canonical_latex_str = core.prompts.domain_function_library.FractionOps.to_latex(final_result, mixed=False)
    
    return {
        "question_text": f"Compute the exact value of $\\left( \\frac{9}{22} + \\frac{11}{18} \\right) - \\left( \\frac{23}{22} - \\frac{7}{18} \\right)$.",
        "correct_answer": {
            "numerator": final_result.numerator,
            "denominator": final_result.denominator,
            "canonical_latex": canonical_latex_str
        },
        "oracle_payload": frozen_params
    }

# Wait, the instruction says "Do not use input...". It implies a function definition. 
# I will write the complete script including imports and the generate function as requested.
# The user wants ONLY Python source.

import math
from fractions import Fraction

try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    # Fallback implementation if module not present, though prompt implies it exists. 
    # To ensure code runs in isolation for the "source" request without external deps failing immediately during parse/run check:
    class LocalFractionOps(FractionOps):
        @staticmethod
        def create(value): return Fraction(str(value))
        
        @staticmethod
        def add(a, b): return a + b
        
        @staticmethod 
        def to_latex(val, mixed=False):
            if not isinstance(val, Fraction): raise TypeError("Expected Fraction")
            num = val.numerator
            den = val.denominator
            
            sign_str = "-" if num < 0 else ""
            n_abs, d_red = abs(num), den
            
            # Check for reducibility? Fractions class handles it automatically.
            
            int_part = n_abs // d_red
            rem_num = n_abs % d_red
            
            parts = []
            if mixed:
                pass 
            else:
                 # Standard improper or proper fraction format in LaTeX
                 latex_parts = []
                 if num < 0: sign_str = "-"
                 
                 latex_parts.append(f"{sign_str}{rem_num}" if rem_num > 0 else "")
                 latex_parts.insert(0, f"\\frac{{{latex_parts[1]}}}{{d_red}}") # Logic messy in fallback.
            
            # Correct simple LaTeX for fraction: \numerator/denominator
            s = ""
            if num < 0: s += "-"
            s += f"\frac{abs(num)}{den}" # Wait, need to handle sign inside or outside? 
            # Fraction class keeps signs in numerator.
            
            return f"\\frac{{{num}}}{{d_red}}"

# Actually, let's just use the standard library and simulate the API if not found, but keep it clean.
# Since I must output ONLY Python source:

import math
from fractions import Fraction as F

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen", {"expression": "9/22 + 11/18 - (23/22 - 7/18)"})
    
    # Using the requested domain API structure if available, else local implementation logic.
    try:
        from core.prompts.domain_function_library import FractionOps as RealFractionOps
        
        term1 = RealFractionOps.create("9/22")
        term2 = RealFractionOps.create("11/18")
        
        # inner part: 23/22 - 7/18 -> add(23/22, create(-7/18)) or subtract directly? 
        # API only has `add`. So use negative.
        term_neg_7 = RealFractionOps.create("-7/18")
        inner_part = RealFractionOps.add(term1, term2) # Wait, left side is 9/22 + 11/18
        
        t_a = RealFractionOps.create("23/22")
        t_b = RealFractionOps.create("-7/18")
        paren_result = RealFractionOps.add(t_a, t_b)
        
        # Total: (t1+t2) - paren_result -> add((t1+t2), (-paren_result)) ? 
        # Or just standard math. The prompt says "Use the listed domain API for each supported core operation".
        # Operations needed: create, add. Subtraction is addition of negative.
        
        left_sum = RealFractionOps.add(term1, term2)
        neg_paren = RealFractionOps.create(-paren_result.numerator / paren_result.denominator) if hasattr(paren_result, 'numerator') else -F(str(paren_result)) # Simplified
        
        # Actually simpler: create("A/B") returns Fraction. 
        # Subtraction A-B is add(A, -B).
        
        left_side = RealFractionOps.add(term1, term2)
        right_side_neg = RealFractionOps.create("-" + str(Fraction(str(paren_result))))
        final_res = RealFractionOps.add(left_side, real_fraction_from_str(f"{paren_result.numerator}/{paren_result.denominator}")) # Too complex.

    except ImportError:
        from fractions import Fraction as F_std
        
        term1 = F("9/22")
        term2 = F("11/18")
        
        p_a = F("23/22")
        p_b = F("-7/18") # Subtraction handled by negative numerator or add function if available. 
        # Assuming standard Fraction math for calculation but formatting via API.
        
        inner = p_a + p_b
        
        left_sum = term1 + term2
        final_res = left_sum - inner

    canonical_latex_str = f"\\frac{{{final_res.numerator}}}{{d_final}}" if hasattr(final_res, 'numerator') else str(final_res) # Placeholder
    
    # Let's implement the API logic inline to be safe and compliant with "Use listed domain API".
    # Since I cannot guarantee external import works in this snippet context without file system:
    
    class MockFractionOps:
        def __init__(cls): pass
        
        @classmethod
        def create(cls, value): return F(value) if isinstance(value, str) else value
        
        @classmethod 
        def add(cls, a, b): return cls.create(str(a)+str(b)) # No. 
        
    # Re-evaluating: The prompt asks to implement `generate`. It assumes the environment has `core.prompts.domain_function_library`.
    # I will write code that imports it and uses it. If import fails (which shouldn't in target env), fallback is risky but here we assume success.

import core.prompts.domain_function_library as lib_math

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen", {"expression": "9/22 + 11/18 - (23/22 - 7/18)"})
    
    # Parse expression components using FractionOps.create for strings like "a/b"
    t1 = lib_math.FractionOps.create("9/22")
    t2 = lib_math.FractionOps.create("11/18")
    
    p_a = lib_math.FractionOps.create("23/22")
    p_b = lib_math.FractionOps.create("-7/18") # Representing - 7/18 as + (-7/18) for add
    
    inner_sum = lib_math.FractionOps.add(p_a, p_b)
    
    left_sum = lib_math.FractionOps.add(t1, t2)
    
    final_frac = lib_math.FractionOps.add(left_sum, -inner_sum.numerator / inner_sum.denominator if hasattr(inner_sum, 'numerator') else (-lib_math.FractionOps.create(str(-inner_sum)))) # Fallback logic
    
    # Better: Use add with negative fraction string
    neg_inner_str = f"-{int(inner_sum)}" + (f"/{denom}" if not isinstance(inner_sum, str) and '/' in str(inner_sum) else "") 
    # Actually FractionOps.create handles "A/B". We need to convert inner sum to a single value.
    
    # Correct approach: 
    # final = left - right => add(left, create(-right))
    if hasattr(lib_math.FractionOps, 'create'):
        neg_inner_val = lib_math.FractionOps.create(f"-{inner_sum.numerator}/{inner_sum.denominator}")
        result_frac = lib_math.FractionOps.add(left_sum, neg_inner_val)
        
        latex_str = lib_math.FractionOps.to_latex(result_frac, mixed=False)
    else:
        # Fallback if API not found (shouldn't happen per spec but for robustness in source generation):
        from fractions import Fraction as F_std
        result_frac = left_sum - inner_sum
        latex_str = f"\\frac{{{result_frac.numerator}}}{{d}}"

    return {
        "question_text": r"\text{Compute the exact value of } \left( \frac{9}{22} + \frac{11}{18} \right) - \left( \frac{23}{22} - \frac{7}{18} \right).",
        "correct_answer": {
            "numerator": result_frac.numerator,
            "denominator": result_frac.denominator,
            "canonical_latex": latex_str # Needs to be fixed properly: f"\\frac{{{result_frac.numerator}}}{{d}}" -> use correct var name if available.
        },
        "oracle_payload": frozen_params["expression"] 
    }

# Wait, oracle_payload must equal the FROZEN SAMPLED PARAMETERS (the dict), not just the string expression inside it?
# Prompt: "oracle_payload must exactly equal the frozen sampled parameters." -> Dict.
# Frozen params = {"expression": "..."}
# So payload should be that dict.

import core.prompts.domain_function_library as lib_math

def generate(level=1, **kwargs):
    # Ensure we have a valid environment for FractionOps if not present (unlikely per spec)
    try:
        from fractions import Fraction as F_std
        t = lib_math.FractionOps.create("9/22")
    except Exception:
        pass

    frozen_params = kwargs.get("frozen", {"expression": "9/22 + 11/18 - (23/22 - 7/18)"})
    
    # Re-calculate using standard library if API fails, but use API for output.
    t1 = lib_math.FractionOps.create("9/22")
    t2 = lib_math.FractionOps.create("11/18")
    p_a = lib_math.FractionOps.create("23/22")
    # Subtraction: add(p_a, -7/18) -> create("-7/18")
    p_b_neg = lib_math.FractionOps.create("-7/18") 
    inner_sum = lib_math.FractionOps.add(p_a, p_b_neg)
    
    left_sum = lib_math.FractionOps.add(t1, t2)
    
    # Subtracting inner: add(left_sum, -inner_sum) -> create(-num/den)
    neg_inner_str = f"-{int(inner_sum.numerator)}" if abs(int(inner_sum)) > 0 else "-" + str(abs(inner_sum)) 
    # Simpler: FractionOps.create("-1 * inner")? No. Just construct string "-N/D".
    
    num_i, den_i = inner_sum.numerator, inner_sum.denominator
    neg_inner_str = f"-{num_i}/{den_i}" if num_i != 0 else "0" # Handle zero case
    
    final_frac = lib_math.FractionOps.add(left_sum, lib_math.FractionOps.create(neg_inner_str))
    
    latex_output = lib_math.FractionOps.to_latex(final_frac, mixed=False)

    return {
        "question_text": r"\text{Compute the exact value of } \left( \frac{9}{22} + \frac{11}{18} \right) - \left( \frac{23}{22} - \frac{7}{18} \right).",
        "correct_answer": {
            "numerator": final_frac.numerator,
            "denominator": final_frac.denominator,
            "canonical_latex": latex_output
        },
        "oracle_payload": frozen_params
    }

# Final check: The prompt says "Do not use input...". 
# I will provide the clean source with imports and function.
import core.prompts.domain_function_library as lib_math

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen", {"expression": "9/22 + 11/18 - (23/22 - 7/18)"})
    
    t1 = lib_math.FractionOps.create("9/22")
    t2 = lib_math.FractionOps.create("11/18")
    
    p_a = lib_math.FractionOps.create("23/22")
    # - 7/18 is adding -7/18
    p_b_neg = lib_math.FractionOps.create("-7/18") 
    inner_sum = lib_math.FractionOps.add(p_a, p_b_neg)
    
    left_sum = lib_math.FractionOps.add(t1, t2)
    
    # Calculate final: left - right. Since we have Fraction objects, subtraction is available via operator- or add with negative.
    # The API `add` takes two fractions. We need to subtract inner_sum from left_sum.
    # Construct "-inner" as a fraction string? 
    # If lib_math.FractionOps.create accepts "a/b", we can create the negation of inner_sum by creating its additive inverse manually or using logic.
    
    # Let's assume standard Fraction subtraction works if `add` isn't overloaded, but spec says use API for operations.
    # We need to add left_sum and (-inner_sum). 
    # Create string representation: f"-{num}/{den}"? No, sign is in numerator usually. "-1/2".
    
    num_i = inner_sum.numerator
    den_i = inner_sum.denominator
    
    if num_i < 0:
        neg_inner_str = f"{num_i}/{den_i}" # Already negative
    else:
        neg_inner_str = f"-{num_i}/{den_i}"
        
    final_frac = lib_math.FractionOps.add(left_sum, lib_math.FractionOps.create(neg_inner_str))
    
    latex_output = lib_math.FractionOps.to_latex(final_frac, mixed=False)

    return {
        "question_text": r"\text{Compute the exact value of } \left( \frac{9}{22} + \frac{11}{18} \right) - \left( \frac{23}{22} - \frac{7/18} \right).",
        "correct_answer": {
            "numerator": final_frac.numerator,
            "denominator": final_frac.denominator,
            "canonical_latex": latex_output
        },
        "oracle_payload": frozen_params
    }

# Wait, the question text in my draft had a typo. Fix: 7/18 not 7/18 with slash inside wrong place.
# Also verify `to_exact` adapter mentioned? No, it says "use to_exact adapter" but then lists FractionOps.to_latex. 
# I'll stick to the listed APIs in DOMAIN section.

import core.prompts.domain_function_library as lib_math

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen", {"expression": "9/22 + 11/18 - (23/22 - 7/18)"})
    
    t1 = lib_math.FractionOps.create("9/22")
    t2 = lib_math.FractionOps.create("11/18")
    
    p_a = lib_math.FractionOps.create("23/22")
    # - 7/18 -> create("-7/18")
    p_b_neg = lib_math.FractionOps.create("-7/18") 
    inner_sum = lib_math.FractionOps.add(p_a, p_b_neg)
    
    left_sum = lib_math.FractionOps.add(t1, t2)
    
    # Construct negative of inner sum for subtraction using add API
    if inner_sum.numerator < 0:
        neg_inner_str = f"{inner_sum.numerator}/{inner_sum.denominator}"
    else:
        neg_inner_str = f"-{abs(inner_sum.numerator)}/{inner_sum.denominator}"
        
    final_frac = lib_math.FractionOps.add(left_sum, lib_math.FractionOps.create(neg_inner_str))
    
    latex_output = lib_math.FractionOps.to_latex(final_frac, mixed=False)

    return {
        "question_text": r"\text{Compute the exact value of } \left( \frac{9}{22} + \frac{11}{18} \right) - \left( \frac{23}{22} - \frac{7}{18} \right).",
        "correct_answer": {
            "numerator": final_frac.numerator,
            "denominator": final_frac.denominator,
            "canonical_latex": latex_output
        },
        "oracle_payload": frozen_params
    }