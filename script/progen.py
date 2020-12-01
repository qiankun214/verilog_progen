import argparse
from utils import design_generate, markdown_analysis, testbench_generate
# from md2json import md2json
# from json2vsv import json2vsv
import os

# def json_path_generate():
#     script_path = os.path.split(os.path.realpath(__file__))[0]
#     root = os.path.split(script_path)[0]
#     return os.path.join(root,"info")

# def generate_vsv(source,tb,rtl,is_update=True):
#     m2j = md2json(source,json_path_generate())
#     m2j()
#     j2vsv = json2vsv(m2j.js_path,rtl,tb)
#     j2vsv(is_update)

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--markdown", help="input markdown file path")
parser.add_argument("-t", "--tb", help="output testbench root",default="./testbench")
parser.add_argument("-d", "--design", help="output rtl design root",default="./rtl")
parser.add_argument("-u", "--noupdate",help="if your donnot want keep your work,use '-u'",action='store_false')
args = parser.parse_args()
# print(args.update)

# generate_vsv(args.markdown,args.tb,args.design,args.noupdate)
name = markdown_analysis(
    path=args.markdown,
    rtl_root=args.design,
    tb_root=args.tb
)
# print(args.noupdate)
design_generate(name,args.noupdate)
testbench_generate(name,args.noupdate)