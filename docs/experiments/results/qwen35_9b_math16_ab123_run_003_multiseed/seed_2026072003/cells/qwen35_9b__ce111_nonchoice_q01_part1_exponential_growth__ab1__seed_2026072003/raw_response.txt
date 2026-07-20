def generate(level=1, **kwargs):
    question_text = r"A bacterial culture starts with 1 bacterium and divides every $h$ hours by a factor of $s$. Given that the initial count is $N_0$, the number of bacteria after $t$ days (where there are $d_h$ generations per day) can be modeled as $N(t) = N_0 \cdot s^{g}$, where $g$ is the total number of generations in $t$ days. Calculate the final population count if: initial ($N_0$) = 1, split factor ($s$) = 4, hours per generation ($h$) = 20, and duration ($d_{days}$) = 15 days."
    correct_answer = {"k": 67108864}
    oracle_payload = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }