# Raccoon KUKA Robot Cell MoveIt Config

This package contains the **MoveIt 2 Jazzy** configuration for the Raccoon KUKA Robot Cell
The cell consists of two **KUKA KR300 R2500 Ultra** robots mounted on independent linear rails.

##  System Overview

* **ROS Distro:** ROS 2 Jazzy
* **Solver:** KDL (Default) 
* **Hardware Interface:** `ros2_control` with support for Mock (Simulation) and KUKA KUKAVARPROXY (east_on_rail only).

### Planning Groups
| Group Name | DOF | Description | Solver |
| :--- | :--- | :--- | :--- |
| `east` | 6 | East robot manipulator only (Rail locked) | KDL |
| `east_on_rail` | 7 | East robot manipulator + Rail (Redundant) | KDL |
| `west` | 6 | West robot manipulator only (Rail locked) | KDL |
| `west_on_rail` | 7 | West robot manipulator + Rail (Redundant) | KDL |
| `dual` | 14 | Both robots + Both rails (Coordinated) | None (Subgroups) |

---

## Read-only joint state mode (east_on_rail)
The MoveIt config can be started in a read-only mode that only publishes `/joint_states` from the physical East robot. Use these xacro args when launching:

- `use_mock:=false`
- `robot_ip:=<robot ip>`
- `robot_port:=<robot port>`

The ros2_control config is trimmed to `joint_state_broadcaster` only, so no trajectory controllers are spawned.