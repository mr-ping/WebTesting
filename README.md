#WebTesting

##属性：
自动测试脚本

##功能：
WEB负载测试  
WEB基准测试（下版添加）

##相较pylot、siege等：

1. 自动持续打压
2. 测试日志可视分类统计

##使用：
###运行环境：
Linux, Unix, BSD

###依赖：
siege  
matplotlib

###运行：

    ./main.py -u http://webhost:port/path -t log_file

测试从10个并发用户开始，直到100个并发用户结束，每阶段并发数增加20。（10, 30, 50, 70, 90）:

    ./main.py -f urls_waiting_to_test.txt -b 10 -m 100 -s 20

更多:

    ./main.py --help

##结果：
![](https://cloud.githubusercontent.com/assets/2333186/6519475/79b8ea6c-c3ef-11e4-95c4-abfa78eb01e0.png)
