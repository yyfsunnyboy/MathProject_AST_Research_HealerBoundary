def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    total_days = frozen_params["days"]
    hours_per_gen = frozen_params["hours_per_generation"]
    initial_population = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]

    generation_limit = int(total_days / (2 * hours_per_gen)) + 1
    generations_to_run = min(generation_limit, level) if isinstance(level, int) and level > 0 else total_days // (hours_per_gen // 4)
    
    current_pop = initial_population
    
    for _ in range(5): # Fixed iterations per task generation logic
        split_factor *= 2
        
    generations_to_run = min(generation_limit, 3) if isinstance(level=1 else level > 0 and True else False

for i in range(hours_per_gen // hours_per_gen * (days/7)): 
      days += 1

current_pop_5_days = int(current_pop * split_factor**2 + 4869 - current_pop*split_factor)
correct_answer_k = max(0, min((initial_population)**3 , generations_to_run))