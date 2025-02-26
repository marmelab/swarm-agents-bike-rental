import json
from dotenv import load_dotenv
from agents import *
from evals.eval_utils import run_function_evals
load_dotenv()

triage_test_cases = "evals/eval_cases/triage_cases.json"
welcome_test_cases = "evals/eval_cases/welcome_cases.json"
reservation_test_cases = "evals/eval_cases/reservation_cases.json"

n = 3

if __name__ == "__main__":
    # Run triage_agent evals
    with open(triage_test_cases, "r") as file:
        triage_test_cases = json.load(file)
    run_function_evals(
        triage_agent,
        triage_test_cases,
        n,
        eval_path="evals/eval_results/triage_evals.json",
    )

    # Run welcome_agent evals
    with open(welcome_test_cases, "r") as file:
        welcome_test_cases = json.load(file)
    run_function_evals(
        welcome_agent,
        welcome_test_cases,
        n,
        eval_path="evals/eval_results/welcome_evals.json",
    )

    # Run reservation_agent evals
    with open(reservation_test_cases, "r") as file:
        reservation_test_cases = json.load(file)
    run_function_evals(
        reservation_agent,
        reservation_test_cases,
        n,
        eval_path="evals/eval_results/reservation_evals.json",
    )