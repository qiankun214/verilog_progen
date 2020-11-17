# parameter

| 名称   | 说明                               | 默认值 |
| ------ | ---------------------------------- | ------ |
| DWIDTH | 单个数据位宽                       | 16     |

# port

| 名称       | 类型   | 位宽   | 说明                 |
| ---------- | ------ | ------ | -------------------- |
| clk        | input  | 1      | 系统时钟             |
| rst_n      | input  | 1      | 系统复位信号，低有效 |
| dout_valid | output | 1      | 输出有效端口         |
| dout_data  | output | DWIDTH | 输出数据端口         |