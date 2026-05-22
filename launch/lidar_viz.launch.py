from launch import LaunchDescription
from launch_ros.actions import Node

import os


def generate_launch_description():

    rviz_config = os.path.join(
        os.getenv('HOME'),
        'ros2_ws',
        'src',
        'pc_core',
        'rviz',
        'lidar.rviz'
    )

    return LaunchDescription([

        # Static TF (map → laser_frame)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'laser_frame']
        ),

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        ),
    ])
