# 基于朴素贝叶斯的垃圾邮件分类器

### 数据集
https://plg.uwaterloo.ca/cgi-bin/cgiwrap/gvcormac/foo06
来自uwateloo收集的邮件数据，本代码采用中文邮件版本(`trec06c`),里面包含了60000多条中文邮件数据，在`index`里面已经标注好了那些是SPAM(垃圾邮件)或者HAM(正常邮件)。

### 使用
下载数据集到项目目录，运行`PreData(SPAM).py`得到预处理好的data目录，再运行`train.py`预测结果。