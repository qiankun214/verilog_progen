# 生成工具

本项目用于直接通过可读的markdown文本生成rtl设计中需要使用的verilog模板和SystemVerilog的TB的模板，后续将添加其他功能。使用方法为按要求编写markdown文本，随后使用如下命令：

```shell
python3 <root>/progen/progen <markdown path> -d <rtl root> -t <tb root>
```

同时可以使用如下指令查询：

```
python3 <root>/progen/progen -h
```


## md格式定义

md定义模块信息需要包括以下方面：
- 基本信息：模块名称
- parameter：模块外部可变参数信息，包括名称
- port：模块端口信息，包括端口类型、参数和名称（描述以注释的方式存在）
- link: 描述链接信息，包括子模块，连线等
- dependent: 描述依赖的文件，如不适用link自动例化的模块文件

其中，基本信息以文件名的方式提供，其他包括在md文件中，一个例子如下所示：


```markdown
# parameter

| 名称   | 说明                               | 默认值 |
| ------ | ---------------------------------- | ------ |
| DWIDTH | 单个数据位宽                       | 16     |
| AWIDTH | 主cache地址总线位宽                | 16     |
| OWIDTH | 临时cache地址总线位宽              | 8      |
| PWIDTH | PE阵列地址位宽（log_2(PE\_ROW)） | 4      |
| PE_ROW | PE阵列的行数，与PE阵列列数相等     | 12     |
| PE_COL | PE阵列的列数，与PE阵列行数相等     | 12     |

# port

## 系统端口

| 名称  | 类型  | 位宽 | 说明                 |
| ----- | ----- | ---- | -------------------- |
| clk   | input | 1    | 系统时钟             |
| rst_n | input | 1    | 系统复位信号，低有效 |

## 配置-指令端口

| 名称          | 类型   | 位宽        | 说明                                 |
| ------------- | ------ | ----------- | ------------------------------------ |
| cfg_valid     | input  | 1           | 指令输入有效信号，高有效             |
| cfg_busy      | output | 1           | 指令正在执行信号，高表示正在执行指令 |
| cfg_data_data | input  | DATA_CWIDTH | 数据准备部分指令                     |
| cfg_wicp_data | input  | WICP_CWIDTH | 权值-计算部分指令                    |
| cfg_tmpc_data | input  | TMPC_CWIDTH | 临时cache部分指令                    |
| cfg_post_data | input  | POST_CWIDTH | 后处理部分指令                       |

## 存储器端口

| 名称                | 类型   | 位宽             | 说明                     |
| ------------------- | ------ | ---------------- | ------------------------ |
| outside_memory_addr | input  | AWIDTH           | 外部存储器访问端口       |
| outside_memory_wreq | input  | 1                | 外部存储器写请求，高有效 |
| outside_memory_din  | input  | DWIDTH * PE_ROW​ | 外部存储器写数据         |
| outside_memory_dout | output | DWIDTH * PE_ROW​ | 外部存储器读数据         |

# dependent

- ./rtl/testtest.v

# link

| 实例化名    | 模块名    |
| ----------- | --------- |
| inst_test_a | test_dout |
| inst_test_b | test_din   |
| inst_test_c | test_din   |

- inst_test_a.dout_valid <> inst_test_b.din_valid
- inst_test_a.dout_data <> inst_test_b.din_data
- inst_test_a.dout_valid <> inst_test_c.din_valid
- inst_test_a.dout_data <> inst_test_c.din_data

```

对应的markdown包括四块内容，分别是parameter信息、port信息、dependent信息和link信息。parameter信息和port信息均以markdown表格语法存储，表头信息而言：
- parameter：表头顺序为名称、说明和默认值，顺序不可改变
- port：表头顺序为名称、类型、位宽和说明

dependent使用markdown中的无序列表描述，需要直接给出文件路径，系统在进行生成时会检查该文件是否存在，因此需要在生成前将依赖文件放置在指定的位置。

需要注意的是，名称和说明栏类型为string，位宽为数字表达式，可以使用parameter部分定义的参数。link部分使用专门格式编写，用于描述子模块和连接关系，若没有调用子模块可以不写，link部分包括一个表格和链接关系描述符：
- 表格：为实例化名-模块名的对用关系，模块必须由progen生成过（info文件夹中有对用的json文件）
- 连接关系，格式如下所示：
``` markdown
- <实例化名>.<端口名> <> <实例化名>.<端口名>
```

生成的Verilog中会包含以下一句注释：

```
// pro-gen:start here,coding before this line
```
这是用于标注progen生成的开始位置，请务必在这句注释上方进行代码编写，该语句下方的代码会在更新时被删除。还会包括以下注释：

```
// pro-gen:stop here,coding after this line
```

这是用于标注progen生成的结束位置，请务必在这句注释下方进行代码编写，该语句上方的代码会在更新时被删除。

# filelist生成

使用方法为

```shell
python3 script/filelistgen.py -v <模块名> -o <输出filelist路径> -t
```

其中添加`-t`表示在filelist中增加TB文件路径，用于vcs仿真，不添加则生成全部为rtl文件filelist

# 代码提交

在前端工作完成后，需要将代码提交给后端进行正式的综合和物理实现，此时需要将所有代码打包到一个文件中，脚本`progen/submit.py`可实现该功能，用法为：

```shell
usage: submit.py [-h] [-i INFO_ROOT] [-m] [-p PRE] verilog

positional arguments:
  verilog               module name to submit

optional arguments:
  -h, --help            show this help message and exit
  -i INFO_ROOT, --info_root INFO_ROOT
                        info root
  -m, --makefile        use makefile to nlint,default is true
  -p PRE, --pre PRE     nlint order name in makefile module,default is make
```

`verilg`为要提供的模块名（不是文件路径），该脚本的行为如下所示：
- 根据json文件分析依赖关系，生成filelist（不保存）
- 根据filelist将所有依赖的代码顺序拼接到一起
- 将结果保存在路径`submit_workspace/SUBMIT_<verilog>.v`中，若`submit_workspace`已经存在，则将其删除后重建
- 对提交结果进行nlint检查

# EDA工具

EDA工具提供以下脚本：

- [x] nLint代码风格检查
- [x] VCS仿真
- [x] Verdi波形查看
- [ ] DC综合（正在开发）

## nLint代码检查

nlint进行代码检查，位于`<root>/progen/eda_nlint.py`。运行脚本如下所示：

```
usage: eda_nlint.py [-h] [-a] [-m] [-p PRE] [-i INFO_ROOT] module

positional arguments:
  module                module name you want to nlint

optional arguments:
  -h, --help            show this help message and exit
  -a, --macro           submodule of this module handle as macro cell
  -m, --makefile        use makefile to nlint,default is true
  -p PRE, --pre PRE     nlint order name in makefile module,default is make
  -i INFO_ROOT, --info_root INFO_ROOT
                        root path of infoy
```

makefile模式为生成一个makefile脚本，并将命令写入makefile中，随后以make命令运行脚本，使用`-p PRE`可以改变运行make的命令，默认为`make`。`-a`表示是否以macro模式运行，在macro模式下将不会检查子模块。

该脚本所有结果保存在nlint_workspace文件夹中，若之前存在nlint_workspace文件夹则会将nlint_workspace删除。

该脚本产生的makefile会生成在运行目录下，若原本存在makefile，则会将原有的makefile重命名为makefile_old，若原本存在makefile_old，则将其删除。

## VCS仿真工具

vcs进行仿真，位于`<root>/progen/eda_vcs.py`。运行脚本如下所示：

```
usage: eda_vcs.py [-h] [-s SIMMODE] [-m] [-p PRE] [-i INFO_ROOT] module

positional arguments:
  module                module name you want to nlint

optional arguments:
  -h, --help            show this help message and exit
  -s SIMMODE, --simmode SIMMODE
                        simmode pre or post
  -m, --makefile        use makefile to nlint,default is true
  -p PRE, --pre PRE     nlint order name in makefile module,default is make
  -i INFO_ROOT, --info_root INFO_ROOT
                        root path of info
```

simmode用于指定rtl仿真、网表仿真还是后仿，目前仅支持rtl仿真，即`pre`（默认值）。其他行为与nlint脚本相同

## verdi波形查看

打开verdi进行代码查看，位于`<root>/progen/eda_verdi.py`，运行脚本如下所示：

```
usage: eda_verdi.py [-h] [-s SIMMODE] [-m] [-p PRE] [-i INFO_ROOT] module

positional arguments:
  module                module name you want to nlint

optional arguments:
  -h, --help            show this help message and exit
  -s SIMMODE, --simmode SIMMODE
                        simmode pre or post
  -m, --makefile        use makefile to nlint,default is true
  -p PRE, --pre PRE     nlint order name in makefile module,default is make
  -i INFO_ROOT, --info_root INFO_ROOT
                        root path of info
```

参数说明和行为与nlint和vcs相同
