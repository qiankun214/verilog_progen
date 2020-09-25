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