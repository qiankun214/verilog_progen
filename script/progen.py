import argparse
from md2json import md2json
from json2vsv import json2vsv
import os

def json_path_generate():
    script_path = os.path.split(os.path.realpath(__file__))[0]
    root = os.path.split(script_path)[0]
    return os.path.join(root,"json_md")

def generate_vsv(source,tb,rtl):
    m2j = md2json(source,json_path_generate())
    m2j()
    j2vsv = json2vsv(m2j.js_path,rtl,tb)
    j2vsv()

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--markdown", help="input markdown file path")
parser.add_argument("-t", "--tb", help="output testbench root",default="./testbench")
parser.add_argument("-d", "--design", help="output rtl design root",default="./rtl")
args = parser.parse_args()

generate_vsv(args.markdown,args.tb,args.design)