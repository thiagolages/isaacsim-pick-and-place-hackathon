#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from mobile_robot_interfaces.action import MoveTo
from nav2_simple_commander.robot_navigator import BasicNavigator
import tf_transformations
from geometry_msgs.msg import PoseStamped

class MoveToNode(Node):
    def __init__(self):
        super().__init__("MoveTo_server")
        self.move_to_server = ActionServer(
            self, 
            MoveTo, 
            "move_to",
            execute_callback=self.execute_callback)
        self.nav = BasicNavigator()
        self.get_logger().info("Move to Server has been started")

    def transform_pose_struct(self, x, y, yaw):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, float(yaw))
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.nav.get_clock().now().to_msg()
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = float(q_x)
        pose.pose.orientation.y = float(q_y)
        pose.pose.orientation.z = float(q_z)
        pose.pose.orientation.w = float(q_w)
        return pose





    def execute_callback(self, goal_handle: ServerGoalHandle):
        x_target = float(goal_handle.request.x_position)
        y_target = float(goal_handle.request.y_position)
        yaw_target = float(goal_handle.request.yaw_angle)


        self.get_logger().info("Executing the goal")
        self.nav.goToPose(self.transform_pose_struct(x_target,y_target,yaw_target))
        while not self.nav.isTaskComplete():
            feedback = self.nav.getFeedback()
        goal_handle.succeed()
        result = MoveTo.Result()
        result.success = True
        result.message = "Goal reached"
        return result



def main(args=None):
    rclpy.init(args=args)
    node = MoveToNode() 
    rclpy.spin(node)
    rclpy.shutdown()





















if __name__=="__main__":
    main()
