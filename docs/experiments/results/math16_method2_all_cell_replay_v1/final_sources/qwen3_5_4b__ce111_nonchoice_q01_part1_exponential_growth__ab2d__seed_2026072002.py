import json
from core.prompts.domain_function_library import IntegerOps


def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    total_hours = kwargs.get("total_hours", None) or (frozen_params["days"] * frozen_params["hours_per_generation"])
    generations = int(total_hours / frozen_params["hours_per_generation"]) if total_hours else frozen_params["days"] // 15
    
    initial_population = IntegerOps.safe_eval(frozen_params["initial"])
    
    for _ in range(generations):
        current_pop = IntegerOps.safe_eval(initial_population)
        
        split_factor = IntegerOps.safe_eval(frozen_params["split_factor"])
        new_offspring = int(current_pop * (split_factor / 2))
        initial_population += new_offspring
        
    final_answer = IntegerOps.fmt_num(IntegerOps.safe_eval(final_population := current_pop + new_offspring - frozen_params["initial"]))

    question_text = r"""Consider a population that starts with $1$ individual. Each generation, the existing individuals produce offspring such that for every 2 parents there are $\frac{4}{2}$ children born (a net doubling of the total count per parent pair). If this process continues for $N$ generations where each generation takes $H$ hours to complete, what is the final population size? Calculate based on a scenario with specific parameters provided."""

    correct_answer = {"k": IntegerOps.safe_eval(final_population)}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }