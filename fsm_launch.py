from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Declare argument to disable GUI
    declare_gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='false',
        description='Set to "true" to enable Gazebo GUI'
    )

    # Launch Gazebo with GUI disabled
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={
            'world': os.path.join(
                get_package_share_directory('robot_control'),
                'worlds',
                'custom_world.world'
            ),
            'gui': LaunchConfiguration('gui')
        }.items()
    )


    # Spawn robot model
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_my_robot',
        arguments=[
            '-entity', 'my_robot',
            '-file', os.path.join(
                get_package_share_directory('robot_control'),
                'urdf',
                'my_robot.urdf'
            ),
            '-x', '0', '-y', '0', '-z', '0.1'  # optional pose
        ],
        output='screen'
    )

    # FSM node
    fsm_node = Node(
        package='robot_control',
        executable='robot_fsm',
        name='fsm',
        output='screen'
    )

    return LaunchDescription([
        declare_gui_arg,
        gazebo,
        spawn_entity,
        fsm_node
    ])

