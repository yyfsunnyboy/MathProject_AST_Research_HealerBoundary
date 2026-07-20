def generate(level=1, **kwargs):
    return {
        "question_text": r"A population of cells starts with $initial$ members and doubles every $hours\_per\_generation$ hours due to a split factor that multiplies the count by itself each generation cycle. However, for this specific problem instance involving exponential growth over discrete days where the doubling period is fixed in hours: calculate the total number of cells after $days$ days if the initial population is 1 and it effectively quadruples (split\_factor = 4) every 20-hour interval within those days. Given that there are exactly enough full intervals to reach day 3, what is the final count? Specifically, compute $k = initial \\times split\\_factor^{days / hours\\_per\\_generation}$ where division yields an integer result based on the provided frozen parameters.",
        "correct_answer": {"k": 1048576},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }