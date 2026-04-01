from datetime import datetime, timedelta
import pandas as pd
import numpy as np
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


def generate_chat_log_ten_lines(number_to_generate,
        start_time=None, end_time=None,

        room_names = ["Room1", "Room2", "Room3", "Room4", "Room5"],
        usernames  = ["User1", "User2", "User3", "User4", "User5"],
        message_1 = [
            "Echo1", "Echo2", "Echo3", "Echo4",
            "Bravo1", "Bravo2", "Bravo3", "Bravo4",
            "Tango1", "Tango2", "Tango3", "Tango4",
        ],
        message_2 = [
            "SMACK", "ESCORT", "TEST", "DANCE",
        ],
        message_3 = [
            "TEST1", "TEST2", "TEST3", "TEST4",
            "TEST5", "TEST6", "TEST7", "TEST8",
            "TEST9", "TEST10", "TEST11", "TEST12",
        ],
        message_4 = [
            "APPLE", "ORANGE", "BANANNA", "PEACH",
        ],
        message_5 = ["N/A"],
        message_6 = ["N/A"],
        message_7 = ["N/A"],
        message_8 = ["N/A"],
        message_9 = ["N/A"],

        roomname_column  = "Room Name",
        username_column  = "Username",
        message_column   = "Message",
        timestamp_column = "Timestamp",

        appendId        = False,
        incomplete_odds = 0.001,

        latency_odds    = 0.01,
        latency_millis  = 200,

    ):
    """
    Generate a number of ten-line messages in the chat format.  This is only an approximations, not a perfect match.  There is no message_10, since that is the timestamp field.

    Args:
        number_to_generate: Number of ten lines to generate.
        start_time: (Optional) Start time frame for the messages to arrive at, if None is provided it will use the start of the current day.
        end_time: (Optional) End time frame for the messages to arrive at, if None is provided it will add one hour to the start_time.
        room_names: (Optional) List of the names of the rooms to generate messages for.
        usernames: (Optional) List of the users to generate messages for.
        message_1: (Optional) List of the messages to generate.
        message_2: (Optional) List of the messages to generate.
        message_3: (Optional) List of the messages to generate.
        message_4: (Optional) List of the messages to generate.
        message_5: (Optional) List of the messages to generate.
        message_6: (Optional) List of the messages to generate.
        message_7: (Optional) List of the messages to generate.
        message_8: (Optional) List of the messages to generate.
        message_9: (Optional) List of the messages to generate.

        appendId: (Optional) Boolean of should we append the id to the messages.
        incomplete_odds: (Optional) Odds that we generate incomplete_odds messages.

    Returns:
        Returns a dataframe of the generated chat logs.

    Raises:
        KeyError: Raises an exception.
    """

    ## If start_time is None
    if start_time is None:
        start_time = datetime.datetime.now()
        start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    ## If end_time is None
    if end_time is None:
        end_time = start_time + datetime.timedelta(hours=1)

    ## Get the differnce between the start_time and end_time
    time_difference = (end_time - start_time) / number_to_generate

    ## ====     DELETE ME
    #display(start_time)
    #display(end_time)
    #display(time_difference)
    ## ==== END DELETE ME

    ## Convert the message params to an array to make our life a little easier
    messages = [message_1, message_2, message_3, message_4, message_5, message_6, message_7, message_8, message_9]

    ## Create or initial Dictionary for our data to return
    chat_log = {
        roomname_column  : [],
        username_column  : [],
        message_column   : [],
        timestamp_column : [],
    }

    ## Intantiate our random number generator
    rnd_generator = np.random.default_rng()
    idx = 1

    ## == Loop through the number of messages to generate and start generating them
    for i in range(number_to_generate):
        r = np.random.choice(room_names)
        u = np.random.choice(usernames)
        t = start_time

        for j in range(len(messages)):
            ## Generate a random number, if we are greater then continue generating our message
            if rnd_generator.random() > incomplete_odds:
                ## Generate a random number, if we are less than it, then go ahead and add an
                ##    offset to our timestamp
                if rnd_generator.random() <= latency_odds:
                    t += datetime.timedelta(milliseconds=np.random.randint(1, latency_millis+1))

                chat_log[roomname_column].append(r)
                chat_log[username_column].append(u)
                chat_log[message_column].append(f"{j+1}. {np.random.choice(messages[j])}{f'_{idx}' if appendId else ''}")
                chat_log[timestamp_column].append(t.strftime('%Y-%m-%d %H:%M:%S.%fZ'))

        chat_log[roomname_column].append(np.random.choice(room_names))
        chat_log[username_column].append(np.random.choice(usernames))
        chat_log[message_column].append(f"10. Time to Completion{f'_{idx}' if appendId else ''} : {start_time.strftime('%Y-%m-%d %H:%M:%S.%fZ')}")
        chat_log[timestamp_column].append(start_time.strftime('%Y-%m-%d %H:%M:%S.%fZ'))

        idx += 1
        start_time += time_difference
    ## ================== END LOOP ==================

    return pd.DataFrame(chat_log)

if __name__ == "__main__":
    generated_chat_data = generate_chat_data_v1(num_to_generate=10)
    print(generated_chat_data.head())