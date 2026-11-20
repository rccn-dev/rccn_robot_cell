cmake_minimum_required(VERSION 3.8)
project(rccn_west_robot_moveit_config)

find_package(ament_cmake REQUIRED)

ament_package()

install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
  PATTERN "setup_assistant.launch" EXCLUDE
)
