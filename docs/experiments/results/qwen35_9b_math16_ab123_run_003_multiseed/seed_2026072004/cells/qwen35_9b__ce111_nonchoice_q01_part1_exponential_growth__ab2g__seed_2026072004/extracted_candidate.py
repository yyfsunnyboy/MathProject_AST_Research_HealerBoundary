def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    days = frozen_params["days"]
    hours_per_gen = frozen_params["hours_per_generation"]
    initial_pop = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]

    total_hours = days * 24
    num_generations = int(total_hours / hours_per_gen)
    
    if num_generations < 0:
        num_generations = 0
        
    final_population = initial_pop * (split_factor ** num_generations)

    question_text = f"An organism starts with an initial population of {initial_pop} and splits every {hours_per_gen} hours. After a period of {days} days, what is the total population? Assume each split multiplies the current count by the split factor."
    
    correct_answer = {"k": int(final_population)}

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }