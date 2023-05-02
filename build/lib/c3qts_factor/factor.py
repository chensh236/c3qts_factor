import pandas as pd
class Factor:
    name: str = ''
    author: str = ''
    freq_list = []
    def __init__(self, name, author, freq_list):
        self.name = name
        self.author = author
        # 读取的频率
        self.freq_list = freq_list
    
    def compute(self, data, timestamp, column_dict) -> dict:
        '''
        demo
        '''
        result_dict = {}
        result_dict['a1'] = (timestamp, data[column_dict['AskPrice1']] + data[column_dict['BidPrice1']])
        result_dict['a2'] = (timestamp, data[column_dict['AskPrice1']] + data[column_dict['BidPrice1']])
        a3 = pd.Series(index= data[column_dict['AskPrice1']]).rolling(5).mean()
        result_dict['a3'] = (a3.index, a3.values)
        return result_dict
    
    def get_data(self, data, col):
        return data[:, col]