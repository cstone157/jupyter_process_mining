from datetime import datetime, timedelta
import json
import random

def generated_string_enum_value(config, target_obj):
    """
    Generate a value based on config and add it to target_obj.
    
    Args:
        config: {"column_name": <string>, "values": [{"value": <string>, "odds": float}, ...]}
        target_obj: Dictionary to add the generated value to
    
    Returns:
        Modified target_obj with the generated value added
    """
    column_name = config["column_name"]
    values = config["values"]
    
    # Extract values and their odds
    value_list = [v["value"] for v in values]
    odds_list = [v["odds"] for v in values]
    
    # Normalize odds to probabilities if needed
    total_odds = sum(odds_list)
    probabilities = [o / total_odds for o in odds_list]
    
    # Generate value based on probabilities
    generated_value = random.choices(value_list, weights=probabilities, k=1)[0]
    
    # Add to target object
    target_obj[column_name] = generated_value
    
    return target_obj

def generated_integer_range_value(config, target_obj, offset=0):
    """
    Generate an integer value based on config and add it to target_obj.
    
    Args:
        config: {"column_name": <string>, "min": int, "max": int}
        target_obj: Dictionary to add the generated value to
    Returns:
        Modified target_obj with the generated value added
    """
    column_name = config["column_name"]
    min_value = config["min"]
    max_value = config["max"]
    
    generated_value = random.randint(min_value, max_value) + offset
    target_obj[column_name] = generated_value
    
    return target_obj

def generated_timestamp_range_value(config, target_obj, offset_seconds=0, timestamp=None):
    """
    Generate a timestamp value based on config and add it to target_obj.
    
    Args:
        config: {"column_name": <string>, "start": datetime, "end": datetime}
        target_obj: Dictionary to add the generated value to
    Returns:
        Modified target_obj with the generated value added
    """    
    column_name = config["column_name"]
    min_duration = config["min_duration"]
    max_duration = config["max_duration"]

    random_seconds = random.randint(min_duration, max_duration) + offset_seconds
    if timestamp is None:
        timestamp = datetime.now()
    generated_timestamp = timestamp + timedelta(seconds=random_seconds)
    target_obj[column_name] = generated_timestamp.isoformat()
    
    return target_obj