
import sys
sys.path.append('./../c3qts_factor')
from factor_system import FactorSystem
from test_factor import TestFactor
from c3qts.core.constant import Interval, Exchange
from c3qts.core.settings import SETTINGS

SETTINGS["database.basedir"] = '/14T/dev_database_factor'

test_factor_class = TestFactor(name='momentum', author='csh', freq_list=[Interval.TICK])
test_factor_system = FactorSystem(test_factor_class)
# test_factor_system.parallel_generate(['rb', 'ag'], n_threads=10)
test_factor_system.generate(product=['AG'], instrument='AG1801', exchange=Exchange.SHFE, write=True, append=False)
