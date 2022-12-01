import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm

from c3qts.core.util import logger
from c3qts.core.settings import SETTINGS
from c3qts.core.constant import Exchange, Interval, Product, ContractType
import sys
sys.path.append('/home/cyh/mycta/vnpy_localdb')
from c3qts_localdb.localdb_database import LocaldbDatabase

class FactorSystem:
    def __init__(self, factor_class):
        # factor_class: 因子类
        self.db = LocaldbDatabase()
        self.factor_class = factor_class
    
    def generate(self, product, instrument, begin_datetime=None, end_datetime=None, exchange=Exchange.SHFE, symbol_type=ContractType.MERGE_ORI, write=False, append=False):
        '''
        instrument: 合约名
        begin_date: 生成因子的开始时间
        end_date: 生成因子的结束时间
        append: 生成的因子是覆盖还是追加
        
        TODO:
        Step1: 日期左右空缺(如果为左为空，右为空，分别取值)
        Step2: 日期合法性
        Step3: 逐日读取数据
        Step4: 因子计算
        
        Append: 时间序列上的追加？
        处理某一个合约？
        '''
        for frequency in self.factor_class.freq_list:
            if frequency == Interval.TICK:
                data, timestamp, column_dict = self.db.load_tick_data(symbol=instrument, start=begin_datetime, end=end_datetime, symbol_type=symbol_type)
                # data, timestamp, column_dict = self.db.load_tick_data(symbol=instrument, start=begin_date, end=end_date, symbol_type=symbol_type, factor_name='a1_csh')
                # print(data, timestamp)
                # return
                return_dict = self.factor_class.compute(data, timestamp, column_dict)
                # TODO(重要): 这里保存的时候需要将timestampe与return结合，才能进行截取
                # return
                if write:
                    for key_ in return_dict.keys():
                        # print(key_)
                        factor_name = f'{key_}_{self.factor_class.author}'
                        timestamp, ticks = return_dict[key_]
                        flag = self.db.save_tick_data(ticks=ticks, timestamp=timestamp, exchange=exchange, symbol=instrument, symbol_type=symbol_type, factor_name=factor_name, append=append)
                        # print(flag)
                else:
                    return return_dict
            else:
                pass
        # TODO: 保存的时候在因子的名称后面加上作者名称，避免覆盖
        # 直接写入? 如果是直接写入，
    
    def parallel_generate(self, products='All', begin_datetime='19000101', end_datetime='210000101', write=False, append=False, n_threads=1):
        '''
        products:
            All: 全部品种
            list: 指定品种列表
        begin_date: 生成因子的开始时间
        end_date: 生成因子的结束时间
        append: 生成的因子是覆盖还是追加
        n_threads: 并行核数
        '''
        if products == 'All':
            products = self.db.get_all_products(interval=Interval.TICK, symbol_type=ContractType.MERGE_ORI)

        for product in products:
            print(f'generating factor: {product}...')
            inst_list = self.db.get_all_instruments(interval=Interval.TICK, symbol_type=ContractType.MERGE_ORI, product=product)
            Parallel(n_jobs=n_threads)(delayed(self.generate)
                                (product, instrument, begin_datetime, end_datetime, write, append)
                                for instrument in tqdm(inst_list))