from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }
    
    total_hours = frozen_params["days"] * 24
    hours_per_gen = frozen_params["hours_per_generation"]
    generations = IntegerOps.safe_eval(f"{total_hours} // {hours_per_gen}")
    
    question_text = f"從 \\(1\\) 個細胞開始培養。每經過 \\({frozen_params['hours_per_generation']}\\) 小時，每個細胞分裂成 \\({frozen_params['split_factor']}\\) 個，且新細胞仍依相同規則繼續分裂。經過 \\({frozen_params['days']}\\) 天後，細胞總數可寫成 \\(4^k\\)，求 \\(k\\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": {"k": generations},
        "oracle_payload": frozen_params
    }