from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }
    
    total_hours = frozen_params["days"] * 24
    
    if total_hours % frozen_params["hours_per_generation"] != 0:
        raise ValueError("Total hours must be divisible by generation time")
        
    k = IntegerOps.sub(total_hours, (total_hours // frozen_params["hours_per_generation"]) * frozen_params["hours_per_generation"])
    
    # Actually we need integer division for the count of generations directly if logic holds
    # But let's re-calculate strictly: 
    # The problem states "After 15 days... total cells can be written as 4^k".
    # This implies k is the number of doublings (generations).
    # However, the processing steps say: 3) k = total_hours // hours_per_generation.
    # Let's follow step 3 exactly for calculation logic even if mathematically it represents generations count directly.
    
    num_generations = IntegerOps.sub(total_hours, ((total_hours // frozen_params["hours_per_generation"]) * frozen_params["hours_per_generation"])) 
    # Wait, the above line is wrong implementation of division check.
    # Correct integer division:
    k_val = total_hours // frozen_params["hours_per_generation"]
    
    return {
        "question_text": "從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。",
        "correct_answer": {"k": k_val},
        "oracle_payload": frozen_params
    }