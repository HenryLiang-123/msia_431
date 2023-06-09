#!/bin/bash

input_path="HW2Q1/*" # in hdfs
output_path="HW2Q1/out_q1" # in hdfs and must not exist
python_path=$(pwd)
hadoop_lib_path="/opt/hadoop/hadoop/share/hadoop/tools/lib"

yarn jar ${hadoop_lib_path}/hadoop-streaming-2.10.1.jar \
       -files ${python_path}/mapper.py,${python_path}/reducer.py \
    -input ${input_path} \
    -output ${output_path} \
    -mapper mapper.py \
    -reducer reducer.py
