import datetime
import random
import numpy as np
import pandas as pd

## I need to generate some fake tabular data and event log data that is related by an id
class Data_Generator:
    tabular_states = ["sensed", "transfer", "submitted", "transfer2", ]
    tabular_id_templates = ["idx_{0}", "id_{0}", "{0}"]
    tabular_message_templates = ["Message regarding entity [entity_{0}] tracked by ..."]
    
    ## Setup our Constructor
    ##     tabular_states - ordered list of the states for our tabular data (0 index is first, n is last)
    ##     tabular_config - json/object of the states in tabular states, with a offset(int), range(int),
    ##                      probability(float) for all, but the first one; that will have a min(date_time) 
    ##                      and range(int)
    def __init__(self, tabular_states=None, tabular_config=None):
        ## What are the states that we use for our tabular states
        if tabular_states is not None:
            self.tabular_states = tabular_states
        else:    
            self.tabular_states = Data_Generator.tabular_states
        
        ## If a tabular_config isn't passed, build a randomized one
        if tabular_config is None:
            self.tabular_config = {}
            states = self.tabular_states
            
            ## Loop through states
            for i in range(len(states)):
                self.tabular_config[states[i]] = {}
                if i == 0:
                    self.tabular_config[states[i]]["min"] = datetime.datetime.now() + datetime.timedelta(0, -3600 * 24 * 2)
                    self.tabular_config[states[i]]["range"] = 3600
                else:
                    self.tabular_config[states[i]]["offset"]      = random.randrange(100)
                    self.tabular_config[states[i]]["range"]       = random.randrange(2000)
                    self.tabular_config[states[i]]["probability"] = .9
        else:
            self.tabular_config = tabular_config

        ## FIX-ME
        self.tabular_id_templates       = Data_Generator.tabular_id_templates
        self.tabular_message_templates  = Data_Generator.tabular_message_templates
        
        ## Setup the one that we would like to have down the road
        self.tabular_dataframe           = None
    ## ========================== end init ==========================

    ## Generate tabular data using the tabular_states and tabular_config
    ##     num - number of records / ids to generate
    def gen_tabular_data(self, num=500):
        col_id, col_msg = "id", "message"
        ## To save some click, go ahead and make some variables to save some space
        tabular_states, tabular_config = self.tabular_states, self.tabular_config

        ## Our data, that we will be contructing from
        df = { col_id: [], col_msg: [] }
        for s in tabular_states:
            df[s] = []

        ## Loop through all of our records
        for i in range(num):
            id = self.tabular_id_templates[random.randrange(len(self.tabular_id_templates))].format(i)
            msg = self.tabular_message_templates[random.randrange(len(self.tabular_message_templates))].format(id)

            ## Save the id / msg to our datas
            df[col_id].append(id)
            df[col_msg].append(msg)

            ## Deal with the initial value
            s = tabular_states[0]
            timestamp = tabular_config[s]["min"] + datetime.timedelta(0, random.randrange( tabular_config[s]["range"] ))
            df[s].append(timestamp)
            workflow_ended = False
            ## Deal with the rest of our columns
            for s in tabular_states[1:]:
                if workflow_ended:
                    df[s].append(None)
                    continue
                    
                if random.random() <= tabular_config[s]["probability"]:
                    timestamp = timestamp + datetime.timedelta(0, random.randrange( tabular_config[s]["offset"], tabular_config[s]["offset"] + tabular_config[s]["range"] ))
                    df[s].append(timestamp)
                else:
                    ## If we didn't meet the minimum probablity of this stage, then we are done.  Bail out
                    workflow_ended = True
                    df[s].append(None)

        ## We are now done, convert to a dataframe, store and return
        self.tabular_dataframe = pd.DataFrame(df)
        return self.tabular_dataframe
    ## ========================== end gen_tabular_data ==========================











