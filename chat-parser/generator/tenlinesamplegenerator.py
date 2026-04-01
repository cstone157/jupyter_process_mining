import numpy as np
import pandas as pd

import datetime

class TenLineSampleGenerator:
    """Generate some sample ten-line data for testing the multi-line parser

    You don't need a messagebody for the last prefix.  It will alwasy be a timestamp of the message being generated.

    Attributes:
        prefixes: what are the default prefixes that ten-lines use
    """
    NOT_AVAILABLE = "N/A"
    room_name_parts = ["s", "t", "us", "fvey", "test", "experiment", "c2", "south", "north"]
    user_name_parts = ["joa", "c2", "falcon", "flame", "cannon", "bearcat", "test", "dragon", "wasp", "bearcat"]
    message_parts =   {
        0: [
            "Echo01", "Echo11", "Echo21", "Echo31", "Echo41",
            "Taco01", "Taco11", "Taco21", "Taco31",
            "Bravo01", "Bravo21", "Bravo41", "Bravo51",
            "Maple01", "Maple11", "Maple21",
            "Gravity01", "Gravity11", "Gravity21", "Gravity31", "Gravity41"
        ],
        1: ["SMACK", "ESCORT", "TEST", "DANCE"],
        2: ["TEST", "Test", "PRACTICE", "PERFORMANCE"],
        3: ["APPLE", "ORANGE", "BANANNA", "PEACH", "MANGO"],
        4: ["N/A"],
        5: ["N/A"],
        6: ["N/A"],
        7: ["N/A"],
        8: ["N/A"],
    }


    def __init__(self,
            sample_roomnames = None,
            num_of_rooms = 5,
            sample_usernames = None,
            num_of_users = 5,
            prefixes=["1. ", "2. ", "3. ", "4. ", "5. ",
                      "6. ", "7. ", "8. ", "9. ", "10. "],
            message_parts   = None,
            appendId        = False,
            incomplete_odds = 0.001,

            latency_odds    = 0.01,
            latency_millis  = 200,
        ):
        """Return a new Ten_Line_Sample_Generator object."""
        if sample_roomnames is None:
            self.sample_roomnames = self.generate_sample_roomnames(num_of_rooms)
        else:
            self.sample_roomnames = sample_roomnames

        if sample_usernames is None:
            self.sample_usernames = self.generate_sample_usernames(num_of_users)
        else:
            self.sample_usernames = sample_usernames

        self.prefixes = prefixes

        if message_parts is None:
            self.sample_message_parts = TenLineSampleGenerator.message_parts

        self.appendId = appendId
        self.incomplete_odds = incomplete_odds

        self.latency_odds = latency_odds
        self.latency_millis = latency_millis

        self.room_name_column = "Room Name"
        self.username_column = "Username"
        self.message_column = "Message"
        self.timestamp_column = "Timestamp"

    def generate_sample_roomnames(self, num_of_rooms):
        """Generate a list of sample room names"""
        roomnames = []
        while len(roomnames) < num_of_rooms:
            room_name = np.random.randint(1, len(TenLineSampleGenerator.room_name_parts)/2)
            room_name = "_".join(np.random.choice(TenLineSampleGenerator.room_name_parts, room_name))
            if room_name not in roomnames:
                roomnames.append(room_name)
        return roomnames

    def generate_sample_usernames(self, num_of_users):
        """Generate a list of sample user names"""
        usernames = []
        while len(usernames) < num_of_users:
            username = np.random.randint(1, 3)
            username = "_".join(np.random.choice(TenLineSampleGenerator.user_name_parts, username))
            if username not in usernames:
                usernames.append(username)
        return usernames

    def generate_sample_data(self,
        number_to_generate,
        start_time=None,
        end_time=None
    ):
        """Generate some random data for testing, the number of messages will be distrubuted evenly between the start and end time.

        Args:
            number_to_generate: how many records to generate?
            start_time: (Optional) what is the start time, if none is provided it will be set to now
            end_time: (Optional) what is the end time, if none is provided it will be set to start_time + 1 hour
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

        ## Create our initial dictionary for returning
        chat_log = {
            self.room_name_column  : [],
            self.username_column   : [],
            self.message_column    : [],
            self.timestamp_column  : [],
        }

        ## Intantiate our random number generator and our index number
        rnd_generator = np.random.default_rng()
        idx = 1

        ## Loop through the number of messages to generate
        while idx <= number_to_generate:
            r = np.random.choice(self.sample_roomnames)
            u = np.random.choice(self.sample_usernames)
            t = start_time

            for j in range(len(self.message_parts)):
                ## Generate a random number, if we are greater then continue generating our message
                if rnd_generator.random() > self.incomplete_odds:
                    ## Generate a random number, if we are less than it, then go ahead and add an
                    ##    offset to our timestamp
                    if rnd_generator.random() <= self.latency_odds:
                        t += datetime.timedelta(milliseconds=np.random.randint(1, self.latency_millis+1))

                    chat_log[self.room_name_column].append(r)
                    chat_log[self.username_column].append(u)
                    #chat_log[self.message_column].append(f"{j+1}. {np.random.choice(self.message_parts[j])}{f'_{idx}' if self.appendId else ''}")
                    chat_log[self.message_column].append(f"{self.prefixes[j]}{np.random.choice(self.message_parts[j])}{f'_{idx}' if self.appendId else ''}")
                    chat_log[self.timestamp_column].append(t.strftime('%Y-%m-%d %H:%M:%S.%fZ'))

            chat_log[self.room_name_column].append(r)
            chat_log[self.username_column].append(u)
            chat_log[self.message_column].append(f"10. Time to Completion{f'_{idx}' if self.appendId else ''} : {start_time.strftime('%Y-%m-%d %H:%M:%S.%fZ')}")
            chat_log[self.timestamp_column].append(t.strftime('%Y-%m-%d %H:%M:%S.%fZ'))

            idx += 1
            start_time += time_difference
        ## ================== END LOOP ==================


        return pd.DataFrame(chat_log)