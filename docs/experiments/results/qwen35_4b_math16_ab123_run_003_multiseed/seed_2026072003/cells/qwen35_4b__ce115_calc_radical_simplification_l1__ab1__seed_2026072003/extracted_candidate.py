def generate(level=1, **kwargs):
    radicals = kwargs.get('radicals', [27])
    
    if level == 1:
        radicand = 27
        
        # Simplify radical mathematically
        import math
        factors = []
        temp = int(radicand)
        
        for i in range(2, int(temp**0.5)+1):
            while temp % (i*i) == 0:
                count = 0
                d = i
                t = radicand
                while t % (d*d) == 0:
                    factors.append(d)
                    t //= (d*d)
        
        # Calculate coefficient and final radicand
        coeff_prod = math.prod(factors) if factors else int(radicand)**(1/3)
        final_radicand = int((radicand / (coeff_prod**2))**(1/3)) * 0.5
        
        # Proper simplification logic for cube root of 27
        coeff = 3
        remaining_rad = radicand // (coeff ** 2)
        
        question_text = r"\text{Simplify the radical: } \sqrt[3]{\text{" + str(radicand) + "}}"
        
    else:
        raise NotImplementedError("Level not supported")

    correct_answer_dict = {
        'coefficient': int(coeff),
        'radicand': remaining_rad,
        'canonical_latex': r"3 \sqrt[3]{\text{" + str(remaining_rad) + "}}"
    }

    return {
        'question_text': question_text,
        'correct_answer': correct_answer_dict,
        'oracle_payload': radicals
    }