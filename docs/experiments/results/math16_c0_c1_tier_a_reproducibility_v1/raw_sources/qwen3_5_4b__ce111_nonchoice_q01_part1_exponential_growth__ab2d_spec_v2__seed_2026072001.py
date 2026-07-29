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
    # Given the frozen parameters, we calculate how many full cycles fit in 15 days with a 20-hour cycle.
    # 15 * 24 = 360 hours total available per day? No, "days": 15 usually means duration of simulation or observation window.
    # However, the task says "k is the number of complete generations". 
    # If we assume the process runs for 'days' amount of time where each generation takes 'hours_per_generation':
    # Total hours = days * 24? Or does 'days' represent something else?
    # Re-reading: "Convert days to hours using 24 hours per day." -> This implies total duration is days * 24.
    # k = floor((days * 24) / hours_per_generation)
    
    k = (days * 24) // hours_per_generation
    
    correct_answer = {"k": int(k)}
    
    question_text = r"""The population starts with $initial$ individuals and undergoes exponential growth. Each generation, the population splits by a factor of $split\_factor$. The process runs for a total duration of $days$ days, where each day has 24 hours, and one complete generation takes $hours\_per\_generation$ hours. Determine $k$, which represents the number of complete generations that can occur within this timeframe."""
    
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