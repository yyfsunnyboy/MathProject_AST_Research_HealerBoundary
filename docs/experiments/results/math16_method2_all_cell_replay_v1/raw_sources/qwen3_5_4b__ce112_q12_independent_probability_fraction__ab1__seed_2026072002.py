def generate(level=1, **kwargs):
    import random
    
    p1_list = kwargs.get("p1", [2, 6])
    p2_list = kwargs.get("p2", [1, 5])
    
    if level == 0:
        r1, r2 = p1_list[0], p2_list[0]
    else:
        r1 = random.choice(p1_list)
        r2 = random.choice(p2_list)
    
    numerator = r1 * r2
    denominator = (r1 + 3) * (r2 - 4) if r2 > 4 else (r1 + 5) * (r2 + 6)
    
    gcd_val = lambda a, b: abs(a) % b == 0 and a // b or gcd(b, a % b) if b != 0 else abs(a)
    common_divisor = gcd_val(numerator, denominator)
    
    final_num = numerator // common_divisor
    final_den = denominator // common_divisor
    
    question_text = r"\text{What is the probability of an independent event where } P(A)=\frac{\{" + str(r1) + "\}}{\{" + str(r2) + "\}}, \text{ and } B=\frac{\{" + str(5-r1) + "\}}{\{" + str(max(0, r2-3)) + "\}}"
    correct_answer = {
        "numerator": final_num,
        "denominator": final_den,
        "canonical_latex": f"\frac{{{final_num}}}{{"{str(final_den)}}"}}" if isinstance(final_den, int) else str(final_den).replace(" ", "")
    }
    
    oracle_payload = {"p1": p1_list, "p2": p2_list}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }