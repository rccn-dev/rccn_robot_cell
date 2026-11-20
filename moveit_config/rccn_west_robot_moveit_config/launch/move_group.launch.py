import os
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def load_file(package_name: str, relative_path: str) -> str:
    package_path = get_package_share_directory(package_name)
    file_path = os.path.join(package_path, relative_path)
    with open(file_path, "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def load_yaml(package_name: str, relative_path: str) -> dict:
    package_path = get_package_share_directory(package_name)
    file_path = os.path.join(package_path, relative_path)
    with open(file_path, "r", encoding="utf-8") as file_handle:
        return yaml.safe_load(file_handle) or {}


def generate_launch_description() -> LaunchDescription:
    declared_arguments = [
        DeclareLaunchArgument("pipeline", default_value="ompl"),
        DeclareLaunchArgument("allow_trajectory_execution", default_value="true"),
        DeclareLaunchArgument(
            "moveit_controller_manager",
            default_value="moveit_fake_controller_manager/MoveItFakeControllerManager",
        ),
        DeclareLaunchArgument("fake_execution_type", default_value="interpolate"),
        DeclareLaunchArgument("moveit_manage_controllers", default_value="true"),
        DeclareLaunchArgument("capabilities", default_value=""),
        DeclareLaunchArgument("disable_capabilities", default_value=""),
        DeclareLaunchArgument("publish_monitored_planning_scene", default_value="true"),
    ]

    robot_description = {
        "robot_description": load_file(
            "rccn_kuka_robot_cell", "urdf/rccn_west_robot.urdf"
        )
    }

    robot_description_semantic = {
        "robot_description_semantic": load_file(
            "rccn_west_robot_moveit_config", "config/rccn_west_robot.srdf"
        )
    }

    robot_description_kinematics = {
        "robot_description_kinematics": load_yaml(
            "rccn_west_robot_moveit_config", "config/kinematics.yaml"
        )
    }

    robot_description_planning = load_yaml(
        "rccn_west_robot_moveit_config", "config/joint_limits.yaml"
    )
    robot_description_planning.update(
        load_yaml("rccn_west_robot_moveit_config", "config/cartesian_limits.yaml")
    )
    robot_description_planning = {"robot_description_planning": robot_description_planning}

    ompl_yaml = load_yaml(
        "rccn_west_robot_moveit_config", "config/ompl_planning.yaml"
    )
    ompl_planning_pipeline_config = {
        "ompl": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "request_adapters": "default_planner_request_adapters/AddTimeParameterization "
            "default_planner_request_adapters/ResolveConstraintFrames "
            "default_planner_request_adapters/FixWorkspaceBounds "
            "default_planner_request_adapters/FixStartStateBounds "
            "default_planner_request_adapters/FixStartStateCollision "
            "default_planner_request_adapters/FixStartStatePathConstraints",
            "start_state_max_bounds_error": 0.1,
            "jiggle_fraction": 0.05,
            **ompl_yaml,
        }
    }

    planning_pipelines_config = {
        "planning_pipelines": {
            "pipeline_names": ["ompl"],
            "default_planning_pipeline": LaunchConfiguration("pipeline"),
        }
    }

    trajectory_execution = {
        "moveit_manage_controllers": LaunchConfiguration("moveit_manage_controllers"),
        "trajectory_execution/allowed_execution_duration_scaling": 1.2,
        "trajectory_execution/allowed_goal_duration_margin": 0.5,
        "trajectory_execution/allowed_start_tolerance": 0.01,
    }

    moveit_controllers = load_yaml(
        "rccn_west_robot_moveit_config", "config/fake_controllers.yaml"
    )

    planning_scene_monitor_config = {
        "planning_scene_monitor/publish_planning_scene": LaunchConfiguration(
            "publish_monitored_planning_scene"
        ),
        "planning_scene_monitor/publish_geometry_updates": LaunchConfiguration(
            "publish_monitored_planning_scene"
        ),
        "planning_scene_monitor/publish_state_updates": LaunchConfiguration(
            "publish_monitored_planning_scene"
        ),
        "planning_scene_monitor/publish_transforms_updates": LaunchConfiguration(
            "publish_monitored_planning_scene"
        ),
    }

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            robot_description_kinematics,
            robot_description_planning,
            ompl_planning_pipeline_config,
            planning_pipelines_config,
            trajectory_execution,
            moveit_controllers,
            planning_scene_monitor_config,
            {
                "allow_trajectory_execution": LaunchConfiguration(
                    "allow_trajectory_execution"
                ),
                "capabilities": LaunchConfiguration("capabilities"),
                "disable_capabilities": LaunchConfiguration("disable_capabilities"),
                "moveit_controller_manager": LaunchConfiguration(
                    "moveit_controller_manager"
                ),
                "fake_execution_type": LaunchConfiguration("fake_execution_type"),
            },
        ],
    )

    return LaunchDescription(declared_arguments + [move_group_node])
