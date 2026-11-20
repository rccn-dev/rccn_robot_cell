import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    default_rviz_config = os.path.join(
        get_package_share_directory("rccn_west_robot_moveit_config"),
        "launch",
        "moveit.rviz",
    )

    declared_arguments = [
        DeclareLaunchArgument("rviz_config", default_value=default_rviz_config),
    ]

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rviz_config")],
        parameters=[{"use_sim_time": False}],
    )

    return LaunchDescription(declared_arguments + [rviz_node])
