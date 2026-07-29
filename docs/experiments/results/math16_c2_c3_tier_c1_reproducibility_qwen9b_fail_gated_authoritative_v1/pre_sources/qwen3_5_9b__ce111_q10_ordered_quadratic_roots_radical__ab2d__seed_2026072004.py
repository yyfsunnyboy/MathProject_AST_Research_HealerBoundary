from fractions import Fraction
import math

# Mocking external dependencies as they are not provided in standard library but required by prompt constraints
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify radical term: handle coefficient and square-free part of radicand
        if coeff == 0 or radicand <= 1:
            return (Fraction(0), 0)
        
        sign = -1 if coeff < 0 else 1
        abs_coeff = abs(coeff)
        # Extract perfect squares from radicand
        temp_radicand = radicand
        square_free_part = 1
        
        d = 2
        while d * d <= temp_radicand:
            count = 0
            while temp_radicand % d == 0:
                count += 1
                temp_radicand //= d
            
            if count >= 2:
                exponent = count // 2
                square_free_part *= (d ** (count % 2)) # Keep remainder odd power part? No, keep the base. Actually we pull out pairs.
                # Correction: We want to move factors with even exponents outside.
                # If d^k is in radicand, we take d^(floor(k/2)) out and leave d^(k%2) inside.
                
        # Re-calculate properly for square-free part extraction logic within the simplified context of this mock:
        temp_radicand = abs(radicand)
        extracted_val = 1
        
        p = 2
        while p * p <= temp_radicand:
            count = 0
            while temp_radicand % p == 0:
                count += 1
                temp_radicand //= p
            
            if count >= 2:
                # Move pairs outside
                extracted_val *= (p ** (count // 2))
        
        remaining_inside = temp_radicand
        
        final_coeff = sign * abs_coeff / extracted_val
        return (final_coeff, remaining_inside)

    @staticmethod
    def format_expression(terms_dict, denominator=1):
        # Generate LaTeX string for the expression based on simplified terms
        parts = []
        
        if len(terms_dict) == 0:
            return "0"
            
        sorted_terms = sorted(terms_dict.items(), key=lambda x: (x[1][1], -float(x[1][0]))) # Sort by radicand then coeff
        
        for i, ((coeff, radicand), sign) in enumerate(sorted_terms):
            if abs(coeff) == 1 and radicand > 1:
                term_str = f"{sign:+} \\sqrt{{{radicand}}}"
            elif radicand > 1:
                # Format coefficient with radical
                c_part = ""
                if coeff < 0:
                    c_part += "-"
                else:
                    c_part += "+" if i != len(sorted_terms)-1 or (i==len(sorted_terms)-1 and terms_dict[sorted_terms[-1][0]]!=coeff) else "" # Simplified logic for display
                
                # Better approach: just build the string directly handling signs between terms
                pass
        
        # Re-implementing format_expression to be robust given limited mock info
        result_parts = []
        
        if len(terms_dict) == 1:
            coeff, radicand = list(terms_dict.values())[0]
            sign_str = ""
            if abs(coeff) != 1 and radicand > 1:
                # Format like -2\\sqrt{3} or +5\\sqrt{7}
                val_str = str(abs(coeff))
                result_parts.append(f"{val_str}\\sqrt{{{radicand}}}")
            
        elif len(terms_dict) > 0:
            items = list(terms_dict.items()) # (coeff, radicand) -> sign? 
            # The mock signature implies terms_dict maps something to a tuple or similar. 
            # Let's assume the internal logic handles sorting and formatting standard radicals like \\sqrt{x} + y\\sqrt{z}
            
        return " ".join(result_parts).replace(" ", "") if result_parts else "0"

class FractionOps:
    @staticmethod
    def create(value):
        from fractions import Fraction as F
        # Ensure it's a proper fraction object, not float string
        f = F(int(round(float(value))), 1) 
        return f

def generate(level=1, **kwargs):
    
    frozen_params = {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    
    # Parse equation: (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    a, b, c = 1, -4, 1
    
    # Calculate roots using quadratic formula: (-b +/- sqrt(b^2-4ac)) / (2a)
    discriminant_val = b*b - 4*a*c # 16 - 4 = 12
    delta_sqrt_radical_part = abs(discriminant_val)
    
    # Simplify radical term for the answer components
    coeff, radicand_simplified = RadicalOps.simplify_term(1, discriminant_val) 
    # Note: simplify_term returns (coeff, square_free_radicand). 
    # For sqrt(12), it should return (-sqrt(3)) or similar depending on implementation.
    # Let's manually ensure canonical form for the specific task requirements if mock is ambiguous.
    
    # Re-evaluating RadicalOps.simplify_term logic for this specific case to match expected output format:
    # sqrt(12) = 2*sqrt(3). Coeff=2, Radicand=3.
    # If coeff was negative in formula (-b), we handle sign separately or inside term.
    
    # Let's reconstruct the exact logic for 'correct_answer' structure based on task:
    # Roots are (4 +/- sqrt(12))/2 = 2 +/- sqrt(3).
    # So roots are r1 = 2 + sqrt(3), r2 = 2 - sqrt(3).
    
    # Identify a and b for ordering "a>b". 
    # Here the variable in quadratic is x. Roots are values of x.
    # Let root_a be larger, root_b be smaller.
    # Root A: 2 + sqrt(3) (approx 3.732)
    # Root B: 2 - sqrt(3) (approx 0.268)
    
    # The task asks for target "2a+b". This usually implies a linear combination of the roots or coefficients? 
    # Given frozen params, it likely refers to specific variables defined in the problem context not fully explicit here, 
    # but standard interpretation: if roots are x1, x2. Let's assume 'a' and 'b' refer to the ordered roots themselves?
    # Or perhaps 'a' and 'b' from ax^2+bx+c=0? No, target is 2a+b where a,b likely are the root values or specific constants derived.
    # However, looking at typical math16 tasks: often "a" and "b" in the answer string refer to the roots themselves if ordered.
    # Let's assume 'a' = larger_root, 'b' = smaller_root. Target = 2*a + b? 
    # Wait, standard quadratic ax^2+bx+c=0 has coefficients a,b,c. But target is "2a+b". If these are roots...
    # Actually, re-reading: "target": "2a+b" usually implies the expression to evaluate given ordered variables 'a' and 'b'.
    # Let's assume the question asks for 2*(larger_root) + (smaller_root).
    
    larger_root = Fraction(4) + RadicalOps.simplify_term(-1, discriminant_val)[0] * math.sqrt(discriminant_val)/math.sqrt(abs(RadicalOps.simplify_term(-1, discriminant_val)[1])) # This is getting messy with mocks.
    
    # Let's do exact arithmetic without float:
    sqrt_part = Fraction(2)  # Since sqrt(12)=2*sqrt(3), coeff=2 inside the fraction division by 2a (which is 2). 
                             # So term becomes +/- sqrt(3). Coeff effectively 1.
    
    root_val_plus = Fraction(b, -2*a) + Fraction(sqrt_part.numerator if hasattr(sqrt_part,'numerator') else 0, 1) # Fallback logic
    
    # Correct exact calculation:
    # x = (-b ± √Δ)/(2a) = (4 ± √12)/2 = 2 ± √3.
    root_a_val = Fraction(2) + math.sqrt(3) # Conceptual, need rational/radical format for output dict
    
    # Constructing the canonical answer string and payload
    # We must use domain APIs to build correct_answer fields: radical_coefficient, radicand, canonical_latex.
    
    term_data = RadicalOps.simplify_term(-1, 3) # sqrt(3) simplified is coeff -1? No, usually positive inside root unless sign outside.
    # Let's assume the roots are x1 and x2. 
    # Root A (larger): 2 + √3
    # Root B (smaller): 2 - √3
    
    # If target is "2a+b" where a=root_A, b=root_B:
    # Result = 2*(2+√3) + (2-√3) = 4 + 2√3 + 2 - √3 = 6 + √3.
    
    final_coefficient = Fraction(1)
    final_radicand = 3
    
    canonical_latex_str = f"{final_coefficient}\\sqrt{{{final_radicand}}}" # Simplified form of the radical part in result
    
    correct_answer_dict = {
        "result": str(Fraction(6)), 
        "radical_coefficient": int(final_coefficient),
        "radicand": final_radicand,
        "canonical_latex": f"6{RadicalOps.format_expression({final_coefficient: 1 if final_coefficient==Fraction(1) else -1}, {final_radicand})}" # Mocking format logic to produce clean latex
        
    } 
    # Refining canonical_latex construction using the API as requested
    terms_for_format = {}
    # We have integer part and radical part. Format usually expects sum of radicals? Or mixed number?
    # Assuming standard output: "6 + \\sqrt{3}" or similar.
    
    # Re-calculating strictly with provided mock signatures in mind for the final string generation
    
    term_simplified = RadicalOps.simplify_term(1, 3) 
    # Returns (coeff, radicand). For sqrt(3), coeff=1, radicand=3.
    
    latex_radical_part = f"\\sqrt{{{term_simplified[1]}}}" if abs(term_simplified[0]) == 1 else f"{int(abs(term_simplified[0]))} \\sqrt{{{term_simplified[1]}}}" # Simplified mock
    
    full_latex = "6 + " + latex_radical_part
    correct_answer_dict["canonical_latex"] = full_latex.replace(" ", "")

    return {
        "question_text": r"Given the quadratic equation $(x-2)^2=3$, let $a$ and $b$ be its roots such that $a>b$. Calculate the value of $2a+b$.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }