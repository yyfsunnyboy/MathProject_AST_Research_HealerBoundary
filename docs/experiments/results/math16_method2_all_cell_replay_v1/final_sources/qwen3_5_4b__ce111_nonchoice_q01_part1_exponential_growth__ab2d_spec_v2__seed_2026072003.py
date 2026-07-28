# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per task specification
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Convert total time to generations (integer division)
    total_hours = days * 24
    k = total_hours // hours_per_generation
    
    correct_answer = {"k": k}
    
    question_text = r"An organism starts with a population of $initial$ individuals. Each generation, the population splits into $split\_factor$ times its previous size. If each generation takes $hours\_per\_generation$ hours and there are $days$ days total, how many complete generations ($k$) occur?"
    
    oracle_payload = {
        "days": days,
        "hours_per_generation": hours_per_generation,
        "initial": initial,
        "split_factor": split_factor
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }