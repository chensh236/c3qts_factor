import sys
sys.path.append('./../c3qts_factor')
from c3qts.core.constant import Interval
from factor import Factor
import numpy as np
import pandas as pd

class TestFactor(Factor):
    def __init__(self, name, author, freq_list):
        super().__init__(name, author, freq_list)
    
    def get_data(self, data, idx):
        return data[:, idx]
    
    def compute(self, data, timestamp, column_dict) -> dict:
        '''
        demo
        '''
        result_dict = {}
        result_dict['a1'] = (timestamp, self.get_data(data, column_dict['AskPrice1']) + self.get_data(data, column_dict['BidPrice1']))
        result_dict['a1'] = (timestamp, self.get_data(data, column_dict['AskPrice1']) - self.get_data(data, column_dict['BidPrice1']))
        a3 = pd.Series(self.get_data(data, column_dict['AskPrice1']), index=timestamp).rolling(5).mean().dropna()
        result_dict['a3'] = (a3.index.values, a3.values)
        return result_dict