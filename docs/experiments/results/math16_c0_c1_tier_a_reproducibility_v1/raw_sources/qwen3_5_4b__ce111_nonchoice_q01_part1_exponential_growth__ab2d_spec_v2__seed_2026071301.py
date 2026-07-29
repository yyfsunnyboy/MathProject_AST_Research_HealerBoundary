# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per task specification
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Convert total time to generations based on the rule: k is the number of complete generations.
    # Total available time in hours = days * 24
    total_hours_available = days * 24
    
    # Calculate maximum possible generations (integer division)
    max_generations_possible = total_hours_available // hours_per_generation
    
    # Determine k based on task specification: "k is the exponent of split_factor" and context implies growth count.
    # The problem asks for exponential growth generation count, where each step multiplies by split_factor.
    # Given 'days' (15) and 'hours_per_generation' (20), we calculate how many generations fit in 15 days.
    # k = floor((15 * 24) / 20) = floor(360 / 20) = 18
    
    k = max_generations_possible

    correct_answer = {"k": k}
    
    question_text = r"An organism starts with a population of $initial$ individuals. Each generation, the population splits into $split\_factor$ times its previous size. If each generation takes $hours\_per\_generation$ hours and there are $days$ days available, what is the value of $k$, representing the number of complete generations that can occur?"

    oracle_payload = {
        "days": 15, 
        "hours_per_generation": 20, 
        "initial": 1, 
        "split_factor": 4
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }