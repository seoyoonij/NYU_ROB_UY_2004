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

    def __init__(self):
        super().__init__("posture_stabilizer")

        self.ik = IKSolver()

        # Definining home positions (x, y, z) in meters
        self.feet_home = np.array([
        [ 0.06, -0.09, -0.14],  # FR
        [ 0.06,  0.09, -0.14],  # FL
        [-0.11, -0.09, -0.14],  # BR
        [-0.11,  0.09, -0.14],  # BL
         ])

        # Subscriber that listens to Imu messages on '/imu/data'
        self.imu_sub = self.create_subscription(
            Imu, 
            '/imu/data', 
            self.imu_callback, 
            10)
        
        # Publisher that sends angles to '/joint_commands'
        self.joint_command_pub = self.create_publisher(
            Float64MultiArray, 
            '/joint_commands', 
            10)

        self.get_logger().info('Posture Stabilizer Node has started!')
    
    def imu_callback(self, msg):
        # unpacking imu info (packaged as quaternion so turning to euler)
        q = msg.orientation
        rot = Rotation.from_quat([q.x, q.y, q.z, q.w])
        roll, pitch, yaw = rot.as_euler('xyz')

        # we want to counter rotate so
        theta = -pitch
        phi = -roll

        #pitch 
        R_y = np.array([
            [np.cos(theta),  0, np.sin(theta)],
            [0,              1, 0            ],
            [-np.sin(theta), 0, np.cos(theta)]
        ])

        #roll
        R_x = np.array([
            [1, 0,           0           ],
            [0, np.cos(phi), -np.sin(phi)],
            [0, np.sin(phi),  np.cos(phi)]
        ])

        #total
        R_total = R_y @ R_x

        # calculate new positions for all 4 feet
        targets = []
        for i in range(4):
            new_target = R_total @ self.feet_home[i]
            targets.append(new_target)

        # finds all corresponding joint angles
        joint_angles = self.ik.solve_ik_all_legs(targets)

        #publishes to robot
        cmd = Float64MultiArray()
        cmd.data = joint_angles.tolist()
        self.joint_command_pub.publish(cmd)
        



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


