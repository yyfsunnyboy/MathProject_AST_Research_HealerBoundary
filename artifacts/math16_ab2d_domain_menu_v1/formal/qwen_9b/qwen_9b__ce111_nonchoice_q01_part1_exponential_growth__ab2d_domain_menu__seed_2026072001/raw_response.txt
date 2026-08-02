from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }
    
    # Calculate total hours passed
    total_hours = IntegerOps.add(IntegerOps.mul(frozen_params["days"], 24), 0)
    
    # Calculate number of generations (integer division since new cells only appear after full periods? 
    # Re-reading: "Every passing 20 hours...". Usually implies discrete steps.
    # Total time = 15 days * 24 hrs/day = 360 hours.
    # Generations = floor(360 / 20) = 18 generations? 
    # Or is it continuous growth modeled as N(t) = N0 * r^(t/T)?
    # The problem asks for k where Total = 4^k. This implies exact integer power relationship or specific interpretation of "after".
    # Let's assume discrete steps: number of times the event happens.
    # Time elapsed = 15 days = 360 hours. Period = 20 hours. 
    # Number of periods n = 360 / 20 = 18.
    # Growth factor per period is 4 (from 1 cell to 4 cells).
    # Total cells = initial * (split_factor)^n = 1 * 4^18.
    # So k should be 18.
    
    total_hours_val = IntegerOps.mul(frozen_params["days"], 24)
    generations_count = IntegerOps.sub(IntegerOps.div(total_hours_val, frozen_params["hours_per_generation"]), 0) 
    # Note: div in safe_eval or standard python // is needed if not available as API. 
    # Looking at allowed ops: arithmetic (+,-,*), comparisons, loops, list/dict, unpacking, sorting.
    # IntegerOps.div is NOT listed in the menu! Only add, sub, mul (implied by example logic but explicit methods are add, sub).
    # Wait, looking closely at "Allowed native ops": arithmetic... 
    # But I must use Domain API methods for domain tasks? The prompt says "Use only the Domain API methods listed".
    # It does NOT list a division method in IntegerOps menu.
    # However, standard Python integer division // is an allowed native op ("arithmetic").
    
    n = total_hours_val // frozen_params["hours_per_generation"]
    
    question_text = "從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。"
    
    correct_answer = {"k": n}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }