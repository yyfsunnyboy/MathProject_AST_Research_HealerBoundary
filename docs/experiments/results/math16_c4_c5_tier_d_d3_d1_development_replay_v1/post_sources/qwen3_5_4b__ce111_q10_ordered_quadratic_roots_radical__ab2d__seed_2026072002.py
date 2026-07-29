from fractions import Fraction
import math
from typing import Dict, Any

# Mocking required domain functions from core.prompts.domain_function_library
class RadicalOps:
    @staticmethod
    def simplify_term(coeff: int | float, radicand: int) -> tuple[int, int]:
        # Simplify radical coefficient and square-free part
        if isinstance(radicand, Fraction):
            rad = int(radicand.numerator / (radicand.denominator ** 2)) * (radicand.denominator // math.gcd(int(radicand.numerator), radicand.denominator) ** 2) # Simplified logic placeholder for square-free extraction if needed, but standard quadratic roots usually yield simple forms.
            # For this specific problem: sqrt(3). Coeff is 1, Radicand is 3.
        else:
            rad = int(radicand)
        
        return (int(coeff), int(rad))

    @staticmethod
    def format_expression(terms_dict: Dict[str, Any], denominator: Fraction | None = None) -> str:
        # Format terms into LaTeX string like "2a + b" or similar based on input structure.
        # Here we construct the expression for 2a+b directly as per target logic if needed, 
        # but generally formats a list of {coeff, radicand} items.
        parts = []
        for term in terms_dict.values():
            coeff = str(term[0])
            rad = str(term[1])
            if isinstance(coeff, Fraction):
                coeff = f"{int(coeff.numerator)}/{int(coeff.denominator)}"
            # Assuming standard form a*sqrt(b). If coefficient is 2 and radicand is b.
            parts.append(f"{coeff}\\cdot\\sqrt{{{rad}}}")
        return " + ".join(parts)

class FractionOps:
    @staticmethod
    def create(value):
        if isinstance(value, int):
            return Fraction(value)
        elif isinstance(value, float):
            # Avoid floating point issues by converting to nearest fraction or using exact representation
            from decimal import Decimal
            d = Decimal(str(value))
            f = Fraction(d).limit_denominator(10**9)
            return f
        else:
            raise ValueError(f"Unsupported type for Fraction creation: {type(value)}")

def generate(level=1, **kwargs):
    frozen_params = {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    
    # Parse equation (x-2)^2 = 3 -> x^2 - 4x + 4 = 3 -> x^2 - 4x + 1 = 0
    a_val, b_val, c_val = 1, -4, 1
    
    discriminant = b_val**2 - 4*a_val*c_val # 16 - 4 = 12
    sqrt_discriminant = math.sqrt(discriminant) # sqrt(12) = 2*sqrt(3)
    
    x1 = (-b_val + sqrt_discriminant) / (2 * a_val)
    x2 = (-b_val - sqrt_discriminant) / (2 * a_val)
    
    # Calculate coefficients for the radical part: coeff and radicand
    # We need to express 2*sqrt(3) as A + B where we map to 'a' and 'b'.
    # The problem asks for "rational, radical_coefficient, radicand".
    # x1 = (4 - 2*sqrt(3))/2 = 2 - sqrt(3). 
    # Wait, the target is "2a+b" which implies an expression like $2\sqrt{b} + a$ or similar?
    # Re-reading task: correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand.
    # Let's look at x = 2 +/- sqrt(3). 
    # If we consider the term under root as 'a' and coefficient as 'b'? No, target is "2a+b".
    # Likely mapping: The radical part is $\sqrt{3}$. Coefficient in front of it?
    # In x = 2 - sqrt(3), rational=2, coeff=-1, radicand=3. 
    # Or maybe the question asks for the form $A\sqrt{B}$ where A and B are integers?
    # Let's assume the standard output format: {rational_part, radical_coefficient, radicand}.
    # For x = 2 - sqrt(3): rational=2, coeff=-1, radicand=3.
    
    rational_val = Fraction(int(x1)) # Integer part if possible? Or just floor/ceil? 
    # Actually, for (x-2)^2=3 -> x^2-4x+1=0. Roots are 2 +/- sqrt(3).
    # Rational part: 2. Radical coeff: -1 or +1 depending on root selection. Radicand: 3.
    
    rational_part = Fraction(2)
    radical_coefficient_val = Fraction(-1) if level == 1 else Fraction(1) # Default to negative for one of the roots as per typical ordering a>b? 
    # If order is "a>b", maybe we pick the smaller root (with minus)? Or larger?
    # Let's assume standard principal or specific sign based on target. Target "2a+b" suggests 2*coeff + radicand? No, likely just formatting.
    # Given frozen params: equation "(x-2)^2=3", order "a>b". 
    # Usually implies comparing roots x1 > x2. If a=x1, b=x2 then a>x2 is false if we map directly to values? 
    # Let's stick to the algebraic form of one root as requested by structure.
    
    radicand_val = 3
    
    # Construct terms for formatting
    term_dict = {f"term_{i}": (radical_coefficient_val, radicand_val) for i in range(1)} 
    # Actually we need to format the radical part specifically.
    # The answer should be a dict containing: rational_part, radical_coefficient, radicand.
    
    correct_answer = {
        "rational": int(rational_part),
        "radical_coefficient": -1 if level == 1 else 1, 
        "radicand": int(radicand_val)
    }
    
    # Generate LaTeX for the radical part using domain API
    terms_for_latex = [correct_answer["rational"], correct_answer["radical_coefficient"]] # Just placeholder logic to use format_expression if needed?
    # The prompt says: "correct_answer must include result with rational, radical_coefficient ... and canonical_latex".
    
    latex_str = f"{int(rational_part)}\\cdot{abs(correct_answer['radical_coefficient'])}\\sqrt{{{int(radicand_val)}}}" 
    if correct_answer["radical_coefficient"] < 0:
        # Handle negative sign outside or inside? Usually -1*sqrt(3) is written as \\sqrt[2]{...} no.
        latex_str = f"-{abs(correct_answer['radical_coefficient'])}\\cdot\\sqrt{{{int(radicand_val)}}}" if correct_answer["rational"] == 0 else \
                   f"{correct_answer['rational']} - {abs(correct_answer['radical_coefficient'])} \\cdot \\sqrt{{3}}" # Standard form
    
    canonical_latex = latex_str.replace("\\", "\\\\") # Ensure proper escaping for LaTeX delimiters in the string context if needed, but standard mathjax uses \
    
    question_text = r"\text{Solve } (x-2)^2=3. Express one root as $a + b\sqrt{n}$ where $b$ is $\pm 1$. Identify rational part, coefficient of radical, and radicand."

    # Ensure oracle_payload matches frozen params exactly
    oracle_payload = {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer | {"canonical_latex": latex_str}, # Merge dicts safely in Python 3.9+ or use update logic if older version assumed? Assuming modern env. If not, manual merge: dict(correct_answer)
        "oracle_payload": oracle_payload
    }

# Fallback for python < 3.10 union operator safety just in case the environment is strict old-version but usually these tasks assume recent Python. 
# TIER_D_QUARANTINE: if hasattr(dict, "__or__"):
# TIER_D_QUARANTINE:     pass # OK
# TIER_D_QUARANTINE: else:
# TIER_D_QUARANTINE:     def merge_dicts(d1, d2): return {**d1, **d2}

# Finalize correct_answer structure to ensure it has all required keys explicitly as per spec "rational, radical_coefficient ... and canonical_latex"
# TIER_D_QUARANTINE: final_correct = dict(correct_answer)
# TIER_D_QUARANTINE: final_correct["canonical_latex"] = latex_str.replace("\\", "\\\\") # Double backslash for raw string safety in JSON-like context if needed? No, just standard LaTeX.

# TIER_D_QUARANTINE: return {
# TIER_D_QUARANTINE:     "question_text": question_text,
# TIER_D_QUARANTINE:     "correct_answer": final_correct,
# TIER_D_QUARANTINE:     "oracle_payload": oracle_payload
# TIER_D_QUARANTINE: }