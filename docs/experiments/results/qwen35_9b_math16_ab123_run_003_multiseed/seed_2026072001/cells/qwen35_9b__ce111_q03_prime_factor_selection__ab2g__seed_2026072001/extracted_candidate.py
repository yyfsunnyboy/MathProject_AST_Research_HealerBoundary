def generate(level=1, **kwargs):
    question_text = r"Select a prime factor of $n$. Given candidates $\{c_0, c_1, \dots\}$ where each $c_i$ is an integer from the provided list, identify which one divides $n$ evenly. Let $n = 156$ and the candidate set be $\mathcal{C} = [11, 12, 13, 14]$. Which element of $\mathcal{C}$ is a prime factor of $n$?"
    correct_answer = 13
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }