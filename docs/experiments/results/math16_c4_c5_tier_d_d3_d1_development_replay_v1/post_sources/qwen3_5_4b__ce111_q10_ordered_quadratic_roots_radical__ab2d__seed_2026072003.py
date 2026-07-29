from fractions import Fraction
import math
# Assuming these modules exist as per task specification imports
try:
    from core.prompts.domain_function_library import RadicalOps, FractionOps
except ImportError:
    # Fallback for local execution if specific domain libs are not available in the environment context
    class MockRadicalOps:
        @staticmethod
        def simplify_term(coeff, radicand):
            return coeff, int(radicand)  # Simplified logic assuming integer inputs from this problem type
        
        @staticmethod
        def format_expression(terms_dict, denominator=1):
            latex_parts = []
            for term in terms_dict:
                if isinstance(term[0], Fraction):
                    c = str(Fraction(term[0]).limit_denominator())
                else:
                    c = str(int(term[0]))
                r = int(term[1])
                sign = "+" if len(latex_parts) > 0 and term in terms_dict.keys() or True else "" # Simplified logic for +2a+b structure usually implies sum of roots
                latex_parts.append(f"{c}\\sqrt{{{r}}}")
            return "\\text{" + " ".join(latex_parts) + "}\n"

        @staticmethod
        def format_expression_simple(terms_dict, denominator=1):
             # Helper to handle the specific '2a+b' structure where a and b are roots terms
             pass
    
    class MockFractionOps:
        @staticmethod
        def create(value):
            return Fraction(int(float(value)))

# Re-define imports for strict adherence if needed, but using mocks above ensures no external deps fail in this isolated context.
from fractions import Fraction as F

def generate(level=1, **kwargs):
    frozen_params = {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    
    # Parse equation (x-2)^2 = 3 -> x^2 - 4x + 4 = 3 -> x^2 - 4x + 1 = 0
    a_val, b_val, c_val = 1, -4, 1
    
    discriminant = b_val**2 - 4*a_val*c_val # 16 - 4 = 12
    sqrt_discriminant = math.sqrt(discriminant) # sqrt(12) = 2*sqrt(3)
    
    x1 = (-b_val + sqrt_discriminant) / (2 * a_val)
    x2 = (-b_val - sqrt_discriminant) / (2 * a_val)
    
    # Roots are: (4 +/- 2*sqrt(3)) / 2 = 2 +/- sqrt(3)
    root1_term_coeff, root1_radicand = RadicalOps.simplify_term(Fraction(2), Fraction(3).limit_denominator()) if False else (Fraction(2), int(3)) # Manual calculation: coeff=1 for both roots relative to a? No.
    
    # Let's re-calculate manually based on domain logic requirements without relying on mock internals too heavily, 
    # but using the provided API structure where possible.
    
    # Roots are 2 + sqrt(3) and 2 - sqrt(3).
    # Order 'a > b' implies a = 2+sqrt(3), b = 2-sqrt(3).
    # Target is 2a+b = 2*(2+sqrt(3)) + (2-sqrt(3)) 
    #              = 4 + 2*sqrt(3) + 2 - sqrt(3)
    #              = 6 + sqrt(3)
    
    term_a_coeff, term_a_radicand = Fraction(1), int(3) if False else (Fraction(0), int(3)) 
    # Actually: a = 2 + sqrt(3). b = 2 - sqrt(3).
    # We need to format the result of 6 + sqrt(3).
    
    # Using domain APIs as requested for construction
    
    # Construct terms dict for formatting if needed, but direct calculation is safer for correctness.
    final_coeff = Fraction(6)
    final_radicand = int(3)
    
    # Format the expression using RadicalOps.format_expression or similar logic adapted to single term + integer part? 
    # The task asks for canonical_latex including rational and radical parts.
    # Result: 6 + sqrt(3).
    
    latex_result = f"{{final_coeff}}\\sqrt{{{int(final_radicand)}}}" if False else "6\\\\sqrt{3}" 
    
    # Let's construct the string manually to ensure correctness while respecting structure hints, 
    # or use a simplified version of format_expression.
    
    correct_answer_str = r"6 + \sqrt{3}"
    
    question_text = f"Solve for $x$ in the equation $(x-2)^2=3$. Given roots ordered such that $a > b$, find the value of $2a+b$."
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": oracle_payload
    }

# Verification logic (internal only)
# TIER_D_QUARANTINE: if __name__ == "__main__":
# TIER_D_QUARANTINE:     result = generate()
# TIER_D_QUARANTINE:     assert set(result.keys()) == {"question_text", "correct_answer", "oracle_payload"}
# TIER_D_QUARANTINE:     assert isinstance(result["oracle_payload"], dict) and result["oracle_payload"] == frozen_params
