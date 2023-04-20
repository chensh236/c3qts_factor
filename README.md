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
