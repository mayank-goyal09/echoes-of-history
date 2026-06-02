import os
import json
from engine import HistoricalEngine

def load_config():
    if not os.path.exists('persona_config.json'):
        with open('persona_config.json', 'w') as f:
            json.dump({}, f)
    with open('persona_config.json', 'r') as f:
        return json.load(f)

def save_config(config):
    with open('persona_config.json', 'w') as f:
        json.dump(config, f, indent=4)

def main():
    print("🚀 Historical Persona Engine: System Booting...")
    config = load_config()
    source_dir = "./source_data"
    
    # 1. Ensure source directory exists
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        print(f"📁 Created {source_dir}. Add your folders (e.g., /Grandfather) there!")
        return

    # 2. Scan for new personas
    folders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
    
    for folder in folders:
        if folder not in config:
            print(f"✨ New Persona Detected: [{folder}]. Initiating Autonomous Profiling...")
            
            # Temporary engine for ingestion
            temp_engine = HistoricalEngine() 
            sample_text = temp_engine.ingest_new_persona(folder)
            
            # AI generates the 'Soul' (Persona Details)
            print(f"🧠 {folder} is being analyzed by the AI...")
            persona_details = temp_engine.auto_profile(sample_text)
            
            # Save it to our registry
            config[folder] = persona_details
            save_config(config)
            print(f"✅ Persona Registry Updated for {folder}!")

    # 3. Selection Menu
    print("\n--- Available Historical Personas ---")
    for i, p in enumerate(config.keys()):
        print(f"{i+1}. {config[p]['name']}")
    
    choice = int(input("\nSelect a persona to chat with (number): ")) - 1
    selected_id = list(config.keys())[choice]
    persona = config[selected_id]

    # 4. Start the Chat Engine
    engine = HistoricalEngine(selected_id)
    print(f"\n🎩 Entering the era of {persona.get('era', 'the past')}...")
    print(f"--- Chatting with {persona['name']} (Type 'exit' to stop) ---\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        response = engine.ask(user_input, persona)
        print(f"\n{persona['name']}: {response}\n")

if __name__ == "__main__":
    main()