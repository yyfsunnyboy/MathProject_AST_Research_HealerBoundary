def generate(level=1, **kwargs):
    question_text = r"An initial population of 1 individual splits into 4 individuals each generation. If this process continues for $d$ generations with an additional growth factor of $h$ hours per generation (where the effective multiplier is determined by the split), what is the final count? Calculate based on: days=$\text{days}$, hours\_per\_generation=$\text{hours\_per_generation}$, initial=$\text{initial}$, split\_factor=$\text{split_factor}$. The total number of generations $d$ is calculated as $\lceil \frac{\text{days}}{24/\text{hours\_per\_generation}} \rceil$."
    
    days = kwargs.get("days", 15)
    hours_per_generation = kwargs.get("hours_per_generation", 20)
    initial = kwargs.get("initial", 1)
    split_factor = kwargs.get("split_factor", 4)

    generations_per_day = 24 / hours_per_generation
    
    total_generations = (days + generations_per_day - 1) // generations_per_day if generations_per_day > 0 else days * int(hours_per_generation/24)
    
    # Recalculate generatioons based on logic: 
    # If it takes H hours to do one generation, in D days we have floor(D*24/H) full generations.
    # Using ceiling for partial day completion if the problem implies "at least".
    # Let's stick to standard integer division with ceiling for safety as per common discrete math problems unless specified otherwise.
    
    g_per_day = 24 / hours_per_generation
    
    total_gen = int((days * g_per_day) + (1 - abs(0))) if days > 0 else 0 # Simplified logic: just calculate based on ratio
    
    # Re-evaluating the prompt's implied math for "exponential growth" with these specific params
    # Usually, simple exponential problems are: final = initial * split^generations
    # Let's compute generations precisely. 
    # If 20 hours per gen -> in one day (24h) we get ~1.2 gens? Or does it mean discrete steps?
    # Assuming continuous time to days conversion for the exponent base, but integer count of splits:
    
    num_days = int(days)
    max_hours_per_day = 24
    
    if hours_per_generation <= 0 or hours_per_generation > max_hours_per_day * (num_days + 1):
        # Fallback logic ensuring at least one gen if params are weird, but here they seem fine.
        pass
        
    # Calculate exact generations based on total available time vs per-gen cost
    # Total capacity = days * 24 hours
    effective_generations = int((num_days * max_hours_per_day) / hours_per_generation) + (1 if ((num_days * max_hours_per_day) % hours_per_generation > 0) else 0)

    k = initial * split_factor ** effective_generations
    
    correct_answer_json = {"k": k}
    
    oracle_payload = {
        "days": days, 
        "hours_per_generation": hours_per_generation, 
        "initial": initial, 
        "split_factor": split_factor
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_json,
        "oracle_payload": oracle_payload
    }