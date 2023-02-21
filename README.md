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
因子生成、因子保存
## 使用
- 在读取的时候，需要以'{factor_name}_{author}'的形式来读取；
- 日期统一以str类型的变量，如:20220101或者20220101000000000（如果只有日期自动填充，日期范围为左闭，右闭）
- data与index的类型均为np.ndarray
