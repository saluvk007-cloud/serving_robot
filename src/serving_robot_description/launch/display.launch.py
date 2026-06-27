from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_path = get_package_share_directory("serving_robot_description")
    urdf_file = os.path.join(pkg_path, "urdf", "serving_robot.urdf")

    with open(urdf_file, "r") as file:
        robot_description = file.read()

    return LaunchDescription([

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen"
        ),

        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            output="screen"
        )

    ])