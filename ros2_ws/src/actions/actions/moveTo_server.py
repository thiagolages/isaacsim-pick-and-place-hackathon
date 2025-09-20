#!/usr/bin/env python 3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from mobile_robot_interfaces.action import MoveTo

class MoveToNode(Node):
    def __init__(self):
        super().__init__("MoveTo_server")
        self.move_to_server = ActionServer(
            self, 
            MoveTo, 
            "move_to",
            execute_callback=self.execute_callback)
        self.get_logger().info("Move to Server has been started")


    def execute_callback(self, goal_handle: ServerGoalHandle):
        x_target = goal_handle.request.x_position
        y_target = goal_handle.request.y_position
        yaw_target = goal_handle.request.yaw_angle

        self.get_logger().info("Executing the goal")
        pass
        goal_handle.succeed()
        result = MoveTo.Result.success = True



def main(args=None):
    rclpy.init(args=args)
    node = MoveToNode() 
    rclpy.spin(node)
    rclpy.shutdown()





















if __name__=="__main__":
    main()
