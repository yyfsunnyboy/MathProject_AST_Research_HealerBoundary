from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }
    
    # Calculate total hours elapsed: days * hours per generation
    total_hours = IntegerOps.add(IntegerOps.mul(frozen_params["days"], frozen_params["hours_per_generation"]), 0)
    
    # Each generation takes hours_per_generation. Number of generations is floor(total_hours / hours_per_generation).
    # Since the problem states "every 20 hours", we divide by 20 directly if total_hours matches exactly, 
    # but generally it's ceil or exact division depending on interpretation. 
    # Given discrete steps: number of generations = (total_hours // hours_per_generation) + 1?
    # Actually, let's re-read carefully: "Every 20 hours...". Starting at t=0 with n=1.
    # At t=20h -> gen 1 done. At t=40h -> gen 2 done. ...
    # Total time = days * 24? Or is the problem using a non-standard day definition where "day" aligns with generations?
    # Wait, standard biology: 1 day = 24 hours. 
    # But let's look at the math structure implied by exponential growth problems in this context (Math16).
    # Usually these are simplified models or specific to a curriculum.
    # Let's calculate total hours first assuming 1 day = 24h? Or is "day" just a unit here equal to generation time?
    # Re-reading: "Every 20 hours...". If it takes 20 hours per gen, then in 15 days (assuming 24h/day), total hours = 360. 
    # Generations = floor(360 / 20) + 1? Or just count of full generations passed?
    # However, often in these generated tasks, the "day" might be defined such that it aligns with the split factor or time unit given.
    # Let's assume standard 24h/day unless context implies otherwise. 
    # But wait, if I calculate k from 1 * 4^k = N, then k is log_4(N).
    # If total hours = days * 24? Then generations = (days*24)/20 = 360/20 = 18. 
    # Start with 1 cell at t=0. After 1st gen (t=20), count is 4^1.
    # So after G generations, count is 4^G.
    # If total time T hours, and period P=20h. Number of periods = floor(T/P)? Or ceil? 
    # "After 15 days". Usually implies the state at t=end_of_15_days.
    # Let's assume standard conversion: 1 day = 24 hours. Total hours = 360. Generations = 360/20 = 18 exactly? 
    # If so, k=18.
    
    # Alternative interpretation for Math16 generated tasks: Sometimes "day" is a placeholder and the time units are consistent with the problem statement's logic without external constants like 24h/day unless specified. 
    # But here it explicitly says "hours_per_generation": 20. And asks about "days".
    # If we assume standard calendar days, k = (15 * 24) / 20 = 360/20 = 18.
    
    total_hours_val = IntegerOps.mul(frozen_params["days"], 24)
    generations_count = IntegerOps.div(total_hours_val, frozen_params["hours_per_generation"]) # Assuming exact division
    
    # The population starts at 1 (which is 4^0). After g generations, it's 4^g.
    # So k should be the number of generations completed? Or does "after" include partial? 
    # Given integer exponent form required, likely an integer result.
    
    correct_k = int(generations_count)
    
    question_text = f'從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。'
    
    return {
        "question_text": question_text,
        "correct_answer": {"k": correct_k},
        "oracle_payload": frozen_params
    }
