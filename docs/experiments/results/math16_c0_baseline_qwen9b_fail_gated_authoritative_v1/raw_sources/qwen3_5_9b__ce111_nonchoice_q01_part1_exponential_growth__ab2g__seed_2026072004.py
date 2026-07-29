def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations: (total_hours) / hours_per_generation
    total_days = frozen_params["days"]
    days_in_hours = total_days * 24
    num_generations = int(days_in_hours // frozen_params["hours_per_generation"])
    
    # Exponential growth formula: final = initial * (split_factor ^ generations)
    initial = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    k = initial * (split_factor ** num_generations)
    
    question_text = f"Starting with {frozen_params['initial']} bacteria, where each generation takes {frozen_params['hours_per_generation']} hours and the population splits by a factor of {frozen_params['split_factor']}, how many bacteria will there be after {frozen_params['days']} days? Express your answer as an integer."
    
    correct_answer = {"k": k}
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }