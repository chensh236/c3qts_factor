#  C3QTS系统的因子模块
<p align="center">
  <img src ="https://gitee.com/ccc-quantitative-team/img/raw/master/C3QTS%20%E4%B8%BBLOGO%20800x600.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-0.0.1-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.9-blue.svg" />
</p>

## 说明

`c3qts_factor`模块是一个包含因子计算和管理功能的模块，它主要由两个子模块构成：factor_system和factor。factor_system模块提供了因子生成和处理的功能，如并行生成因子、按日期区间计算因子等，它的核心是FactorSystem类，该类实例化时接受一个因子类作为参数。factor模块定义了一个名为Factor的抽象基类，用于创建具体的因子类。因子类需要继承Factor基类并实现具体的因子计算逻辑。`c3qts_factor`模块使得用户可以方便地创建和管理因子，以满足各种因子分析和策略开发需求。
## 函数解析
```
factor_system.py
factor.py
```
### factor_system.py

factor_system模块中定义了一个名为FactorSystem的类，用于处理因子生成的任务。该类主要包括两个方法：generate和parallel_generate。FactorSystem类包含以下方法：

#### init
```python
__init__(self, factor_class): 
```
初始化方法，接受一个因子类作为参数，用于计算因子。同时，它创建一个LocaldbDatabase实例来处理数据库相关操作。

参数：
factor_class: 传入具体的因子类。
```python
generate(self, instrument, begin_datetime=None, end_datetime=None, symbol_type=ContractType.MERGE_ORI, write=False, append=False): 
```
生成指定合约的因子。参数如下：

- instrument: 合约名。
- begin_datetime: 因子生成的开始时间。
- end_datetime: 因子生成的结束时间。
- symbol_type: 合约类型，默认为ContractType.MERGE_ORI。
- write: 是否将计算结果写入数据库，默认为False。
- append: 是否在已有因子基础上追加计算结果，默认为False。


#### get_factor_list (静态函数)
为方便合并因子数据，FactorSystem类也包括因子的搜索功能。

```python
@staticmethod
def get_factor_list(database_dir: str, factor_name: str = '', author: str = '', product_name=Product.FUTURES, full: bool=False, interval: Interval=Interval.TICK)
功能：根据因子名称和作者名称，从数据库中获得不同周期的因子列表。如若full为True则只返回存在主力合约的因子，否则返回所有因子。

参数：

- database_dir (str)：数据库目录。
- factor_name (str)：因子名称，默认为空。当因子名称和作者名称都为空时，将报错并返回None。
- author (str)：作者名，默认为空。当因子名称和作者名称都为空时，将报错并返回None。
- product_name：产品类型，默认为期货。
- full (bool)：是否只返回存在主力合约的因子，默认为False。
- interval：时间间隔，默认为TICK。

返回值：

- factor_list：符合筛选条件的因子列表。

使用方法：

```python
factor_list = FactorSystem.get_factor_list(database_dir, factor_name='Factor1', author='Author1', full=True)
```

示例代码调用了 get_factor_list 函数，传入数据库目录、因子名称、作者名称、产品类型、筛选条件和时间间隔，函数将返回一个包含符合筛选条件的因子列表。如果因子名称和作者名称都为空，将会报错并返回None。

#### remove_factor_list (静态函数)
```python
@staticmethod
def remove_factor_list(database_dir, factor_list, author: str='', product_name=Product.FUTURES, interval: Interval=None, contract_type: ContractType=None, variety_list=[]):
```

功能：批量删除因子。

参数：

- database_dir：数据库目录。
- factor_list：要删除的因子列表。
- author (str)：作者名，默认为空。
- product_name：产品类型，默认为期货。
- interval：时间间隔，默认为None。
- contract_type：合约类型，默认为None。
- variety_list：品种列表，默认为空列表。

使用方法：

```python
from c3qts.core.constant import Interval
from c3qts_factor.factor_system import FactorSystem
from c3qts.core.settings import SETTINGS
SETTINGS["database.basedir"] = '/dev_data/database'

remove_list = FactorSystem.get_factor_list(SETTINGS["database.basedir"], 'sma', 'chensh236')
FactorSystem.remove_factor_list(SETTINGS["database.basedir"], remove_list)
```
示例代码首先调用 get_factor_list 函数获取要删除的因子列表，然后调用 remove_factor_list 函数删除这些因子。在删除因子之前，会提示用户确认是否要继续删除。如果用户输入'y'，则继续删除；如果输入'n'，则取消操作。

#### remove_factor (静态函数)
```python
@staticmethod
def remove_factor(database_dir, factor_name, author: str='', product_name=Product.FUTURES, interval: Interval=None, contract_type: ContractType=None, variety_list=[], confirm=False):
```

功能：根据因子名称和作者名称删除因子。

参数：

- database_dir：数据库目录。
- factor_name：要删除的因子名称。
- author (str)：作者名，默认为空。
- product_name：产品类型，默认为期货。
- interval：时间间隔，默认为None。
- contract_type：合约类型，默认为None。
- variety_list：品种列表，默认为空列表。
- confirm：是否需要用户确认，默认为False。

使用方法：

```python
from c3qts.core.constant import Interval
from c3qts_factor.factor_system import FactorSystem
from c3qts.core.settings import SETTINGS
SETTINGS["database.basedir"] = '/dev_data/database'

FactorSystem.remove_factor(SETTINGS["database.basedir"], 'Factor1', 'Author1', interval=Interval.D1)
```

示例代码调用了 remove_factor 函数，传入数据库目录、因子名称、作者名称、产品类型、时间间隔等参数，函数将删除符合条件的因子。在删除因子之前，会提示用户确认是否要继续删除。如果用户输入'y'，则继续删除；如果输入'n'，则取消操作。

#### parallel_generate
```python
parallel_generate(self, products='All', begin_datetime=None, end_datetime=None, symbol_type=ContractType.MERGE_ORI, write=False, append=False, n_threads=1): 
```
并行生成指定品种的因子。参数如下：

- products: 品种列表，默认为'All'，表示全部品种。
- begin_datetime: 因子生成的开始时间。
- end_datetime: 因子生成的结束时间。
- symbol_type: 合约类型，默认为ContractType.MERGE_ORI。
- write: 是否将计算结果写入数据库，默认为False。
- append: 是否在已有因子基础上追加计算结果，默认为False。
- n_threads: 并行处理的线程数，默认为1。

示例代码
```python
# 创建 FactorSystem 实例，传入因子类
factor_system = FactorSystem(factor_class=YourFactorClass)
# 生成特定合约的因子
factor_system.generate(instrument="AG2203", begin_datetime="20220101", end_datetime="20220301", write=True, append=False)
# 并行生成指定品种的因子
factor_system.parallel_generate(products=["AG"], begin_datetime="20220101", end_datetime="20220301", write=True, append=False, n_threads=32)
```
在这个示例代码中，首先创建了一个FactorSystem实例，并传入了一个因子类。然后分别调用generate方法和parallel_generate方法生成特定合约和品种的因子。

### factor.py
该模块中定义了一个名为Factor的抽象类，作为所有因子类的基类。这个抽象类提供了因子计算的基本框架，包括因子的名称、作者和频率列表。各具体因子类需要继承这个基类并实现compute方法，以完成因子的计算。Factor类包含以下属性和方法：
- name: 因子名称，字符串类型。
- author: 因子作者，字符串类型。
- freq_list: 因子计算需要的频率列表，列表类型。

#### init
```python
__init__(self, name, author, freq_list): 
```
初始化方法，接受因子名称、作者和频率列表作为参数。

#### compute
```python
compute(self, data, timestamp, column_dict) -> dict: 
```
计算因子的方法。子类需要重写这个方法以实现具体的因子计算逻辑。参数如下：

- data: 用于计算因子的数据，通常是一个二维数组。
- timestamp: 数据对应的时间戳列表。
- column_dict: 数据的列名字典，键是列名，值是列索引。
返回值是一个字典，键是因子名称，值是一个包含时间戳列表和因子值列表的元组。

```python
# 创建一个继承 Factor 的自定义因子类
class CustomFactor(Factor):
    def __init__(self):
        super().__init__(name="CustomFactor", author="YourName", freq_list=[Interval.TICK])

    def compute(self, data, timestamp, column_dict) -> dict:
        result_dict = {}
        # 计算因子逻辑
        # ...
        return result_dict

# 创建 CustomFactor 实例
custom_factor = CustomFactor()

# 在 FactorSystem 中使用自定义因子类
factor_system = FactorSystem(factor_class=CustomFactor)
```
在这个示例代码中，首先创建了一个名为CustomFactor的自定义因子类，继承自Factor抽象类。然后重写了compute方法以实现具体的因子计算逻辑。最后，在FactorSystem实例中使用自定义因子类。

注意事项：
- 在读取的时候，需要以'{factor_name}_{author}'的形式来读取；
- 日期统一以str类型的变量，如:20220101或者20220101000000000（如果只有日期自动填充，日期范围为左闭，右闭）
- data与index的类型均为np.ndarray
