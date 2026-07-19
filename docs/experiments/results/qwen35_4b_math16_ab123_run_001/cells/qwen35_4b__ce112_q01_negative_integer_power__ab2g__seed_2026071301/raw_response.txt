def generate(level=1, **kwargs):
    question_text = r"In mathematics, a negative integer power is defined as $(-b)^n$, where $b$ is a positive base and $n$ is an exponent.\n\nWhat is the value of $(-3)^3$?"
    
    frozen_params = {"base": -3, "exponent": 3}
    
    correct_answer = (-frozen_params["base"]) ** frozen_params["exponent"] if isinstance(frozen_params["base"], int) else float((-float(frozen_params["base"])) ** frozen_params["exponent"])

return {
"question_text": question_text,
"correct_answer": int(correct_answer),
"oracle_payload": frozen_params
}