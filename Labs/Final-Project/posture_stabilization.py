#!/usr/bin/env python3
"""
Active Posture Stabilization for Pupper v3
Uses PID controller + IK solver to maintain level orientation
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from std_msgs.msg import Float64MultiArray
import numpy as np
from scipy.spatial.transform import Rotation
import time

from ik_solver import IKSolver
from pid import PIDController # Stage 1
from adrc import ADRController # Stage 2

np.set_printoptions(precision=3, suppress=True)


class PostureStabilizer(Node):
    """
    ROS2 Node for active posture stabilization using PID + IK
    """
    # TODO

def main(args=None):
    rclpy.init(args=args)
    
    node = PostureStabilizer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down posture stabilizer...')
    finally:
        # Send zero commands to stop robot
        zero_cmd = Float64MultiArray()
        zero_cmd.data = [0.0] * 12
        node.joint_command_pub.publish(zero_cmd)
        
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


