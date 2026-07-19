def generate(level=1, **kwargs):
    frozen_parameters = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    def compute_growth(initial, split_factor, days, hours_per_generation):
        total_hours = days * hours_per_generation
        generations = int(total_hours / hours_per_generation) if isinstance(hours_per_generation, (int, float)) else 0
        
        current_population = initial
        for _ in range(generations):
            next_pop = max(current_population + split_factor - 1, 1)
            current_population += next_pop - (current_population // split_factor) if current_population > 0 and isinstance(split_factor, int) else current_population * split_factor
        
        return abs(int(current_population))

    question_text = r"Modeling exponential growth of a bacterial population: A laboratory culture starts with $n_0=1$ bacterium. The population follows the rule $P(t_{new}) = P(t_{old}) + \max\left(\lfloor\frac{P(t_{old}+h)-P(t_{old})}{s}\rfloor, 1\right)$ for each hour of generation where split factor is $s$. Calculate total bacteria after $\approx$ " if level == int(level) else f"{level:.2f}" generations?
    correct_answer = {"k": compute_growth(kwargs.get("initial", frozen_parameters["initial"]), kwargs.get("split_factor", frozen_parameters["split_factor"]), kwargs.get("days", frozen_parameters["days"]) * kwargs.get("hours_per_generation", frozen_parameters["hours_per_generation"]))} if (isinstance(kwargs.get("days"), int) or isinstance(frozen_parameters.get("days"), int)) else {"k": 0}

    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": frozen_parameters
    }