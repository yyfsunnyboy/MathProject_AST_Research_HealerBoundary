def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations: (total_hours) / hours_per_generation
    total_days = frozen_params["days"]
    days_in_hours = total_days * 24
    num_generations = int(days_in_hours // frozen_params["hours_per_generation"])
    
    # Initial population is given as 'initial'
    initial_pop = frozen_params["initial"]
    
    # Split factor (growth rate per generation)
    split_factor = frozen_params["split_factor"]
    
    # Calculate final population: P_final = P_initial * (split_factor ^ num_generations)
    k = int(initial_pop * (split_factor ** num_generations))
    
    question_text = r"""Calculate the total number of organisms after $d$ days, given that a new generation starts every $h$ hours. The population doubles according to a split factor $s$.

Parameters:
- Initial count ($P_0$): $\text{initial}$
- Days elapsed ($d$): $\text{days}$
- Hours per generation ($h$): $\text{hours\_per\_generation}$
- Split factor ($s$): $\text{split\_factor}$

Formula for number of generations $n$: $n = \lfloor \frac{24 \times d}{h} \rfloor$.
Final population formula: $P_n = P_0 \times s^n$.

Compute the final integer count."""
    
    correct_answer = {"k": k}
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }