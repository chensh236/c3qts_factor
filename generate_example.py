from factor_system import FactorSystem
from factor_class.cyh.test_factor import test

test_factor_class = test()
test_factor_system = FactorSystem(test_factor_class)
test_factor_system.parallel_generate(['rb', 'ag'], n_threads=10)