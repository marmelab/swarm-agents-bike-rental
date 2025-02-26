from swarm.repl import run_demo_loop
from agents import triage_agent
from dotenv import load_dotenv
import database
load_dotenv()

# Initialize the database
database.initialize_database()

if __name__ == "__main__":
    run_demo_loop(triage_agent)
