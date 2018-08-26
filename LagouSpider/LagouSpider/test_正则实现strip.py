#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-26 19:28:26

import re

def re_strip(s, t=r'\s'):
    t_format = r'^%s*|%s*$' % (t, t)
    # print(t_format)
    s_re = re.compile(t_format)
    s = s_re.sub('',s)
    return s

print(re_strip(')aadasdfsaaa', t=r'\W'))
print(re_strip('dafsdfasd,', t=r'\W'))



def re_strip(s):
    s = re.sub(r'^\W*|\W*$', '', s)
    return s

print(re_strip(')aadasdfsaaa'))
print(re_strip('dafsdfasd,'))