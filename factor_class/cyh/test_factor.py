import sys
sys.path.append('/home/cyh/mycta/factor_system')
from utils import save_factor

class test:
    def __init__(self):
        # 避免不同用户的因子重名，最好在因子名中加入用户自己的标识
        self.name = 'test_cyh'
    
    def compute(self, data, timestamp, column_dict, product, instrument, append):
        a1 = data[column_dict['AskPrice1']]
        save_factor(a1, timestamp, self.name, product, instrument, append)
