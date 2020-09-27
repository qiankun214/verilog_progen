# 说明

本项目用于直接通过可读的markdown文本生成rtl设计中需要使用的verilog模板和SystemVerilog的TB的模板，后续将添加其他功能。使用方法为按要求编写markdown文本，随后使用如下命令：

```shell
python3 <root>/script/progen/progen -m <markdown path> -d <rtl root> -t <tb root>
```

同时可以使用如下指令查询：

```
python3 <root>/script/progen/progen -h
```

- 自动化例化连接功能正在开发过程中

# json格式定义

json定义模块信息需要包括以下方面：
- 基本信息：模块名称
- parameter：模块外部可变参数信息，包括名称
- port：模块端口信息，包括端口类型、参数和名称（描述以注释的方式存在）
- link:子模块调用相关信息

其中，基本信息以文件名的方式提供，其他包括在md文件中

## 对应markdown格式规定

```markdown
# parameter

| 名称   | 说明                               | 默认值 |
| ------ | ---------------------------------- | ------ |
| DWIDTH | 单个数据位宽                       | 16     |
| AWIDTH | 主cache地址总线位宽                | 16     |
| OWIDTH | 临时cache地址总线位宽              | 8      |
| PWIDTH | PE阵列地址位宽（$log_2(PE\_ROW)$） | 4      |
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
| outside_memory_din  | input  | DWIDTH * PE_ROW  | 外部存储器写数据         |
| outside_memory_dout | output | DWIDTH * PE_ROW  | 外部存储器读数据         |

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

对应的markdown包括三块内容，分别是parameter信息、port信息和link信息。parameter信息和port信息均以markdown表格语法存储，表头信息而言：
- parameter：表头顺序为名称、说明和默认值，顺序不可改变
- port：表头顺序为名称、类型、位宽和说明

需要注意的是，名称和说明栏类型为string，位宽为数字表达式，可以使用parameter部分定义的参数。link部分使用专门格式编写，用于描述子模块和连接关系，若没有调用子模块可以不写。
调用子模块包括部分包括两个部分：

- 实例化表格：为一个markdown表格，分为两列，第一列为实例化名，第二列为模块名
- 连接关系：使用`- inst1.port1 <> inst2.port2`表示实例化名为inst1的模块的端口port1和实例化名为inst2的模块的端口port2连接。需要注意的是，若某个端口没指定连接关系且与顶层端口名称相同，则会自动连接

## json格式

json格式如下所示
```json
{
    "name":"test",
    "parameter":{
        "DWIDTH":["16","单个数据位宽"],
        "AWIDTH":["16","主cache地址总线位宽"],
        "..."
    },
    "port":{
        "clk":["input","1","系统时钟"],
        "..."
    },
    "link":{...}
}
```