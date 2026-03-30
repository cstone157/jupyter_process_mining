from datetime import datetime, timedelta
import pandas as pd
import random

def generate_chat_data_v1(num_to_generate: int, 
                          timestamp: datetime = None,
                          min_seconds: int = 0,
                          max_seconds: int = 600,
                          min_milliseconds: int = 0,
                          max_milliseconds: int = 15) -> pd.DataFrame:
    """
    Generate synthetic multi-line chat messages for testing purposes.
    
    Returns:
        Dataframe with columns: 
    """
    rooms_list = ["Room1", "Room2", "Room3", "Room4", "Room5"]
    usernames_list = ["UserA", "UserB", "UserC", "UserD", "UserE"]
    callsigns_list = ["Echo", "Tango", "Bravo", "Charlie", "Delta"]
    idenfifiers_list = ["SMACK", "ESCORT", "TEST", "N/A"]
    line3_prefixes_list = ["TEST", "TST", "PANDAS", "NUMPY", "SCIKIT"]
    line4_prefixes_list = ["N/A", "None"]
    line5_prefixes_list = ["Time to Completion", "ETA", "Expected Completion Time", "TTC"]

    timestamp = timestamp or datetime.now()
    rooms = []
    usernames = []
    messages = []
    timestamps = []

    for i in range(num_to_generate):
        room = random.choice(rooms_list)
        username = random.choice(usernames_list)

        rooms += [room] * 5
        usernames += [username] * 5
        for i in range(5):
            timestamp += timedelta(milliseconds=random.randint(min_milliseconds, max_milliseconds))
            timestamps += [timestamp]

        messages.append(f"1. {random.choice(callsigns_list)}{random.randint(1, 10)}")
        messages.append(f"2. {random.choice(idenfifiers_list)}{random.randint(1, 10)}")
        messages.append(f"3. {random.choice(line3_prefixes_list)}")
        messages.append(f"4. {random.choice(line4_prefixes_list)}")
        timestamp += timedelta(seconds=random.randint(min_seconds, max_seconds))
        messages.append(f"5. {random.choice(line5_prefixes_list)}{random.randint(1, 10)}: {timestamp.isoformat()}")

    chat_data = pd.DataFrame({
        "room": rooms,
        "username": usernames,
        "message": messages,
        "timestamp": timestamps
    })

    return chat_data

if __name__ == "__main__":
    generated_chat_data = generate_chat_data_v1(num_to_generate=10)
    print(generated_chat_data.head())