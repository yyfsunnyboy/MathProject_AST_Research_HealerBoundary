def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    radicand_value = frozen_params["radicand"]
    
    # Factorize radicand to simplify radical: sqrt(27) = sqrt(9*3) = 3*sqrt(3)
    simplified_coefficient = 1
    remaining_radicand = radicand_value
    
    for i in range(2, int(radicand_value ** 0.5) + 1):
        while remaining_radicand % (i * i) == 0:
            count = 0
            temp = remaining_radicand
            divisor = i
            while temp % divisor == 0:
                count += 2
                temp //= divisor
            
            if count > 0:
                simplified_coefficient *= (divisor ** (count // 2))
                # Remove the squared part from radicand for canonical form
                remaining_radicand = int(remaining_radicand / (i * i) ** (count // 2))
    
    # If no perfect square factors found other than 1, coefficient is 1 and radicand remains same
    if simplified_coefficient == 1:
        final_coefficient = 1
        final_radicand = remaining_radicand
    else:
        final_coefficient = simplified_coefficient
        # Recalculate remaining radicand properly by dividing out all square factors
        temp_n = radicand_value
        for i in range(2, int(temp_n ** 0.5) + 1):
            while temp_n % (i * i) == 0:
                count = 0
                divisor_sq = i * i
                while temp_n % divisor_sq == 0:
                    count += 1
                    temp_n //= divisor_sq
                if count > 0:
                    final_coefficient *= (i ** count)
        # Reconstruct remaining radicand from original divided by coefficient^2
        final_radicand = int(radicand_value / (final_coefficient * final_coefficient))

    canonical_latex = f"{final_coefficient}\\sqrt{{{final_radicand}}}" if final_coefficient != 1 else f"\\sqrt{{{radicand_value}}"
    
    question_text = r"Simplify the radical expression: $\\sqrt{" + str(radicand_value) + "}$."
    correct_answer_str = canonical_latex
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": frozen_params
    }