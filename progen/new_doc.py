import os
import argparse

PARAMETER_TEMPLATE = """
# parameter

| 名称   | 说明                               | 默认值 |
| ------ | ---------------------------------- | ------ |

"""

PORT_TEMPLATE = """ 
# port

| 名称      | 类型  | 位宽   | 说明                 |
| --------- | ----- | ------ | -------------------- |
| clk       | input | 1      | 系统时钟             |
| rst_n     | input | 1      | 系统复位信号，低有效 |

"""

DEPENDENT_TEMPLATE = """
# dependent

- <dependent>/<file>/<path>
"""

LINK_TEMPLATE = """
# link

| inst name | module name |
| --------- | ----------- |

- inst1.port1 <> inst2.port
"""

parser = argparse.ArgumentParser()
parser.add_argument("name", help="name of module")
parser.add_argument("-r", "--root_path", help="root path of module doc",default="module_doc")
parser.add_argument("-p", "--parameter",help="need parameter or not,default not need",action='store_true',default=False)
parser.add_argument("-l", "--link",help="need link or not,default not need",action='store_true',default=False)
parser.add_argument("-d", "--dependent",help="need dependent or not,default not need",action='store_true',default=False)
args = parser.parse_args()

module_name = args.name
root_path = args.root_path
is_parameter = args.parameter
is_link = args.link
is_dependent = args.dependent

# check path
if not os.path.exists(root_path):
    raise ValueError("FATAL:root path {} not exists".format(root_path))
target_path = os.path.join(root_path,"{}.md".format(module_name))
if os.path.exists(target_path):
    raise ValueError("FATAL:module {} is already exists".format(module_name))

# generate template
if is_parameter:
    result = [PARAMETER_TEMPLATE,PORT_TEMPLATE]
else:
    result = [PORT_TEMPLATE]
if is_dependent:
    result.append(DEPENDENT_TEMPLATE)
if is_link:
    result.append(LINK_TEMPLATE)
result = "".join(result)

# save file
with open(target_path,'w') as f:
    f.write(result)
print("INFO:module doc {} generate successful in {}".format(module_name,target_path))