#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-26 22:59:20

# 手动清理数据

import pandas as pd

df = pd.read_table('rank.tsv', sep=' ', names=['terms', 'frequency'], header=0)
df.terms