from datetime import datetime, timedelta
import json
import random
from typing import List, Dict, Any

from value_gen import *

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
        if "additional_fields" in current_state:
            for field in current_state["additional_fields"]:
                if field["type"] == "string_enum":
                    event = generated_string_enum_value(field, event)
                elif field["type"] == "integer_range":
                    event = generated_integer_range_value(field, event)
                elif field["type"] == "timestamp_range":
                    event = generated_timestamp_range_value(field, event, timestamp=current_time)
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
            {
                "name": "StateA", "initial": True, "min_time": 10, "max_time": 35, "odds_of_complete": 0.2, 
                "next_states": [{"name": "StateB", "odds": 0.5}, {"name": "StateC", "odds": 0.5}],
                "additional_fields": [{"type": "string_enum", "column_name": "sub_category", "values": [{"value": "X", "odds": 0.7}, {"value": "Y", "odds": 0.3}]}]
            },
            {
                "name": "StateB", "initial": False, "min_time": 30, "max_time": 180, "odds_of_complete": 0.3, 
                "next_states": [{"name": "StateD", "odds": 1.0}]
            },
            {
                "name": "StateC", "initial": False, "min_time": 90, "max_time": 560, "odds_of_complete": 0.4, 
                "next_states": [{"name": "StateA", "odds": 0.2}, {"name": "StateD", "odds": 0.8}]
            },
            {
                "name": "StateD", "initial": False, "min_time": 120, "max_time": 480, "odds_of_complete": 0.8, 
                "next_states": [{"name": "StateB", "odds": 1.0}]
            }
        ],
        additional_fields: List[Dict[str, Any]] = [
            {"type": "string_enum", "column_name": "category", "values": [{"value": "A", "odds": 0.5}, {"value": "B", "odds": 0.3}, {"value": "C", "odds": 0.2}]},
            {"type": "integer_range", "column_name": "priority", "min": 1, "max": 5}
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
        states: List of state definitions for generating process instances (defaults to predefined states)

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
        if additional_fields:
            for field in additional_fields:
                if field["type"] == "string_enum":
                    obj = generated_string_enum_value(field, obj)
                elif field["type"] == "integer_range":
                    obj = generated_integer_range_value(field, obj)
                elif field["type"] == "timestamp_range":
                    obj = generated_timestamp_range_value(field, obj, timestamp=created_at_with_offset)
        objects.append(obj)
    
    return objects

if __name__ == "__main__":
    # Example usage
    generated_objects = generate_json_objects(count=10)
    print(json.dumps(generated_objects, indent=4))