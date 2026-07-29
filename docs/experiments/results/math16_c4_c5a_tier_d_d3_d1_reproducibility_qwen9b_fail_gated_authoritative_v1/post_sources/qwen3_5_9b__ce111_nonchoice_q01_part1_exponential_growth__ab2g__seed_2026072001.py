def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations: (total hours) / (hours per generation)
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours // frozen_params["hours_per_generation"])
    
    # Calculate final count using exponential growth formula: initial * (split_factor ^ num_generations)
    k = frozen_params["initial"] * (frozen_params["split_factor"] ** num_generations)
    
    question_text = r"An organism starts with an initial population of $1$. It splits every $\text{hours\_per\_generation}$ hours. Given that the process runs for $\text{days}$ days, calculate the final population count $k$." \
                     .replace("initial", str(frozen_params["initial"])) \
                     .replace("split_factor", str(frozen_params["split_factor"])) \
                     .replace("hours_per_generation", str(frozen_params["hours_per_generation"])) \
                     .replace("days", str(frozen_params["days"]))
    
    return {
        "question_text": question_text,
        "correct_answer": {"k": k},
        "oracle_payload": frozen_params
    }