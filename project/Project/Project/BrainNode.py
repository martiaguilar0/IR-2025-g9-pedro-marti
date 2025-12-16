#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, error):
        P = self.Kp * error
        self.integral += error
        I = self.Ki * self.integral
        D = self.Kd * (error - self.prev_error)
        self.prev_error = error
        return P + I + D

class BrainNode(Node):
    def __init__(self):
        super().__init__('BrainNode')
        
        self.left = 0
        self.right = 0
        self.front = 0
        self.ranges = []

        # PID
        self.pid = PID(Kp=0.3, Ki=0.0, Kd=0.12)
        #FUNCIONA CON KP=0.5 KD=0.2
        
        # Suscriptor LIDAR
        self.subscriber_ = self.create_subscription(LaserScan,'/scan', self.scan_callback, 10)

        # Publisher de velocidad
        self.cmd_vel_publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Timer
        self.timer = self.create_timer(0.1, self.comparation)

        self.get_logger().info("BrainNode has been started")

    def scan_callback(self, msg):
        self.ranges = msg.ranges
        n = len(msg.ranges)

        # Índices correctos según angle_min y angle_increment
        front_index = int((0 - msg.angle_min) / msg.angle_increment)
        right_index = int((-math.pi/2 - msg.angle_min) / msg.angle_increment)
        left_index  = int((math.pi/2 - msg.angle_min) / msg.angle_increment)

        # Sector ±10 lecturas
        sector_width = 10

        # Función para calcular media ignorando None o 0
        def sector_mean(ranges, center, width):
            sector = []
            for i in range(center - width, center + width):
                val = ranges[i % n]
                if val is not None and val > 0:
                    sector.append(val)
            if not sector:
                return msg.range_max
            return sum(sector)/len(sector)

        # Función para front: mínimo sector para evitar choque
        def sector_min(ranges, center, width):
            sector = []
            for i in range(center - width, center + width):
                val = ranges[i % n]
                if val is not None and val > 0:
                    sector.append(val)
            if not sector:
                return msg.range_max
            return min(sector)

        # Calcular distancias
        self.front = sector_min(self.ranges, front_index, sector_width)
        self.right = sector_mean(self.ranges, right_index, sector_width)
        self.left  = sector_mean(self.ranges, left_index, sector_width)

    def move_robot(self, linear, angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_vel_publisher_.publish(msg)

    def comparation(self):
        self.get_logger().info(f"R:{self.right:.2f} L:{self.left:.2f} F:{self.front:.2f}")

        # Control PID lateral
        error = self.left - self.right
        correction = self.pid.compute(error)

        # Mover el robot
        if self.front < 1.3:
            if self.right>self.left:
                self.move_robot(0.1, -1.0)
            else:
                self.move_robot(0.1, 1.0)
               
        else:
            self.move_robot(0.6, correction)

def main(args=None):
    rclpy.init(args=args)
    node = BrainNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
