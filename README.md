# Raccoon Robot Cell

The ros packages for the robot cell at Raccoon.

# Update the URDF
The URDF files of KUKA KR300 R2500 ultra is still actively being updated. When there is a change in the URDF, the following command should be run to update the URDF file.

```sh
rosrun xacro xacro -o rccn_kuka_robot_cell.urdf rccn_kuka_robot_cell.xacro
rosrun xacro xacro -o rccn_west_robot.urdf rccn_west_robot.xacro
rosrun xacro xacro -o rccn_east_robot.urdf rccn_east_robot.xacro
```

as well as the moveit configuration files.

```sh
roslaunch moveit_setup_assistant setup_assistant.launch
```