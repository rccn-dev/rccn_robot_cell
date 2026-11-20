cmake_minimum_required(VERSION 3.10)
project(rccn_kuka_robot_cell)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
	launch
	meshes
	rviz
	urdf
	DESTINATION share/${PROJECT_NAME}
)

ament_package()
