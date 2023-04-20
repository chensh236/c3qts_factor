import sys
sys.path.append('./../c3qts_factor')
#from factor_system import FactorSystem
#from test_factor import TestFactor
from factor_system.c3qts_factor.factor_system import FactorSystem
from factor_system.demo.test_factor import TestFactor
from c3qts.core.constant import Interval, Exchange, ContractType
from c3qts.core.settings import SETTINGS
from c3qts_localdb.localdb_database import LocaldbDatabase

SETTINGS["database.basedir"] = '/dev_data/database'

test_factor_class = TestFactor(name='momentum', author='cyh', freq_list=[Interval.TICK])
test_factor_system = FactorSystem(test_factor_class)
# test_factor_system.parallel_generate(['rb', 'ag'], n_threads=10)
db = LocaldbDatabase()

test_factor_system.generate(instrument='AG1801', begin_datetime='19000101', end_datetime='21000101', write=True, append=False)
data, ts, _ = db.load_tick_data(symbol='AG1801',
                        symbol_type=ContractType.MERGE_ORI,
                        start='19000101000000000',
                        end='21000101000000000',
                        factor_name = 'a1_cyh')
print(data, ts, len(data))

test_factor_system.generate(instrument='AG1801', write=True, append=True)
data, ts, _ = db.load_tick_data(symbol='AG1801',
                        symbol_type=ContractType.MERGE_ORI,
                        start='20180102000000000',
                        end='20180116083000000',
                        factor_name = 'a1_cyh')
print(data, ts, len(data))

test_factor_system.parallel_generate(products=['AG'], begin_datetime='19000101', end_datetime='21000101',  append=False, n_threads=2)
