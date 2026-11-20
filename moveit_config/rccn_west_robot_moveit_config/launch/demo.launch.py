import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def load_file(package_name: str, relative_path: str) -> str:
    package_path = get_package_share_directory(package_name)
    file_path = os.path.join(package_path, relative_path)
    with open(file_path, "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def generate_launch_description() -> LaunchDescription:
    declared_arguments = [
        DeclareLaunchArgument("pipeline", default_value="ompl"),
        DeclareLaunchArgument("use_gui", default_value="false"),
        DeclareLaunchArgument("use_rviz", default_value="true"),
        DeclareLaunchArgument("allow_trajectory_execution", default_value="true"),
        DeclareLaunchArgument(
            "moveit_controller_manager",
            default_value="moveit_fake_controller_manager/MoveItFakeControllerManager",
        ),
        DeclareLaunchArgument("fake_execution_type", default_value="interpolate"),
    ]

    robot_description = {
        "robot_description": load_file(
            "rccn_kuka_robot_cell", "urdf/rccn_west_robot.urdf"
        )
    }

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="virtual_joint_broadcaster_0",
        arguments=["0", "0", "0", "0", "0", "0", "map", "kuka_robot_cell_world"],
        output="screen",
    )

    joint_state_publisher = Node(
        name="joint_state_publisher",
        package="joint_state_publisher",
        executable="joint_state_publisher",
        parameters=[
            {"source_list": ["move_group/fake_controller_joint_states"]}
        ],
        condition=UnlessCondition(LaunchConfiguration("use_gui")),
    )

    joint_state_publisher_gui = Node(
        name="joint_state_publisher_gui",
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        parameters=[
            {"source_list": ["move_group/fake_controller_joint_states"]}
        ],
        condition=IfCondition(LaunchConfiguration("use_gui")),
    )

    robot_state_publisher = Node(
        name="robot_state_publisher",
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    move_group_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("rccn_west_robot_moveit_config"),
                "launch",
                "move_group.launch.py",
            )
        ),
        launch_arguments={
            "pipeline": LaunchConfiguration("pipeline"),
            "allow_trajectory_execution": LaunchConfiguration(
                "allow_trajectory_execution"
            ),
            "moveit_controller_manager": LaunchConfiguration(
                "moveit_controller_manager"
            ),
            "fake_execution_type": LaunchConfiguration("fake_execution_type"),
        }.items(),
    )

    moveit_rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("rccn_west_robot_moveit_config"),
                "launch",
                "moveit_rviz.launch.py",
            )
        ),
        condition=IfCondition(LaunchConfiguration("use_rviz")),
    )

    return LaunchDescription(
        declared_arguments
        + [
            static_tf,
            joint_state_publisher,
            joint_state_publisher_gui,
            robot_state_publisher,
            move_group_launch,
            moveit_rviz_launch,
        ]
    )
