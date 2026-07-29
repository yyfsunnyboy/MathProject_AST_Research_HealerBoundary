def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135) if "radicand" in kwargs else 135
    
    import math
    
    def simplify_radical(n):
        """Simplify the radical n."""
        temp_n = int(abs(float(n)))
        
        # Find all divisors of temp_n to check for perfect squares
        max_divisor = int(math.sqrt(temp_n)) + 1
        
        for i in range(2, max_divisor + 1):
            if temp_n % i == 0:
                divisor_a = i
                divisor_b = temp_n // i
                
                # Check both divisors and their pairs to find the largest perfect square factor
                factors_to_check = [divisor_a, divisor_b]
                
                for d in factors_to_check:
                    if math.isqrt(d) ** 2 == d:
                        return simplify_radical(temp_n // (d * math.sqrt(d))) # This logic is recursive and slightly flawed for direct extraction. Let's use a cleaner approach below.

    def get_largest_square_factor(n):
        """Returns the largest perfect square factor of n."""
        max_sq = 1
        i = int(math.isqrt(n))
        while i > 0:
            if math.isqrt(i) ** 2 == i and (n % i) == 0: # Check if i is a perfect square AND divides n
                return i, n // i
            
            i -= 1
        
        return max_sq, n

    def simplify(n):
        """Simplify the radical expression."""
        largest_square_factor, remaining = get_largest_square_factor(int(abs(float(n))))
        
        coefficient = math.isqrt(largest_square_factor)
        radicand_simplified = int(remaining) if isinstance(remaining, int) else float(remaining).is_integer() and int(remaining) or str(round(float(remaining))) # Ensure it's an integer
        
        return {
            "coefficient": coefficient,
            "radicand": radicand_simplified,
            "canonical_latex": f"{coefficient}\\sqrt{{{int(radicand_simplified)}}}}" if not isinstance(coefficient, int) or not isinstance(radicand_simplified, int) else str(int(coefficient)) + "\\sqrt{" + str(int(radicand_simplified)) + "}" # Fix logic for latex
        }

    # Corrected Simplification Logic
    n = radicand
    
    if n < 0:
        return {
            "coefficient": -1,
            "radicand": abs(n),
            "canonical_latex": "-\\sqrt{" + str(int(abs(float(n)))) + "}"
        }

    # Find largest square factor k such that n = k * m and k is a perfect square
    max_k = 1
    
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % (i*i) == 0:
            max_k = i*i
            
    coefficient = math.sqrt(max_k).astype(int) # Convert to int safely
    radicand_final = int((n / float(max_k)))

    latex_str = f"{coefficient}\\sqrt{{{radicand_final}}}" if isinstance(coefficient, (int, float)) and not isinstance(radicand_final, str) else "Error"

    return {
        "question_text": r"$\text{Simplify the radical: } \sqrt{\overline{" + str(n) + "}"}$",
        "correct_answer": latex_str if isinstance(latex_str, str) and not (isinstance(coefficient, float)) else f"{int(coefficient)}\\sqrt{{{radicand_final}}}", # Ensure int types for safety in string representation logic used below
        "oracle_payload": {"radicand": n}
    }

# Re-implementing the core math cleanly to ensure correctness without recursion issues or type errors
    
def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135) if "radicand" in kwargs else 135
    n = int(radicand)

    # Handle negative numbers explicitly for the coefficient sign
    is_negative = False
    abs_n = abs(n)
    
    if abs_n < 0:
        pass
    
    # Find largest perfect square factor of abs_n
    max_sq_factor = 1
    i = int(math.isqrt(abs_n))
    while i > 0:
        sq_val = i * i
        if abs_n % sq_val == 0:
            max_sq_factor = sq_val
        else:
            # If not divisible, try smaller factors? No, we just need the largest square factor.
            # Actually, iterating down from sqrt(n) is efficient enough for small numbers like 135.
            pass
        i -= 1
    
    coefficient = int(math.sqrt(max_sq_factor))
    radicand_simplified = abs_n // max_sq_factor

    if n < 0:
        latex_ans = f"-{coefficient}\\sqrt{{{radicand_simplified}}}"
    else:
        latex_ans = f"{coefficient}\\sqrt{{{radicand_simplified}}}"

    return {
        "question_text": r"$\text{Simplify the radical: } \sqrt{\overline{" + str(n) + "}"}$",
        "correct_answer": latex_ans,
        "oracle_payload": {"radicand": n}
    }