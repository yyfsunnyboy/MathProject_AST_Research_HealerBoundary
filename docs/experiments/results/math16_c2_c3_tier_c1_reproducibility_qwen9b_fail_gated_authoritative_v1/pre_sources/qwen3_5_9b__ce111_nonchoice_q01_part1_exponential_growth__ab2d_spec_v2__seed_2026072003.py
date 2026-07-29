# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per task specification
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Convert days to total available hours using native Python arithmetic
    total_hours = days * 24
    
    # Compute the number of complete generations (k)
    # k is the integer part of floor(total_hours / hours_per_generation)
    k = total_hours // hours_per_generation
    
    correct_answer = {"k": k}
    
    question_text = r"Given an initial population of $1$ and a split factor of $4$, with generations occurring every $\text{hours\_per\_generation}$ hours over $\text{days}$ days, calculate the number of complete generations that can occur. Use 24 hours per day."
    
    oracle_payload = {"days": days, "hours_per_generation": hours_per_generation, "initial": initial, "split_factor": split_factor}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }