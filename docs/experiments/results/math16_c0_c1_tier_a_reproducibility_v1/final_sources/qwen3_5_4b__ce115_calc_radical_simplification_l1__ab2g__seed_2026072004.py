def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27) if "radicand" in kwargs else 27
    
    import math
    
    def simplify_radical(n):
        """Simplify the radical n."""
        # Find largest perfect square factor of n
        i = int(math.sqrt(n))
        while i > 0:
            root, remainder = divmod(i * i, n)
            if remainder == 0:
                coefficient = root
                simplified_radicand = n // (i * i)
                break
            i -= 1
        
        # If no perfect square factor found other than 1*1
        if not isinstance(coefficient, int):
            return "n", radicand
            
        canonical_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"
        
    simplified_n, final_radicand = simplify_radical(radicand)
    
    question_text = r"$$\text{Simplify the radical: } \sqrt{\overline{{radicand}}}$$"
    correct_answer = f"{final_radicand}, {simplified_n}"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"radicand": radicand}
    }