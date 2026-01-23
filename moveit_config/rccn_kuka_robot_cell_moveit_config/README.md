# Raccoon KUKA Robot Cell MoveIt Config

This package contains the **MoveIt 2 Jazzy** configuration for the Raccoon KUKA Robot Cell
The cell consists of two **KUKA KR300 R2500 Ultra** robots mounted on independent linear rails.

##  System Overview

* **ROS Distro:** ROS 2 Jazzy
* **Solver:** KDL (Default) 
* **Hardware Interface:** `ros2_control` with hybrid support for Mock (Simulation) and KUKA RSI (Planned).

### Planning Groups
| Group Name | DOF | Description | Solver |
| :--- | :--- | :--- | :--- |
| `east` | 6 | East robot manipulator only (Rail locked) | KDL |
| `east_on_rail` | 7 | East robot manipulator + Rail (Redundant) | KDL |
| `west` | 6 | West robot manipulator only (Rail locked) | KDL |
| `west_on_rail` | 7 | West robot manipulator + Rail (Redundant) | KDL |
| `dual` | 14 | Both robots + Both rails (Coordinated) | None (Subgroups) |

---