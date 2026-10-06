# ROS2 系统状态监视器
ROS2课程作业，实现自定义消息通信 + Qt图形化订阅界面

## 项目结构
- status_interfaces：自定义消息功能包，定义SystemStatus.msg，用于传输系统状态数据
- status_publisher：发布节点 + Qt图形订阅节点

## 运行环境
- ROS2 Humble
- Python3
- PyQt5

## 编译指令
```bash
colcon build --packages-select status_interfaces status_publisher
source install/setup.bash

## 运行步骤
终端1（发布端，发送CPU、内存数据）
```bash
ros2 run status_publisher sys_status_pub

终端2（qt订阅图形界面）
ros2 run status_publisher sys_status_sub_qt

## 项目功能
发布节点定时采集电脑CPU使用率、内存占用，使用自定义话题向外发布；
Qt订阅节点接收话题数据，在图形窗口实时展示系统状态。
