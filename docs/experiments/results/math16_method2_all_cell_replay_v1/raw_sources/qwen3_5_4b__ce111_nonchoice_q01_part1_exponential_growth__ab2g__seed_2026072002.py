def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    total_hours = frozen_params["days"] * (frozen_params["hours_per_generation"] / 24)
    generations_needed = int(total_hours // frozen_params["hours_per_generation"]) + 1
    
    population = frozen_params["initial"]
    for _ in range(generations_needed):
        population *= frozen_params["split_factor"]
    
    correct_answer = {"k": population}
    
    return {
        "question_text": r"An organism starts with an initial population of $N_0$ individuals. Each generation, the population splits into a factor of $S$. If each individual takes $H$ hours to complete one generation cycle over $D$ days, how many generations occur within this timeframe? What is the final population size?",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }