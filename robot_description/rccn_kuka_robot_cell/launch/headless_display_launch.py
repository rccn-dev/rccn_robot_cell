#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    model_arg = DeclareLaunchArgument(
        "model",
        default_value=PathJoinSubstitution(
            [FindPackageShare("rccn_kuka_robot_cell"), "urdf", "rccn_kuka_robot_cell.urdf"]
        ),
        description="Absolute path to URDF/Xacro file to load",
    )

    robot_description = Command(["xacro ", LaunchConfiguration("model")])

    # Publishes joint states (default 0) so TF tree is complete
    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )

    # Publishes TFs and the robot_description topic
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        output="screen"
    )

    return LaunchDescription(
        [
            model_arg,
            joint_state_publisher_node,
            robot_state_publisher_node,
        ]
    )
