#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class DecisionSubscriberNode(Node):
    def __init__(self):
        super().__init__('decision_subscriber')

        # Inicialización de valores
        self.left_number_ = 0
        self.right_number_ = 0

        # Suscriptores
        self.Left_subscriber_ = self.create_subscription(
            Int64, "left_sensor", self.callback_left, 10
        )
        self.Right_subscriber_ = self.create_subscription(
            Int64, "right_sensor", self.callback_right, 10
        )

        # Timer: ejecuta comparacion cada 1s
        self.timer = self.create_timer(1.0, self.comparation)

        self.get_logger().info("DecisionSubscriber has been started")
    
    def callback_left(self, msg_L: Int64):
        self.left_number_ = msg_L.data
    
    def callback_right(self, msg_R: Int64):
        self.right_number_ = msg_R.data 
        
    def comparation(self):
        if self.right_number_ < 40 and self.left_number_ < 40:
            self.get_logger().info("R:"+str(self.right_number_)+" L:"+str(self.left_number_)+" Action: stop")
        elif self.left_number_ < 40:
            self.get_logger().info("R:"+str(self.right_number_)+" L:"+str(self.left_number_)+" Action: turn right")
        elif self.right_number_ < 40:
            self.get_logger().info("R:"+str(self.right_number_)+" L:"+str(self.left_number_)+" Action: turn left")
        else:
            self.get_logger().info("R:"+str(self.right_number_)+" L:"+str(self.left_number_)+" Action: forward")


def main(args=None):
    rclpy.init(args=args)
    node = DecisionSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
