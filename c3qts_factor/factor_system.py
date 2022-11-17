import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm

class FactorSystem:
    def __init__(self, factor_class):
        # factor_class: 因子类
        # 静态？
        self.factor_class = factor_class
    
    def generate(self, product, instrument, begin_date='19000101', end_date='21000101', append=False):
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
        
        data, timestamp, column_dict = read_contract_data(product, instrument, begin_date, end_date)
        self.factor_class.compute(data, timestamp, column_dict, product, instrument, append)
    
    def parallel_generate(self, products='All', begin_date='19000101', end_date='210000101', append=False, n_threads=1):
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
            products = get_all_products()

        for product in products:
            print(f'generating factor: {product}...')
            inst_list = get_all_instruments(product)
            Parallel(n_jobs=n_threads)(delayed(self.generate)
                                (product, instrument, begin_date, end_date, append)
                                for instrument in tqdm(inst_list))