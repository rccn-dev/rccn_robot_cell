""" Static transform publisher acquired via MoveIt 2 hand-eye calibration """
""" EYE-IN-HAND: east_tool0 -> revo_rgb_optical_frame """
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    nodes = [
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            output="log",
            arguments=[
                "--frame-id",
                "east_tool0",
                "--child-frame-id",
                "revo_rgb_optical_frame",
                "--x",
                "-0.214413",
                "--y",
                "-0.242772",
                "--z",
                "0.33035",
                "--qx",
                "0.508056",
                "--qy",
                "0.510107",
                "--qz",
                "-0.481358",
                "--qw",
                "0.499965",
                # "--roll",
                # "1.60747",
                # "--pitch",
                # "0.0209593",
                # "--yaw",
                # "-1.55462",
            ],
        ),
    ]
    return LaunchDescription(nodes)
