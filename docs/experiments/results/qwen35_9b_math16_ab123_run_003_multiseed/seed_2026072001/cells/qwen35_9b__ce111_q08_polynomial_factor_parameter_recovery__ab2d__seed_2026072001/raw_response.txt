from fractions import Fraction
import sys
sys.path.insert(0, '/app')
try:
    from core.prompts.domain_function_library import PolynomialOps, FractionOps
except ImportError:
    pass

def generate(level=1, **kwargs):
    frozen = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    # Parse quadratic coefficients from frozen parameters: ax^2 + bx + c
    a_quad, b_quad, c_quad = frozen["quadratic_coefficients"]
    
    # The task specifies the first factor is fixed as (3x+a) where 'a' in this context refers to the constant term of that specific linear factor.
    # However, looking at the correct_answer requirement "integer a+2c", we must deduce the intended meaning.
    # In polynomial division problems often found in these datasets:
    # If one root is derived from (3x + A) = 0 => x = -A/3.
    # The other factor would be (x + B).
    # Product: (3x+A)(x+B) = 3x^2 + (3B+A)x + AB.
    # Matching to ax^2+bx+c: 
    # a_quad = 3 => But our frozen 'a' is 39? Wait, the problem says "quadratic_coefficients": [39, 5, -14]. This implies A=39 in standard form Ax^2+Bx+C.
    # BUT the template_left_x_coefficient is fixed at 3. 
    # Let's re-read carefully: "first factor is fixed as (3x+a)". Here 'a' is a variable we need to find? Or is it related to c_quad?
    # Usually, in these specific recovery tasks:
    # We have P(x) = ax^2 + bx + c.
    # Factors are often (mx + n). One factor has coefficient m fixed by template_left_x_coefficient.
    # If the first factor is (3x + k), then 3 * x_other_const = a_quad? No, leading coeff of product is 3 * lead_of_second.
    # Let's assume standard monic-like scaling or specific integer constraints common in these benchmarks.
    
    # Hypothesis: The polynomial P(x) has roots r1 and r2.
    # Factor 1: (3x + k). Root x = -k/3.
    # Factor 2: (mx + n).
    # Product: m*3 * x^2 + ... 
    # Given a_quad=39, b_quad=5, c_quad=-14.
    # If we force the first factor to be (3x + k), then the second must provide the scaling for 39/3 = 13? Or maybe the coefficients are just integers and we solve for factors over rationals/integers that fit.
    
    # Let's try a different interpretation based on "correct_answer is integer a+2c".
    # Usually 'a' in this context refers to the constant term of the fixed factor (let's call it k). And c is c_quad? 
    # If answer = k + 2*c_quad. We need to find k such that factors are integers/valid.
    
    # Let's solve for integer roots/factors first.
    # P(x) = 39x^2 + 5x - 14.
    # Discriminant D = b^2 - 4ac = 25 - 4(39)(-14) = 25 + 2184 = 2209.
    # sqrt(D) = 47 (since 47*47 = 2209).
    # Roots x = (-5 +/- 47) / (2 * 39).
    # Root 1: (-5 + 47)/78 = 42/78 = 7/13. Factor -> (13x - 7). Or scaled? 
    # Root 2: (-5 - 47)/78 = -52/78 = -2/3. Factor -> (3x + 2).
    
    # We have factors corresponding to roots x=7/13 and x=-2/3.
    # Factors in monic form relative to denominators: 
    # For root -2/3, factor is (3x + 2). Leading coeff 3 matches template_left_x_coefficient!
    # So the fixed first factor must be (3x + 2). Thus k = 2.
    # The other factor corresponds to root 7/13 -> denominator 13 -> (13x - 7) or scaled? 
    # If we use integer factors: P(x) is not monic, so factors are usually written as integers if possible.
    # Let's check product of (3x+2)(13x-7): 
    # = 39x^2 + (-21 + 26)x - 14 = 39x^2 + 5x - 14. Matches exactly!
    
    # So the factors are indeed (3x + 2) and (13x - 7).
    # The fixed factor is (3x + a) where a = 2.
    # c_quad = -14.
    # Correct answer formula: "a+2c". 
    # Is 'c' the constant term of the polynomial (-14)? Or something else?
    # If result = 2 + 2*(-14) = 2 - 28 = -26.
    
    k = 2
    c_val = frozen["quadratic_coefficients"][2]
    
    correct_answer_int = k + 2 * c_val
    
    question_text = r"""
Find the constant term $a$ of the linear factor $(3x+a)$ in the polynomial expansion of $P(x) = 39x^2 + 5x - 14$, given that one factor is fixed as $(3x+a)$ with integer coefficients. Then compute the value $V = a + 2c$, where $c$ is the constant term of $P(x)$.
""".strip()

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen
    }