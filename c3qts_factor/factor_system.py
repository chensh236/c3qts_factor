import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm
from pathlib import Path
import os
from c3qts.core.util import logger
from c3qts.core.settings import SETTINGS
from c3qts.core.constant import Exchange, Interval, Product, ContractType
from c3qts_localdb.localdb_database import LocaldbDatabase


class FactorSystem:
    def __init__(self, factor_class):
        # factor_class: 因子类
        self.db = LocaldbDatabase()
        self.factor_class = factor_class
    
    '''
    根据因子名称以及作者名称获得不同周期的因子列表
    '''
    @staticmethod
    def get_factor_list(database_dir: str, factor_name:str ='', author:str =''):
        if len(factor_name) == 0 and len(author) == 0:
            logger.error(f'因子{factor_name}, 作者{author}至少需要一个必要元素')
            return None
        database_dir = Path(database_dir)
        input_fp = database_dir / '期货' / '因子'
        file_list = os.listdir(input_fp)
        file_list.sort()
        file_list = [factor for factor in file_list if factor_name in factor and author in factor]
        return file_list
    
    def generate(self, instrument, begin_datetime=None, end_datetime=None, symbol_type=ContractType.MERGE_ORI, write=False, append=False):
        '''
        instrument: 合约名
        begin_date: 生成因子的开始时间
        end_date: 生成因子的结束时间
        append: 因子追加
        '''
        logger.info(f'合约{instrument}生成因子开始\t开始日期:{begin_datetime}\t结束日期:{end_datetime}')
        for frequency in self.factor_class.freq_list:
            if frequency == Interval.TICK:
                data, timestamp, column_dict = self.db.load_tick_data(symbol=instrument, start=begin_datetime, end=end_datetime, symbol_type=symbol_type)
                # data, timestamp, column_dict = self.db.load_tick_data(symbol=instrument, start=begin_date, end=end_date, symbol_type=symbol_type, factor_name='a1_csh')
                # print(data, timestamp)
                # return
                try:
                    return_dict = self.factor_class.compute(data, timestamp, column_dict)
                except Exception as e:
                    logger.error(f'''
                                 因子{self.factor_class}在合约{instrument}上生成产生错误：
                                 {e}
                                 ''')
                    return None
                # 删除很大的变量
                del data
                del timestamp
                if write:
                    for key_ in return_dict.keys():
                        # print(key_)
                        factor_name = f'{key_}_{self.factor_class.author}'
                        timestamp, ticks = return_dict[key_]
                        ticks = ticks.reshape(-1, 1)
                        flag = self.db.save_tick_data(ticks=ticks, timestamp=timestamp, symbol=instrument, symbol_type=symbol_type, factor_name=factor_name, append=append)
                        # print(flag)
                else:
                    return return_dict
            else:
                pass
        logger.info(f'合约{instrument}生成因子结束\t开始日期:{begin_datetime}\t结束日期:{end_datetime}')
        # TODO: 保存的时候在因子的名称后面加上作者名称，避免覆盖
        # 直接写入? 如果是直接写入，
    
    def parallel_generate(self, products='All', begin_datetime=None, end_datetime=None, symbol_type=ContractType.MERGE_ORI, write=False, append=False, n_threads=1):
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
            products = self.db.get_all_products(interval=Interval.TICK, symbol_type=symbol_type)

        for product in products:
            logger.info(f'generating factor: {product}...')
            inst_list = self.db.get_all_instruments(interval=Interval.TICK, symbol_type=symbol_type, product=product)
            Parallel(n_jobs=n_threads)(delayed(self.generate)
                                (instrument, begin_datetime, end_datetime, symbol_type, write, append)
                                for instrument in inst_list)