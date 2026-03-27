import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_process_instance(states: List[Dict[str, Any]], start_time: datetime) -> List[Dict[str, Any]]:
    """
    Generate a process instance by traversing through states starting from the initial state.
    
    Args:
        states: List of state definitions with name, initial, min_time, max_time, odds_of_complete, and next_states
        start_time: Starting timestamp for the process instance
    
    Returns:
        List of dictionaries representing the process instance events
    """
    instance = []
    current_time = start_time
    
    # Find initial state
    current_state = next((s for s in states if s["initial"]), None)
    if not current_state:
        return instance
    
    while current_state:
        # Add event for current state
        duration = random.randint(current_state["min_time"], current_state["max_time"])
        current_time += timedelta(seconds=duration)
        event = {
            "name": current_state["name"],
            "timestamp": current_time.isoformat(),
        }
        instance.append(event)
        
        # Check if process completes
        if random.random() < current_state["odds_of_complete"]:
            break
        
        # Move to next state
        if current_state["next_states"]:
            next_state_choice = random.random()
            cumulative_odds = 0
            next_state_name = None
            
            for next_state in current_state["next_states"]:
                cumulative_odds += next_state["odds"]
                if next_state_choice < cumulative_odds:
                    next_state_name = next_state["name"]
                    break
            
            current_state = next((s for s in states if s["name"] == next_state_name), None)
        else:
            break
    
    return instance


def generate_json_objects(count: int, 
        name_prefix: str = "OBJ", name_seperator: str = "", name_offset_max: int = 5, 
        created_at: datetime = None, created_at_offset_max: int = 0,
        states: List[Dict[str, Any]] = [
            {"name": "StateA", "initial": True, "min_time": 10, "max_time": 35, "odds_of_complete": 0.2, "next_states": [{"name": "StateB", "odds": 0.5}, {"name": "StateC", "odds": 0.5}]},
            {"name": "StateB", "initial": False, "min_time": 30, "max_time": 180, "odds_of_complete": 0.3, "next_states": [{"name": "StateD", "odds": 1.0}]},
            {"name": "StateC", "initial": False, "min_time": 90, "max_time": 560, "odds_of_complete": 0.4, "next_states": [{"name": "StateA", "odds": 0.2}, {"name": "StateD", "odds": 0.8}]},
            {"name": "StateD", "initial": False, "min_time": 120, "max_time": 480, "odds_of_complete": 0.8, "next_states": [{"name": "StateB", "odds": 1.0}]}
        ]) -> List[Dict[str, Any]]:
    """
    Generate an array of JSON objects with uid, name, and created_at fields.
    
    Args:
        count: Number of objects to generate
        name_prefix: Prefix for the name field (defaults to "OBJ")
        name_seperator: Separator for the name field (defaults to "")
        name_offset_max: Maximum offset for the name field (defaults to 1)
        created_at: Datetime for the created_at field (defaults to current datetime)
        created_at_offset_max: Maximum offset for the created_at field (defaults to 0)

    Returns:
        List of dictionaries with uid, name, and created_at fields
    """
    objects = []
    name_id = 0
    if created_at is None:
        created_at = datetime.now()
    
    for i in range(count):
        name_id += random.randint(1, name_offset_max)
        created_at_with_offset = created_at + timedelta(seconds=random.randint(0, created_at_offset_max))
        obj = {
            "uid": None,
            "name": f"{name_prefix}{name_seperator}{name_id}",
            "created_at": created_at_with_offset.isoformat(),
            "states": generate_process_instance(states, created_at_with_offset)
        }
        objects.append(obj)
    
    return objects

if __name__ == "__main__":
    # Example usage
    generated_objects = generate_json_objects(count=10)
    print(json.dumps(generated_objects, indent=4))