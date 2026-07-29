# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per specification
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Convert days to total hours using native Python arithmetic
    total_hours = days * 24
    
    # Compute k: the number of complete generations (floor division)
    k = total_hours // hours_per_generation
    
    question_text = r"Given an initial population of $1$ and a split factor of $4$, with one generation occurring every $\text{hours\_per\_generation}$ hours, how many complete generations occur in $\text{days}$ days? (Total time is converted to hours using 24 hours per day.) Calculate the number of complete generations $k = \lfloor \frac{\text{total\_hours}}{\text{hours\_per\_generation}} \rfloor$."
    
    correct_answer = {"k": k}
    oracle_payload = {
        "days": days,
        "hours_per_generation": hours_per_generation,
        "initial": initial,
        "split_factor": split_factor
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }