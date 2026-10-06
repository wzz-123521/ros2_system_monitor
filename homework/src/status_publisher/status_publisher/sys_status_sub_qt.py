import sys
import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal

class RosSubThread(QThread):
    data_signal = pyqtSignal(SystemStatus)

    def __init__(self):
        super().__init__()
        self.node = None
        self._running = True

    def run(self):
        rclpy.init()
        self.node = Node("sys_status_sub")
        self.node.create_subscription(
            SystemStatus,
            "/sys_status",
            self.callback,
            10
        )
        while self._running:
            rclpy.spin_once(self.node, timeout_sec=0.05)
        self.node.destroy_node()
        rclpy.shutdown()

    def callback(self, msg):
        self.data_signal.emit(msg)

    def stop(self):
        self._running = False

class StatusWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("系统状态监视器 ROS2")
        self.resize(450,300)
        self.label = QLabel("等待数据...")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)  # ✅这里改成layout！

        self.ros_thread = RosSubThread()
        self.ros_thread.data_signal.connect(self.update_ui)
        self.ros_thread.start()

    def update_ui(self, msg):
        text = f"""时间戳: {msg.stamp.sec}.{msg.stamp.nanosec}
主机名: {msg.hostname}
CPU使用率: {msg.cpu_percent:.2f} %
内存使用率: {msg.mem_percent:.2f} %
内存总大小: {msg.mem_total:.2f} GB
剩余内存: {msg.mem_free:.2f} GB
网络接收: {msg.net_recv/1024/1024:.2f} MB
网络发送: {msg.net_sent/1024/1024:.2f} MB
"""
        self.label.setText(text)

    def closeEvent(self, event):
        self.ros_thread.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    win = StatusWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()