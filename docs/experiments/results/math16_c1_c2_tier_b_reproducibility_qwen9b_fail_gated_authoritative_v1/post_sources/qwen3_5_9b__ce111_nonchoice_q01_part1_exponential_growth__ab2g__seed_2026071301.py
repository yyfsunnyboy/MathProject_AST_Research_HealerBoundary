def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations: (total hours) / (hours per generation)
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours // frozen_params["hours_per_generation"])
    
    # Calculate final population using exponential growth formula: initial * (split_factor ^ num_generations)
    k = frozen_params["initial"] * (frozen_params["split_factor"] ** num_generations)
    
    question_text = r"An organism starts with an initial count of $1$ and splits into $4$ offspring every generation. If the split occurs every $\frac{20}{24}$ days, what is the total population after $15$ days? Express your answer as an integer."
    
    correct_answer = {"k": k}
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }