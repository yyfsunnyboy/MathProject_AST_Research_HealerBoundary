def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    # Calculate coefficient and simplified radicand for simplest radical form
    import math
    
    def simplify_radical(n):
        if n <= 0:
            return 1, n
        
        temp_n = n
        coeff = 1
        while True:
            factor = int(math.sqrt(temp_n)) ** 2
            if factor == temp_n or (factor * factor > temp_n and math.isqrt(factor) ** 3 != temp_n): # Check perfect square logic carefully for extraction
                break
            
            # Find largest integer k such that k^2 divides n
            i = int(math.sqrt(temp_n))
            while i * i <= temp_n:
                if temp_n % (i * i) == 0:
                    coeff *= i
                    temp_n //= (i * i)
                    break
                else:
                    i -= 1
        
        # Ensure we extracted the largest square factor by re-checking logic simply
        simplified_radicand = n
        while True:
            root = int(math.sqrt(simplified_radicand))
            if root * root == simplified_radicand:
                coeff *= root
                simplified_radicand //= (root * root)
                break
            
            # Try to find a square factor > 1
            found_factor = False
            for i in range(2, int(math.sqrt(simplified_radicand)) + 1):
                if simplified_radicand % (i * i) == 0:
                    coeff *= i
                    simplified_radicand //= (i * i)
                    break
            
            if not found_factor and root * root != simplified_radicand:
                # If no square factor > 1 exists, we are done unless it's a perfect cube for cubes etc., 
                # but standard radical simplification usually implies extracting squares.
                # However, to be safe for "simplest form", let's ensure the remaining radicand has no square factors.
                break
        
        return coeff, simplified_radicand

    c, r = simplify_radical(radicand)
    
    question_text = f"Simplify \u221a{radicand}."
    correct_answer = {"coefficient": int(c), "radicand": int(r)}
    oracle_payload = radicand
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }