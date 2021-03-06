# -*-coding:utf-8-*-
# author:ZhuHaitao

import sys
import numpy as np

# Function-读取固定行
def readlines(f,number_of_lines):
    lines = []
    for ii in range(number_of_lines):
        lines.append(f.readline())
    return lines

# Function-提取该行数据里的时间戳(str)
def get_line_time_stamp(line):
    line_time_stamp = line.split(' ')[0].replace('@', ' ')
    return line_time_stamp

# Function-找到起始时间行00.000(start)
def find_start(f):
    while 1:
        line = f.readline()
        if get_line_time_stamp(line).split(':')[-1]=='00.000':
            start = line
            return start

# Function-将时间索引(str)转换成自然数索引(1:1440)
def transfer_time_to_number(line_time_stamp):
    time_stamp = line_time_stamp.split(' ')[-1].split(':')
    time_stamp = [float(i) for i in time_stamp]
    number = int(time_stamp[0]*60 + time_stamp[1])
    return number

# Function-转成待写入行(str)
def transfer_to_prepared_line(start, RMS):
    line_time_stamp = get_line_time_stamp(start)
    prepared_line = str(transfer_time_to_number(line_time_stamp)) + ' ' +  str(RMS) + '\n'
    return prepared_line

# Function-计算RMS
def calculate_RMS(list):
    accelerate = [float(x.split(' ')[-1].strip()) for x in list]
    RMS = np.sqrt(sum(x ** 2 for x in accelerate)/len(accelerate))
    return RMS

# 参数输入
main_path = sys.argv[1]
day_specified = sys.argv[2]
long = int(sys.argv[3])
Fs = int(sys.argv[4])
RMS_path = sys.argv[5]

# main_path = r'G:\研一下\宁波站数据\Export-x-accelerate\A-W-GGL1-2-Xx-accelerate'
# day_specified = '2014-06-08'
# long = 6000 # 样本长度
# Fs = 100 # 采样频率
# RMS_path = main_path + '\\' + 'RMS-' + day_specified + '.txt'

# 获取一整天的RMS
RMS_data = []
file_path = main_path + '\\' + day_specified + '.txt'
with open(file_path, 'r') as f:
    while True:
        start = f.readline()
        if get_line_time_stamp(start).split(':')[-1] != '00.000':
            start = find_start(f)
        accelerate = [float(start.split(' ')[-1])]
        lines = readlines(f, long - 1) # start已经占用了一个
        if lines[-1] == '':
            break
        RMS = calculate_RMS(lines)
        prepared_line = transfer_to_prepared_line(start, RMS)
        RMS_data.append(prepared_line)

# 将结果写入文件
with open(RMS_path,'w') as f:
    f.writelines(RMS_data)
