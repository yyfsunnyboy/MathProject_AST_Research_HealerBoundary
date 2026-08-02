from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }
    
    days = frozen_params["days"]
    hours_per_generation = frozen_params["hours_per_generation"]
    
    # Calculate total hours: days * 24
    total_hours = IntegerOps.safe_eval(f"{days} * 24")
    
    # Calculate generations: total_hours // hours_per_generation
    generations = IntegerOps.safe_eval(f"{total_hours} // {hours_per_generation}")
    
    # Since initial is 1 and split_factor is 4, the total cells is 4^generations.
    # Thus, k = generations.
    k = generations
    
    question_text = "從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": {"k": int(k)},
        "oracle_payload": frozen_params
    }