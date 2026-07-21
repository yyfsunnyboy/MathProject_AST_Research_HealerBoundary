def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    total_hours = frozen_params["days"] * (frozen_params["hours_per_generation"] / 24)
    generations_needed = int(total_hours // frozen_params["hours_per_generation"]) + 1
    
    current_population = frozen_params["initial"]
    for _ in range(generations_needed):
        if current_population > 0:
            new_individuals = current_population * (frozen_params["split_factor"] - 1)
            current_population += new_individuals
            
    correct_answer_dict = {"k": int(current_population)}
    
    return {
        "question_text": r"An organism starts with a population of $initial$ individuals. Each generation, every individual splits into $split\_factor$ offspring (meaning the original plus $split\\_factor - 1$ new ones). If each generation takes $hours\\_{per}\\_generation}$ hours and we observe for $days$ days, what is the final population size?",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }