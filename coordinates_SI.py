#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os #operating system
import re
import argparse 
from distutils.dir_util import copy_tree
import subprocess
#if u need arguments from user
#from argpase import ArgumentParser (direct ArgumentParser importieren)
#import module

parser = argparse.ArgumentParser() #parser is a variable, argpaser from module 
parser.add_argument('input_dir') #first argument from user folder
parser.add_argument("remove_this")

#parser.add_argument("second_argument") for second argument, if needed

args = parser.parse_args()

#second_dir = args.second_argument for second argument, if needed
input_dir = args.input_dir
remove_this = args.remove_this



orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

current_dir = input_dir

q = [input_dir] #variable q, take list [input_dir]
i = 1

while len(q) > 0:
    current_dir = q[0]
    q = q[1:]
    for filename in os.listdir(current_dir):
        path = current_dir + "/" + filename
        if filename.endswith(".out") and not filename.startswith("slurm"):
            out_path = path
            input_text = open(out_path, "r", encoding = "utf-8").read()
            #search for orca or cfour, cfour_freq or gaussian
            orca = re.findall(r" O   R   C   A ", input_text)
            cfour = re.findall(r"<<<     CCCCCC     CCCCCC", input_text)
            gaussian = re.findall(r"licensee that it is not a competitor of Gaussian", input_text)
            cfour_freq = re.findall(r"VIB=", input_text)

            hfs = re.findall(r"H[\n ]?[\n ]?F[\n ]?[\n ]?=[\n ]?[\n ]?[+-]?[\n ]?[\n ]*[+-]?[0-9]*[\n ]*[0-9]*[\n ]*[.]?[\n ]*[0-9]+[\n ]*[0-9]+", input_text)
            
            zeropoints = re.findall(r"Z[\n ]?[\n ]?e[\n ]?[\n ]?r[\n ]?[\n ]?o[\n ]?[\n ]?P[\n ]?[\n ]?o[\n ]?[\n ]?i[\n ]?[\n ]?n[\n ]?[\n ]?t[\n ]?[\n ]?=[\n ]?[\n ]?[+-]?[\n ]?[\n ]*[+-]?[0-9]*[\n ]*[0-9]*[\n ]*[.]?[\n ]*[0-9]+[\n ]*[0-9]+",
                                    input_text)

            if len(zeropoints) != 0:
                zero_point = float(zeropoints[-1].replace("\n ", "").replace("ZeroPoint=", ""))   
            if len(hfs) != 0:
                hf = float(hfs[-1].replace("\n ", "").replace("HF=", ""))

            #insert what to search
            full_geometry_blog = re.findall(r"Standard orientation:(.*?)Rotational", input_text, flags=re.DOTALL)
            if len(full_geometry_blog) != 0:
                last_geometry_blog = full_geometry_blog[-1]
                geometry_blog_clean = "\n".join(last_geometry_blog.split("\n")[5:-2])
                geometry_lines = geometry_blog_clean.split("\n")
                geometry_cleaner = []
                for line in geometry_lines:
                    line_string = line[16:19] + line[35:]
                    geometry_cleaner.append(line_string)
                    line_string = ""
                geometry_cleanest = "\n".join(geometry_cleaner)
                print(filename.replace(remove_this, ""))
                print("")
                print(geometry_cleanest)
                print("")
                print("E = " + str(hf) + " au")
                print("ZPVE = " + str(zero_point) + " au\n")

            else:
                continue

        elif os.path.isdir(path):
            q.append(path)

sys.stdout = orig_stdout
f.close()