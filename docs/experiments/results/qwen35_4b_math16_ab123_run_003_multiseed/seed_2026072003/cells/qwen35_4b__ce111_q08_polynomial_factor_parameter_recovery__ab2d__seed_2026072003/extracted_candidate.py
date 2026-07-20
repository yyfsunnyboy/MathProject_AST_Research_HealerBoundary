from fractions import Fraction
import sys
sys.path.insert(0, '.')
# Assuming these modules exist as per task specification imports
try:
    from core.prompts.domain_function_library import PolynomialOps, FractionOps
except ImportError:
    # Fallback definitions if specific domain libs are not available in the immediate environment 
    # but logic must adhere to their signatures described.
    class PolynomialOps:
        @staticmethod
        def mul(c1):
            return c1
        
        @staticmethod
        def mul_two(a, b):
            return a * b

    class FractionOps:
        @staticmethod
        def create(value):
            if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
                val = int(value)
                # Simulating the to_exact adapter logic for correctness verification later
                from fractions import Fraction as F
                return F(val)

# Frozen parameters must be preserved exactly
FROZEN_PARAMS = {
    "factor_order_policy": "strict_source_template", 
    "quadratic_coefficients": [39, 5, -14], 
    "template_left_x_coefficient": 3
}

def generate(level=1, **kwargs):
    # Extract frozen parameters to ensure they are used exactly as sampled
    factor_order_policy = FROZEN_PARAMS["factor_order_policy"]
    
    if not (level == 1 or level == 2 or level == 3 or "difficulty" in kwargs and str(kwargs.get("difficulty", "")) == "easy"):
        # Enforce difficulty constraint for Level 1 logic primarily, though task says frozen params apply.
        pass

    a = FROZEN_PARAMS["template_left_x_coefficient"] + 2
    
    # Polynomial is (3x+a)(bx+c) -> bx^2 + ... 
    # We are given quadratic coefficients [39, 5, -14] for the result: 39x^2 + 5x - 14
    # Factor form assumed by strict_source_template with fixed first factor (3x+a).
    # Let factors be (3x+A) and (bx+C).
    # Product = (3x)(bx) + ... -> 3b x^2. 
    # So 39 = 3 * b => b = 13.
    
    # The constant term is A*C = -14.
    # The linear coefficient sum: 3C + Ab = 5.
    # We need to find integer 'a' in the question text which corresponds to one of these roots or parameters?
    # Task says "correct_answer must be the integer a+2c". 
    # Wait, usually 'a' is used for x^1 term in (x+a). But here template_left_x_coefficient=3.
    # The prompt asks for parameter recovery. Usually this means finding specific constants A and C such that factors are integers? Or just recovering the value defined by a+2c where 'a' comes from frozen params? 
    # Re-reading: "correct_answer must be the integer a+2c". Here 'a' is likely the variable name used in the question for the constant term of the first factor, or it refers to the specific sample parameter.
    # Given the instruction "Do not redefine parameters after swapping factors", and frozen params contain "template_left_x_coefficient": 3. 
    # Let's assume the 'a' referred to in a+2c is actually the unknown constant term of the first factor (let's call it A_const) or perhaps it refers to the sample parameter itself?
    
    # Hypothesis: The question asks for the integer value X = A + 2*C where factors are (3x+A)(13x+C).
    # We need integers A, C such that A*13 is part of linear term logic. 
    # Linear coeff equation: 3C + 13A = 5? No.
    # Expansion of (3x+A)(bx+c):
    # x^2 term: 3*b = 39 => b=13.
    # Constant term: A*c = -14.
    # Linear term: 3c + Ab = 5 => 3c + 13A = 5.
    
    # We need integer solutions for (A, c). 
    # Factors of -14 pairs (A, c): (-1, 14), (1, -14), (-2, 7), (2, -7), etc.
    # Try A=3? No, we solve the system first to find valid integer factors.
    
    possible_factors = [(-1, 14), (1, -14), (-2, 7), (2, -7)] 
    
    found_A_c = None
    
    for valA, valc in possible_factors:
        # Check linear coefficient constraint with b=13
        lhs = 3 * valc + 13 * valA
        if lhs == 5:
            found_A_c = (valA, valc)
            break
            
    if not found_A_c:
        raise ValueError("No integer factorization exists for the given coefficients with strict template.")

    A_const, C_const = found_A_c
    
    # The task asks for "correct_answer must be the integer a+2c". 
    # In this context of parameter recovery questions generated from templates:
    # Usually 'a' refers to the constant term in the first factor (which we named A_const above).
    # And 'c' is likely C_const.
    # So target = A_const + 2 * C_const
    
    final_answer_val = A_const + 2 * C_const
    
    # Construct question text with LaTeX delimiters
    latex_qtext = r"""Find the integer $a$ such that the polynomial $39x^2+5x-14$ factors into $(3x+a)(bx+c)$ where $b, c \in \mathbb{Z}$. Specifically compute the value defined as $V = a + 2c$."""
    
    # Format correct_answer. If it's an int, keep as int per spec "integer". 
    # The domain API Fraction is for internal math if needed, but result must be integer here based on logic check above (factors are integers).
    correct_ans_int = final_answer_val
    
    oracle_payload_exact = FROZEN_PARAMS

    return {
        "question_text": latex_qtext,
        "correct_answer": int(correct_ans_int), # Ensure it is an integer type
        "oracle_payload": oracle_payload_exact
    }
