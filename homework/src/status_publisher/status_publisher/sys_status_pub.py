import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus
import psutil
import socket

class SysStatusPub(Node):
    def __init__(self):
        super().__init__('sys_status_pub')
        self.pub = self.create_publisher(SystemStatus, 'sys_status', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.hostname = socket.gethostname()

        msg.cpu_percent = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        msg.mem_percent = mem.percent
        msg.mem_total = mem.total / 1024**3
        msg.mem_free = mem.available / 1024**3

        net = psutil.net_io_counters()
        msg.net_recv = net.bytes_recv
        msg.net_sent = net.bytes_sent

        self.pub.publish(msg)
        self.get_logger().info(f"Publish: cpu:{msg.cpu_percent}% mem:{msg.mem_percent}%")

def main():
    rclpy.init()
    node = SysStatusPub()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
