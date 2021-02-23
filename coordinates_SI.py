#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
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
    for filename in sorted(os.listdir(current_dir)):
        path = current_dir + "/" + filename
        if filename.endswith(".out") and not filename.startswith("slurm"):
            out_path = path
            input_text = open(out_path, "r", encoding = "utf-8").read()
            #search for orca or cfour, cfour_freq or gaussian
            orca = re.findall(r" O   R   C   A ", input_text)
            cfour = re.findall(r"<<<     CCCCCC     CCCCCC", input_text)
            gaussian = re.findall(r"licensee that it is not a competitor of Gaussian", input_text)
            cfour_freq = re.findall(r"VIB=", input_text)
            is_ts_output = re.findall(r"imaginary", input_text)
            is_cfour_ts_output = re.findall(r"METHOD=TS", input_text)
            cfour_freq = re.findall("VIB=", input_text)
            img_freq_cfours = re.findall(r"Rotationally projected vibrational frequencies(.*?)i", input_text, flags=re.DOTALL)
            cfour_freq_geometry = re.findall(r"Coordinates used in calculation(.*?)Interatomic", input_text, flags=re.DOTALL)
            point_group_gaussian = re.findall(r"Full point group(.*?)NOp", input_text, flags=re.DOTALL)
            point_group_cfour = re.findall(r"Computational point group:(.*?)Initial", input_text, flags=re.DOTALL)

            if len(point_group_cfour) != 0:
                last_point_group_cfour = point_group_cfour[-1].replace("Computational point group:", "").replace("Initial", "").replace(" ", "").replace("1", u"\u2081").replace("2", u"\u2082").replace("3", u"\u2083").replace("V", u"\u1D65").replace("H", u"\u2095").replace("S", u"\u209B").replace("*", u"\u221e")
                last_point_group_cfour = last_point_group_cfour.replace("v", u"\u1D65").replace("h", u"\u2095").replace("s", u"\u209B").replace("*", u"\u221e")

            if len(is_ts_output) != 0:
                imaginary_frequencies_gaussians = re.findall(r"Frequencies -- *-[0-9]*[.]?[0-9]*", input_text)


            zero_point_cfours = re.findall(r"Zero-point energy: [\n ]?[+-]?[\n ]*[+-]?[0-9]*[\n ]*[0-9]*[\n ]*[.]?[\n ]*[0-9]+[\n ]*[0-9]+", input_text)

            final_electronic_energy_cfours = re.findall(r"The final electronic energy is [\n ]?[+-]?[\n ]*[+-]?[0-9]*[\n ]*[0-9]*[\n ]*[.]?[\n ]*[0-9]+[\n ]*[0-9]+", input_text)
            hfs = re.findall(r"H[\n ]?[\n ]?F[\n ]?[\n ]?=[\n ]?[\n ]?[+-]?[\n ]?[\n ]*[+-]?[0-9]*[\n ]*[0-9]*[\n ]*[.]?[\n ]*[0-9]+[\n ]*[0-9]+", input_text)
            
            zeropoints = re.findall(r"Z[\n ]?[\n ]?e[\n ]?[\n ]?r[\n ]?[\n ]?o[\n ]?[\n ]?P[\n ]?[\n ]?o[\n ]?[\n ]?i[\n ]?[\n ]?n[\n ]?[\n ]?t[\n ]?[\n ]?=[\n ]?[\n ]?[+-]?[\n ]?[\n ]*[+-]?[0-9]*[\n ]*[0-9]*[\n ]*[.]?[\n ]*[0-9]+[\n ]*[0-9]+",
                                    input_text)
            if len(final_electronic_energy_cfours) != 0:       
                final_electronic_energy_cfour = float(final_electronic_energy_cfours[-1].replace("\n ", "").replace(" ", "").replace("Thefinalelectronicenergyis", ""))
            if len(zeropoints) != 0:
                zero_point = float(zeropoints[-1].replace("\n ", "").replace("ZeroPoint=", ""))   
            if len(hfs) != 0:
                hf = float(hfs[-1].replace("\n ", "").replace("HF=", ""))
            if len(is_ts_output) != 0:    
                if len(imaginary_frequencies_gaussians) != 0:
                    img_freq_gaussian = imaginary_frequencies_gaussians[-1].replace("Frequencies --  ", "")
            if len(zero_point_cfours) != 0:
                zero_point_cfour = (float(zero_point_cfours[-1].replace("\n ", "").replace(" ", "").replace("Zero-pointenergy:", "")))/627.509608030592
            if len(img_freq_cfours) != 0:
                img_freq_cfour_crude = "\n".join(img_freq_cfours[-1].split("\n")[1:])
                img_freq_cfour_crude = img_freq_cfour_crude.strip()
                img_freq_cfour = img_freq_cfour_crude[2:].strip()
            if len(point_group_gaussian) != 0:
                last_point_group_gaussian = point_group_gaussian[-1].replace("point group", "").replace("NOp", "").replace(" ", "").replace("1", u"\u2081").replace("2", u"\u2082").replace("3", u"\u2083").replace("V", u"\u1D65").replace("H", u"\u2095").replace("S", u"\u209B").replace("*", u"\u221e")
            if len(gaussian) != 0:
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
                    print(filename.replace(remove_this, "") + " (" + str(last_point_group_gaussian) + ")")
                    print("")
                    print(geometry_cleanest)
                    print("")
                    print("E = " + str(hf) + " au")
                    print("ZPVE = " + str(zero_point) + " au")
                    if len(is_ts_output) != 0:
                        print(u'\U0001d708' + u"\u1D62" +" = " + str(img_freq_gaussian).replace("-", "") + u"\U0001D456" + " cm" + u"\u207B\u00B9 \n") #unicode rules i guess
                    else:
                        print("\n")
            if len(cfour) != 0:
                    full_geometry_blog_cfour = re.findall(r"Final ZMATnew file(.*?)CFOUR", input_text, flags=re.DOTALL)
                    if len(full_geometry_blog_cfour) != 0:
                        last_geometry_blog_cfour = full_geometry_blog_cfour[-1]
                        no_stars_geometry_blog_cfour = last_geometry_blog_cfour.replace("*", "")
                        geometry_blog_clean_cfour = "\n".join(no_stars_geometry_blog_cfour.split("\n")[3:-1]) #splits the blog in the right size
                        #print(geometry_blog_clean_cfour)
                        zmat_file = open("Zmat_file.zmat", "w")
                        zmat_file.write(geometry_blog_clean_cfour)
                        zmat_file.close()
                        result_cartesian_cfour = subprocess.run(["python3", "gc.py", "-zmat", "Zmat_file.zmat"], capture_output=True, text=True).stdout #make the nice cartesian coordinates
                        #print(result_cartesian_cfour)
                        result_cartesian_cfour_blog = "\n".join(result_cartesian_cfour.split("\n")[2:])
                        final_cartesian_cfour = result_cartesian_cfour_blog.replace("C", "6").replace("O", "8").replace("H", "1").replace("S", "16").replace("N", "7") #get numbers for elements
                        splitted_final_cartesian_cfour = final_cartesian_cfour.split("\n")

                        cartesian_list_cfour = []
                        for line in splitted_final_cartesian_cfour: #get rid of dummy atoms
                            if line.startswith("X"):
                                continue
                            if line.startswith("0"):
                                continue
                            else:
                                cartesian_list_cfour.append(line)  
                        final_cartesian_cfour_no_dummy = "\n".join(cartesian_list_cfour) #combine all lines back to one string to print it out

                        #now generate the output for the SI
                        print(filename.replace(remove_this, ""))
                        print("")
                        print(final_cartesian_cfour_no_dummy.replace("-0.00000", " 0.00000").replace("\t",""))
                        print("E = " + str(final_electronic_energy_cfour) + " au")
                        print("ZPVE =  au\n")

                    if len(cfour_freq) != 0:
                        if len(cfour_freq_geometry) != 0:
                            cfour_freq_geometry_blog = cfour_freq_geometry[-1]

                            cut_cfour_freq_geometry_blog = "\n".join(cfour_freq_geometry_blog.split("\n")[5:-3])

                            list_cfour_freq_blog_lines = cut_cfour_freq_geometry_blog.split("\n")
                            new_list_cfour_freq_blog_list = []
                            _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
                            for line in list_cfour_freq_blog_lines:
                                line_string = line[14:]
                                new_string = _RE_COMBINE_WHITESPACE.sub(" ", line_string).strip()
                                new_list_cfour_freq_blog_list.append(new_string)

                            Angstrom_translate = 0.529177249 #angstrom in bohr

                            new_values_cfour_list = []
                           
                            new_list_cfour_freq_blog_list_no_dummy = []
                            for line in new_list_cfour_freq_blog_list:
                                if line.startswith("0"):
                                    continue
                                else:
                                    new_list_cfour_freq_blog_list_no_dummy.append(line) 

                            for row in new_list_cfour_freq_blog_list_no_dummy:
                                row_list = row.split(" ")
                                new_row_list = []
                                new_string_1_2 = ""
                                new_string_3_4 = ""
                                row_string_angstrom = ""
                                for index_value in range(len(row_list)):
                                    
                                    if index_value == 0:
                                        new_row_list.append(row_list[index_value])
                                    else:
                                        value = Angstrom_translate * float(row_list[index_value])
                                        format_value = f"{value:.5f}"
                                        if str(format_value) == "-0.00000":
                                            new_row_list.append("0.00000")
                                        else:
                                            new_row_list.append(format_value)
                                
                                if int(new_row_list[0]) > 9 and (float(new_row_list[1]) <= 0 or str(new_row_list[1]) == "0.00000"):        #make sure that we have the nice equal spacing....
                                    new_string_1_2 = "  ".join(new_row_list[:2])
                                elif int(new_row_list[0]) > 9 or float(new_row_list[1]) > 0:
                                    new_string_1_2 = "   ".join(new_row_list[:2])
                                elif int(new_row_list[0]) < 9 and float(new_row_list[1]) > 0:
                                    new_string_1_2 = "    ".join(new_row_list[:2])
                                elif int(new_row_list[0]) < 9 and float(new_row_list[1]) <= 0: 
                                    new_string_1_2 = "  ".join(new_row_list[:2])
                                
                                if str(new_row_list[3]) == "0.00000":
                                    new_string_3_4 = "    ".join(new_row_list[2:])
                                elif float(new_row_list[3]) > 0:
                                    new_string_3_4 = "    ".join(new_row_list[2:])
                                elif float(new_row_list[3]) < 0:
                                    new_string_3_4 = "   ".join(new_row_list[2:])
                                


                                if float(new_row_list[2]) < 0:
                                    row_string_angstrom = new_string_1_2 + "   " + new_string_3_4
                                elif float(new_row_list[2]) > 0:
                                    row_string_angstrom = new_string_1_2 + "    " + new_string_3_4 
                                elif str(new_row_list[2]) == "0.00000":
                                    row_string_angstrom = new_string_1_2 + "    " + new_string_3_4 
                                new_values_cfour_list.append(row_string_angstrom)
                            new_values_cfour_blog = "\n".join(new_values_cfour_list)

                        new_values_cfour_blog_clean = new_values_cfour_blog.replace("-0.0 ", " 0.00000").replace("0.0 ", "0.00000")

                        print(filename.replace(remove_this, "") + " (Comp. point group = " + str(last_point_group_cfour.replace("\n", "").replace(" ", "")) + ")")
                        print("")
                        print(new_values_cfour_blog_clean + "\n")
                        print("E = " + f"{float(final_electronic_energy_cfour):.10f}" + " au")
                        print("ZPVE = " + f"{float(zero_point_cfour):.10f}" + " au")
                        if len(is_cfour_ts_output) != 0:
                            print(u'\U0001d708' + u"\u1D62" +" = " + f"{float(img_freq_cfour):.10f}" + u"\U0001D456" + " cm" + u"\u207B\u00B9 \n") 
                        else:
                            print("\n")
                    
                    

                    else:
                        continue
            else:
                continue

        elif os.path.isdir(path):
            q.append(path)

sys.stdout = orig_stdout
f.close()