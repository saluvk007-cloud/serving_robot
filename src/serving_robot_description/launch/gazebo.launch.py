from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_path = get_package_share_directory("serving_robot_description")

    # Path to your custom world
    world = os.path.join(
        pkg_path,
        "worlds",
        "restaurant.world"
    )

    # Launch Gazebo with custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("gazebo_ros"),
                "launch",
                "gazebo.launch.py"
            )
        ),
        launch_arguments={
            "world": world
        }.items()
    )

    # URDF
    urdf_file = os.path.join(
        pkg_path,
        "urdf",
        "serving_robot.urdf"
    )

    # ros2_control config
    config_path = os.path.join(
        pkg_path,
        "config",
        "ros2_controllers.yaml"
    )

    with open(urdf_file, "r") as file:
        robot_description = file.read()

    robot_description = robot_description.replace(
        "ROS2_CONTROLLERS_YAML_PATH",
        config_path
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description
            }
        ],
        output="screen"
    )

    # Spawn Robot
    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity",
            "serving_robot",
            "-topic",
            "robot_description"
        ],
        output="screen"
    )

    # Joint State Broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen"
    )

    # Diff Drive Controller
    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
        output="screen"
    )

    # Cmd Vel Relay (bridges Nav2's /cmd_vel output to diff_drive_controller's actual topic)
    cmd_vel_relay = Node(
        package="topic_tools",
        executable="relay",
        arguments=["/cmd_vel", "/diff_drive_controller/cmd_vel_unstamped"],
        output="screen"
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        joint_state_broadcaster_spawner,
        diff_drive_controller_spawner,
        cmd_vel_relay
    ])