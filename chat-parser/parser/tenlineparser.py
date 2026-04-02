import numpy as np
import pandas as pd
import datetime

class TenLineParser:
    """A general parser for converting the ten-line messages from irc into standard record format.

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    def __init__(self,
        prefixes=["1. ", "2. ", "3. ", "4. ", "5. ",
                  "6. ", "7. ", "8. ", "9. ", "10. "],
        new_columns=["msg_1", "msg_2", "msg_3", "msg_4", "msg_5",
                  "msg_6", "msg_7", "msg_8", "msg_9", "msg_10"],
        best_matches=True,
        roomname_column  = "Room Name",
        username_column  = "Username",
        message_column   = "Message",
        timestamp_column = "Timestamp",

        groupby_cnt_col="msg_cnt",
        #match_group_col="match_group", 
        time_diff_col="time_diff",
        groupby=["Room Name", "Username"]
    ):
        """Return a new Ten_Line_Parser object.

        Args:
            prefixes: what are the prefixes to look for?
        """
        self.prefixes         = prefixes
        self.new_columns      = new_columns
        self.best_matches     = best_matches
        self.roomname_column  = roomname_column
        self.username_column  = username_column
        self.message_column   = message_column
        self.timestamp_column = timestamp_column

        self.groupby_cnt_col  = groupby_cnt_col
        #self.match_group_col  = match_group_col
        self.time_diff_col    = time_diff_col
        self.groupby          = groupby

    def _parseIncompleteRowTimeDiffs(self, dataset, index, row):
        """Take the index of the passed row and build a list of all the possible matching rows, and build a dictionary of those relationships

        Args:
            dataset: 
            row: row to parse time differences for
        """
        ## Filter down to only those rows, that might match our current row
        potential_matches = dataset[dataset[self.groupby_cnt_col] != len(self.new_columns)]
        potential_matches = potential_matches[~potential_matches.index.isin([index])]
        for col in self.groupby:
            potential_matches = potential_matches[potential_matches[col] == row[col]]
        ## If there are no matches, then just leave
        if len(potential_matches) <= 0:
            return None

        ## Loop throught the rows of our matches
        print(f"{row}")
        for match_index, match_row in potential_matches.iterrows():
            print(f"==> self.time_diff_col: {self.time_diff_col}, match_index: {match_index}, index: {index}")
            a = len(row[self.time_diff_col]) > 0 and row[self.time_diff_col][match_index] is not None
            b = len(match_row[self.time_diff_col]) > 0 and match_row[self.time_diff_col][index] is not None
            ## If both already have a match then go ahead and leave
            if a and b:
                pass
            ## Check to see if we already this index in our time_diffs, if it exists save
            elif a:
                match_row[self.time_diff_col][index] = row[self.time_diff_col][match_index]
                pass
            ## Check to see if our match already this our index in our time_diffs, if it exists save
            elif b:
                row[self.time_diff_col][match_index] = match_row[self.time_diff_col][index]
                pass
            
            ## Loop through the new columns and check to see if our rows have duplicate values
            full_match = True
            column_match = len(self.new_columns)
            bad_match = False
            for col in self.new_columns:
                v1 = row[col]
                v2 = match_row[col]

                ## If both rows already have a value for the same column, go ahead and mark as a bad match
                if v1 is not None and v2 is not None:
                    full_match = False
                    column_match -= 1
                    bad_match = True
                if v1 is None and v2 is None:
                    full_match = False
                    column_match -= 1
            
                ## Calculate the time time difference
                time_diff = { 
                    "time_diff": abs((row[self.timestamp_column] - match_row[self.timestamp_column]).total_seconds() * 1000),
                    "full_match": full_match,
                    "column_match": column_match,
                    "bad_match": bad_match
                }

            ## Store the resulting time_diff
            row[self.time_diff_col][match_index] = time_diff
            match_row[self.time_diff_col][index] = time_diff
        
        return None

    
    def parse(self, dataset):
        """Take a dataset of 10 line data and attempt to parse it, into a columnar format.

        Args:
            dataset: what is the dataset to parse?
        """
        ## ########################################## ADD THE NEW COLUMNS ##########################################
        ## First go ahead and create the new columns and strip off our prefixes
        new_dataset = dataset.copy()
        ## Make sure that our timestamp column is already int timestamp format
        new_dataset[self.timestamp_column] = pd.to_datetime(new_dataset[self.timestamp_column])
        ## Loop through the prefixes and create the new columns
        for i, prefix in enumerate(self.prefixes):
            new_dataset[self.new_columns[i]] = new_dataset[new_dataset[self.message_column].str.startswith(prefix)][self.message_column].str.slice(len(prefix))
        ## Drop the message column, since we don't need it anymore
        new_dataset = new_dataset.drop(columns=[self.message_column])

        ## ################################# MERGE ON IDENTICAL Room/User/Timestamp ################################
        ## Build our groupby (that includes the timestamp column)
        full_groupby = self.groupby.copy()
        full_groupby.append(self.timestamp_column)
        ## Add a column for our groupby count
        new_dataset[self.groupby_cnt_col] = 0
        ## GroupBy, first build a dic for our group by and count for our count column
        agg_dict = {}
        for col in new_dataset.columns:
            if not (col in full_groupby):
              agg_dict[col] = "first"
        agg_dict[self.groupby_cnt_col] = "count"
        new_dataset = new_dataset.groupby(full_groupby).agg(agg_dict).reset_index()
        ## Save off all of the columns we've created for later
        dataset_columns = new_dataset.columns

        ## ############################## Try to MERGE is cnt is less than len(prefix) #############################
        new_dataset[self.time_diff_col] = [{} for _ in range(len(new_dataset))]
        idx_inspected = []
        
        ## Save out the ones that are already fully matched
        already_matched = new_dataset[new_dataset[self.groupby_cnt_col] == len(self.new_columns)].copy()
        need_match = new_dataset[new_dataset[self.groupby_cnt_col] < len(self.new_columns)]
        ## build the merge result data
        merged = {
            self.roomname_column:  [],
            self.username_column:  [],
            self.timestamp_column: [],
            self.groupby_cnt_col:  [],
            self.time_diff_col:    []
        }
        for col in self.new_columns:
            merged[col]: []

        
        for index, row in need_match.iterrows():
            if index not in idx_inspected:
                self._parseIncompleteRowTimeDiffs(new_dataset, index, row)
                idx_inspected.append(index)
                '''## if we are doing best match, then go ahead and add it to the merges
                if self.best_matches and row[self.time_diff_col]["full_match"]:
                    for col in dataset_columns:
                        merged[col].append(row[col])
                    merged[self.time_diff_col].append(row[self.time_diff_col])
                    
                #break'''
        
        return new_dataset