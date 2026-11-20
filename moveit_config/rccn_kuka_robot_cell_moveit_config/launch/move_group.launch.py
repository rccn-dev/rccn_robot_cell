from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch


def generate_launch_description():
    robot_ip = LaunchConfiguration("robot_ip")
    robot_port = LaunchConfiguration("robot_port")
    use_mock = LaunchConfiguration("use_mock")

    moveit_config = (
        MoveItConfigsBuilder(
            "rccn_kuka_robot_cell", package_name="rccn_kuka_robot_cell_moveit_config"
        )
        .robot_description(
            file_path="config/rccn_kuka_robot_cell.urdf.xacro",
            mappings={
                "robot_ip": robot_ip,
                "robot_port": robot_port,
                "use_mock": use_mock,
            },
        )
        .to_moveit_configs()
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("robot_ip", default_value="127.0.0.1"),
            DeclareLaunchArgument("robot_port", default_value="7000"),
            DeclareLaunchArgument("use_mock", default_value="true"),
            generate_move_group_launch(moveit_config),
        ]
    )
