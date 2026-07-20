def generate(level=1, **kwargs):
    import json
    
    # Frozen sampled parameters from task specification
    params = {
        "days": 15, 
        "hours_per_generation": 20, 
        "initial": 1, 
        "split_factor": 4
    }
    
    days = params["days"]
    hours_per_gen = params["hours_per_generation"]
    initial_pop = params["initial"]
    split_factor = params["split_factor"]
    
    # Calculate total generations based on the problem context (assuming a standard day cycle or direct conversion)
    # Given 'days' and 'hours_per_generation', we calculate how many generations occur in those days.
    # Assuming 24 hours per day:
    total_hours = days * 24
    num_generations = int(total_hours / hours_per_gen)
    
    if initial_pop == 0 or split_factor <= 1:
        final_count = initial_pop
    else:
        final_count = initial_pop * (split_factor ** num_generations)
        
    # Ensure k is an integer as per contract
    k = int(final_count)
    
    question_text = f"Starting with {initial_pop} organisms, if each generation takes {hours_per_gen} hours to complete and the population splits by a factor of {split_factor}, what is the total count after {days} days? Assume 24 hours per day."
    
    correct_answer = {"k": k}
    
    oracle_payload = params
    
    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": oracle_payload
    }