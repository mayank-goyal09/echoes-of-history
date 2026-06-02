import os
from engine import HistoricalEngine

def run_tests():
    # 1. Define our persona mimicking the new UI config structure
    lincoln_persona = {
        "name": "Abraham Lincoln",
        "era": "19th Century America",
        "tone_description": "Humble, weary, and resolute. Uses words like 'four score', 'Union', 'reckon'.",
        "cutoff_year": "1865"
    }

    # 2. Initialize the engine
    print("Initializing engine...")
    engine = HistoricalEngine(persona_id="Abraham_Lincoln")

    # 3. Ask questions in sequence to test both Persona Boundaries and Memory!
    questions = [
        "Mr. Lincoln, tell me about your early life.",
        "That's interesting. So what was your primary goal?", # Tests memory!
        "Have you heard of a horseless carriage called a Tesla?" # Tests boundary!
    ]

    for q in questions:
        print("\n" + "="*50)
        print(f"User: {q}")
        response = engine.ask(question=q, persona_details=lincoln_persona)
        print(f"\nLincoln: {response}")

if __name__ == "__main__":
    run_tests()