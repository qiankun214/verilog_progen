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
- [x] DC综合（正在开发）

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

## DC综合

使用DC进行综合，综合前需要填写如下的json文件，json文件可以使用`progen/new_lib.py`脚本生成，该脚本的运行方法如下所示：

```shell
usage: new_lib.py [-h] [-s SAVE_ROOT] [-i] [-m] name

positional arguments:
  name                  name of lib

optional arguments:
  -h, --help            show this help message and exit
  -s SAVE_ROOT, --save_root SAVE_ROOT
                        save path of json
  -i, --io              need io or not,default not need
  -m, --macro           need macro or not,default not need
```

其中，name表示库的名称，SAVE_ROOT为保存的路径，例如需要将json文件保存在`./lib/lib1.json`路径下，name应当为`lib1`，SAVE_ROOT应当为`./lib`。
io和macro分别表示是否需要导入IO库和Marco cell，生成的json如下所示：

```json
{
    "standcell": {
        "fast_db": "延迟最小的库的db文件路径",
        "fast_tluplus": "延迟最小的库的tluplus文件",
        "fast_condition": "延迟最小的库中选择的condition",
        "slow_db": "延迟最大的库的db文件路径",
        "slow_tluplus": "延迟最大的库的tluplus文件",
        "slow_condition": "延迟最大的库中选择的condition",
        "symbol_sdb": "符号库文件路径（可以为空）",
        "tf_file": "工艺tf文件路径",
        "map_file": "tluplus的map文件路径",
        "mw_path": "standcell的milkway文件夹路径"
    },
    "io": { // 若在生成时不添加`-i`则没有，io库功能尚未测试
        "db_path": "io库的db文件路径",
        "mw_path": "io库的milkway库路径"
    },
    "macro": { // 若在生成时不添加`-m`则没有，marco库功能尚未测试
        "db_path": [], // 列表，macro cell的db库路径
        "mw_path": []  // 列表，macro cell的milkway库路径
    }
}
```

用户需要填写上述json作为DC调用库的依据，使用dc综合的脚本如下所示，脚本位于`progen/eda_dc.py`：
```shell
usage: eda_dc.py [-h] [-n NAME] [-m] [-p PRE] [-i INFO_ROOT] [-r] [-s] [-c CYCLE] [--input INPUT] [--output OUTPUT] [--uncertainty UNCERTAINTY] lib_path

positional arguments:
  lib_path              path of lib json

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  module name you want to syn
  -m, --makefile        use makefile to nlint,default is true
  -p PRE, --pre PRE     nlint order name in makefile module,default is make
  -i INFO_ROOT, --info_root INFO_ROOT
                        root path of info
  -r, --run             run dc script,default is false
  -s, --script          not rewrite script,default is true(no rewrite)
  -c CYCLE, --cycle CYCLE
                        clock cycle
  --input INPUT         input delay factor
  --output OUTPUT       output delay factor
  --uncertainty UNCERTAINTY
                        output delay factor
```

与其他不同的eda系列脚本不同的是：
- `-r`/`--run`选项用于标记是否执行脚本，若不添加该命令，则将不会运行脚本（所有环境生成均会完成）
- `-s`/`--script`选项用于标记是否重写覆盖原有的tcl脚本，若不添加该命令，则仅会重置环境、生成verilog和filelist文件，且保持原有的tcl综合脚本和sdc脚本不变
- `-c`/`--cycle`用于输入时钟周期，单位为ns
- `--input`/`--output`/`--uncertainty`用于指定input delay、output delay和时钟的uncertainty，其值为`cycle`和对应的factor相乘，例如input delay的实际值为`--cycle * --input`

该脚本运行会进行如下操作：
1. 建立`dc_workspace`目录，若已经有`dc_workspace`目录，则将其删除后重新建立。
2. 根据`--name`指定的模块名，找到模块及其依赖，将其打包到一个文件，文件保存在`dc_workspace/input/<--name>.v`，同时生成filelist文件保存到`dc_workspace/input/<--name>.f`
3. 生成dc运行脚本和sdc脚本（若没有标记`-s`则使用原有的脚本），保存到`dc_workspace/script`路径下
4. （若不标记`-m`）生成makefile文件，若有makefile文件，则将其命名为`makefile_old`，再生成makefile，makefile的运行目标为`dc`
5. （若标记`-r`）使用makefile运行DC过程，DC的输出保存在`dc_workspace/report`路径下，报告保存在`dc_workspace/report`路径下。

下表表明指定了不同命令脚本的运行情况：

| `-s`/`--script` | `-r`/`--run` | 更新脚本 | 更新文件 | 运行 |
| --------------- | ------------ | -------- | -------- | ---- |
| yes             | yes          | yes      | yes      | yes  |
| yes             | no           | yes      | yes      | no   |
| no              | yes          | no       | yes      | yes  |
| no              | no           | no       | yes      | no   |