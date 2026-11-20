#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
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

    gui_arg = DeclareLaunchArgument(
        "gui",
        default_value="true",
        description="Flag to enable joint_state_publisher_gui",
    )

    rviz_arg = DeclareLaunchArgument(
        "rvizconfig",
        default_value=PathJoinSubstitution(
            [FindPackageShare("rccn_kuka_robot_cell"), "rviz", "urdf.rviz"]
        ),
        description="RViz config file",
    )

    robot_description = Command(["xacro", LaunchConfiguration("model")])

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher",
        condition=IfCondition(LaunchConfiguration("gui")),
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        condition=UnlessCondition(LaunchConfiguration("gui")),
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", LaunchConfiguration("rvizconfig")],
        output="screen",
    )

    return LaunchDescription(
        [
            model_arg,
            gui_arg,
            rviz_arg,
            joint_state_publisher_gui_node,
            joint_state_publisher_node,
            robot_state_publisher_node,
            rviz_node,
        ]
    )
