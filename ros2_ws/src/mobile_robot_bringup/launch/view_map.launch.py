import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command

def generate_launch_description():
    description_pkg = 'mobile_robot_description'
    bringup_pkg = 'mobile_robot_bringup'
    map_file = "/home/victor/projects/isaacsim-pick-and-place-hackathon/ros2_ws/src/mobile_robot_bringup/worlds/world_map.yaml"
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    bringup_launch_file = os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
    rviz_config_file = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')



    urdf_path = os.path.join(get_package_share_directory(description_pkg), 'URDF', 'MineMapper.urdf.xacro')
    gazebo_config_path = os.path.join(get_package_share_directory(bringup_pkg), 'config', 'gazebo_bridge.yaml')
    world_path = os.path.join(get_package_share_directory(bringup_pkg), 'worlds', 'test_world.world')
    map_yaml_path = os.path.join(get_package_share_directory(bringup_pkg), 'worlds', 'world_map.yaml')


    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation time'),



        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': Command(['xacro ', urdf_path])}]
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
            ),
            launch_arguments={'gz_args': f'{world_path} -r'}.items()
        ),

        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description', '-x', '0', '-y', '0', '-z', '0.3'],
            output='screen'
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='ros_gz_bridge',
            parameters=[{'config_file': gazebo_config_path}],
            output='screen'
        ),


        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(bringup_launch_file),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true'
            }.items()
        ),

        Node(
            package='initialconfigs',
            executable='set_initial_pose',
            name='set_initial_pose',
            output='screen'
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='map_to_odom',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        ),


        Node(
            package='actions',
            executable='move_to_server',
            name='move_to_server',
            output='screen'
        )

    ])
