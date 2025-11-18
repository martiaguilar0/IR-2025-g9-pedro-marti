#!/usr/bin/env python3
import random
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class LidarPublisherNode(Node):
    def __init__(self):
        super().__init__('lidar_publisher')
        self.number_publisher_L_ = self.create_publisher(Int64, "left_sensor", 10)
        self.number_publisher_R_ = self.create_publisher(Int64, "right_sensor", 10)
        self.number_timer_ = self.create_timer(1.0, self.publish_number)
        self.get_logger().info("Lidar publisher has been started.")

    def publish_number(self):
        self.right_value_=random.randrange(2,200)
        self.left_value_=random.randrange(2,200)
        msg_R = Int64()
        msg_L = Int64()
        msg_R.data = self.right_value_
        msg_L.data = self.left_value_
        self.number_publisher_R_.publish(msg_R)
        self.number_publisher_L_.publish(msg_L)

def main(args=None):
    rclpy.init(args=args)
    node = LidarPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()