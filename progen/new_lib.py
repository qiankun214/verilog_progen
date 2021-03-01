import json
import json
import os
import argparse
from lib_decoder import compiler_lib_info

parser = argparse.ArgumentParser()
parser.add_argument("name", help="name of lib",default="lib")
parser.add_argument("-s", "--save_root", help="save path of json",default=".")
parser.add_argument("-i", "--io",help="need io or not,default not need",action='store_true',default=False)
parser.add_argument("-m", "--macro",help="need macro or not,default not need",action='store_true',default=False)
args = parser.parse_args()

root = args.save_root
name = args.name
is_io = args.io
is_macro = args.macro

info = compiler_lib_info(name,root)
info.dump(is_io,is_macro)
