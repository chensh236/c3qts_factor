import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm
from pathlib import Path
import os
from c3qts.core.util import logger
from c3qts.core.settings import SETTINGS
from c3qts.core.constant import Exchange, Interval, Product, ContractType
from c3qts_localdb.localdb_database import LocaldbDatabase
import shutil

class FactorSystem:
    def __init__(self, factor_class):
        # factor_class: 因子类
        self.db = LocaldbDatabase()
        self.factor_class = factor_class
    
    '''
    根据因子名称以及作者名称获得不同周期的因子列表。如若full为True则只返回存在主力合约的因子，否则返回所有因子
    '''
    @staticmethod
    def get_factor_list(database_dir: str, factor_name: str = '', author: str = '', symbol: str = '', variety: str = '', product_name=Product.FUTURES, contract_type=ContractType.ZL, interval: Interval=Interval.TICK):
        if len(factor_name) == 0 and len(author) == 0:
            logger.error(f'因子{factor_name}, 作者{author}至少需要一个必要元素')
            return None

        database_dir = Path(database_dir)
        input_fp = database_dir / product_name.value / '因子'
        factor_list = os.listdir(input_fp)
        factor_list.sort()

        if not symbol and not variety:
            logger.warning('Symbol和Variety不能同时为空')
            return []
        elif symbol and not variety:
            contract_type = ContractType.MERGE_ORI
            variety = ''.join([i for i in symbol if not i.isdigit()])
        elif variety and not symbol:
            contract_type = ContractType.ZL
        elif variety and symbol:
            if symbol.startswith(variety):
                contract_type = ContractType.MERGE_ORI
            else:
                logger.error('Variety应该是Symbol的前几个字母')
                return []

        if contract_type == ContractType.ZL:
            factor_list = [factor for factor in factor_list if factor_name in factor and author in factor and (database_dir / product_name.value / '因子' / factor / interval.value / ContractType.ZL.value / variety / f'{variety}.h5').is_file()]
        elif contract_type == ContractType.MERGE_ORI:
            factor_list = [factor for factor in factor_list if factor_name in factor and author in factor and (database_dir / product_name.value / '因子' / factor / interval.value / ContractType.MERGE_ORI.value / variety / f'{symbol}.h5').is_file()]

        return factor_list


    @staticmethod
    def get_factor_list_through_different_product(database_dir: str, factor_name: str = '', author: str = '', symbol_list: list = [], variety_list: list = [], product_name=Product.FUTURES, contract_type=ContractType.ZL, interval: Interval=Interval.TICK):
        if len(factor_name) == 0 and len(author) == 0:
            logger.error(f'因子{factor_name}, 作者{author}至少需要一个必要元素')
            return None

        factor_dict = {}
        if contract_type == ContractType.ZL:
            if len(symbol_list) != 0:
                logger.warning(f'对于主力合约类型，symbol_list应保持为空')
            for variety in variety_list:
                factor_list = FactorSystem.get_factor_list(database_dir, factor_name, author, '', variety, product_name, contract_type, interval)
                factor_dict[variety] = factor_list

        elif contract_type == ContractType.MERGE_ORI:
            if len(variety_list) != 0:
                logger.warning(f'对于原始合约类型，variety_list应保持为空')
            for symbol in symbol_list:
                factor_list = FactorSystem.get_factor_list(database_dir, factor_name, author, symbol, '', product_name, contract_type, interval)
                factor_dict[symbol] = factor_list

        return factor_dict
    
    @staticmethod
    def _confirm_delete(factor_name=None, factor_list=None):
        if factor_name is None and factor_list is None:
            logger.warning('删除的因子名称以及列表为空')
            return False
        # 在删除前获取用户确认
        msg = ''
        if factor_name is not None:
            msg = f'确认删除因子 {factor_name} 及其相关数据? (y/n):\nUser: '
        else:
            msg = f'确认删除因子列表中的因子及其相关数据? (y/n): \n{factor_list}\nUser:'
        confirm = input(msg)
        if confirm.lower() != 'y':
            print('操作已取消。')
            return False
        else:
            return True

    '''
    批量删除因子
    '''
    @staticmethod
    def remove_factor_list(database_dir, factor_list, author: str='', product_name=Product.FUTURES, interval: Interval=None, contract_type: ContractType=None, variety_list=[]):
        if FactorSystem._confirm_delete(factor_list=factor_list):
            for factor_name in factor_list:
                FactorSystem.remove_factor(database_dir, factor_name, author, product_name, interval, contract_type, variety_list, confirm=True)

    
    '''
    根据因子名称以及作者删除因子
    '''
    @staticmethod
    def remove_factor(database_dir, factor_name, author: str='', product_name=Product.FUTURES, interval: Interval=None, contract_type: ContractType=None, variety_list=[], confirm=False):
        if len(factor_name) == 0:
            logger.error(f'因子{factor_name}名称必须存在，作者可以不存在')
            return False
        # 删除前确认
        if confirm or FactorSystem._confirm_delete(factor_name=factor_name):        
            base_path = Path(database_dir)
            base_path = base_path / product_name.value / '因子'
            if len(author) > 0:
                factor_name = f'{factor_name}_{author}'
            factor_path = Path(database_dir) / '期货' / '因子' / factor_name
            
            if interval is None:
                # 删除指定因子下的所有内容
                logger.info(f'删除路径:{factor_path}')
                shutil.rmtree(factor_path, ignore_errors=True)
                return

            interval_path = factor_path / interval.value
            
            if contract_type is None:
                # 删除指定因子和时间间隔下的所有内容
                logger.info(f'删除路径:{interval_path}')
                shutil.rmtree(interval_path, ignore_errors=True)
                return

            contract_type_path = interval_path / contract_type.value
            
            if len(variety_list) == 0:
                # 删除指定因子、时间间隔和合约类型下的所有内容
                logger.info(f'删除路径:{contract_type_path}')
                shutil.rmtree(contract_type_path, ignore_errors=True)
            
            for variety in variety_list:
                # 删除特定品种的数据
                variety_path = contract_type_path / variety
                logger.info(f'删除路径:{variety_path}')
                shutil.rmtree(variety_path, ignore_errors=True)

    def generate(self, instrument, begin_datetime=None, end_datetime=None, symbol_type=ContractType.MERGE_ORI, write=False, append=False):
        '''
        instrument: 合约名
        begin_date: 生成因子的开始时间
        end_date: 生成因子的结束时间
        append: 因子追加
        '''
        logger.info(f'合约{instrument}生成因子{self.factor_class.name}_{self.factor_class.author}开始\t开始日期:{begin_datetime}\t结束日期:{end_datetime}')
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
        logger.info(f'合约{instrument}生成因子{self.factor_class.name}_{self.factor_class.author}结束\t开始日期:{begin_datetime}\t结束日期:{end_datetime}')
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