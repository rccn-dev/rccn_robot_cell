# Raccoon Robot Cell

The ros packages for the robot cell at Raccoon.

## Getting started (recommended)

This workspace depends on at least one ROS package that is not distributed as a ROS apt package (e.g. `kuka_kr300_support`). The common ROS 2 practice is to bring those repositories into the same colcon workspace using a vcstool `.repos` file.

### Devcontainer

Open this repo in the Humble/Jazzy devcontainer. On first create, the container will:

- Install `colcon`, `vcstool`, and `rosdep`
- Import source-only dependencies from `rccn_robot_cell.repos`
- Run `rosdep install ...` and `colcon build`

To rerun manually:

```sh
./scripts/bootstrap_workspace.sh
```

### Local (non-devcontainer)

```sh
mkdir -p src
vcs import src < rccn_robot_cell.repos
rosdep install --from-paths robot_description src -y --ignore-src
colcon build --symlink-install --base-paths robot_description src
source install/setup.bash
```

## RViz preview

After building and sourcing the overlay:

```sh
source install/setup.bash
ros2 launch rccn_kuka_robot_cell display.launch.py
```

# Update the URDF
The URDF files of KUKA KR300 R2500 ultra is still actively being updated. When there is a change in the URDF, the following command should be run to update the URDF file.

```sh
./scripts/update_urdf.sh
```