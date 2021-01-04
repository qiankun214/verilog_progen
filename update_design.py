import os
import argparse

OLD_SPILT = "//progen-spilt:work after here"
NEW_START = "// pro-gen:start here,coding before this line"
NEW_STOP = "// pro-gen:stop here,coding after this line"

parser = argparse.ArgumentParser()
parser.add_argument("root", type=str,help="root of design")
parser.add_argument("-d","--design_root", type=str,help="root name of rtl",default="rtl")
parser.add_argument("-t","--testbench_root", type=str,help="root name of testbench",default="testbench")
args = parser.parse_args()
root = args.root
ds_root = args.design_root
tb_root = args.testbench_root

# check path
if not os.path.exists(root):
    raise ValueError("FATAL:root path {} not exists".format(root))

ds_root = os.path.join(root,ds_root)
if not os.path.join(ds_root):
    raise ValueError("FATAL:rtl path {} not exists".format(ds_root))


# renew
rtl_path = [os.path.join(ds_root,x) for x in os.listdir(ds_root) if ".v" in x]
for path in rtl_path:
    with open(path,'r') as f:
        rtl = f.read()
    if OLD_SPILT in rtl:
        rtl = "{}\n{}".format(NEW_START,rtl)
        rtl = rtl.replace(OLD_SPILT,NEW_STOP)
    # print(rtl)
    # break
    with open(path,'w') as f:
        f.write(rtl)
    print("INFO:renew rtl {} successful".format(path))


tb_root = os.path.join(root,tb_root)
# print(tb_root)
if not os.path.join(tb_root):
    print("WARING:testbench path {} not exists".format(tb_root))
else:
    testbench_path = [os.path.join(tb_root,x) for x in os.listdir(tb_root) if ".sv" in x]
    for path in testbench_path:
        with open(path,'r') as f:
            tb = f.read()
        if OLD_SPILT in tb:
            tb = "{}\n{}".format(NEW_START,tb)
            tb = tb.replace(OLD_SPILT,NEW_STOP)
        # print(tb)
        # break
        with open(path,'w') as f:
            f.write(tb)
        print("INFO:renew testbench {} successful".format(path))