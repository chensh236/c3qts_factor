from c3qts.core.constant import Interval
from c3qts_factor.factor_system import FactorSystem
from c3qts.core.settings import SETTINGS
SETTINGS["database.basedir"] = '/dev_data/database'

remove_list = FactorSystem.get_factor_list(SETTINGS["database.basedir"], 'sma', 'chensh236')
FactorSystem.remove_factor_list(SETTINGS["database.basedir"], remove_list)