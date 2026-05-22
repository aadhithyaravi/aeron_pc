"""
Launch file for PC-side ROS 2 subscriber and processing nodes.
Launches subscriber_node and processing_node from pc_core package.
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition


def generate_launch_description():
    """Generate launch description for pc_core nodes."""

    # Launch arguments
    debug_arg = DeclareLaunchArgument(
        'debug',
        default_value='false',
        description='Enable debug logging'
    )

    config_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value='',
        description='Path to parameters file (optional)'
    )

    # Subscriber node
    subscriber_node = Node(
        package='pc_core',
        executable='subscriber_node',
        name='subscriber_node',
        output='screen',
        parameters=[{
            'debug': LaunchConfiguration('debug')
        }],
        remappings=[
            ('/scan', '/scan'),
            ('/cmd_vel', '/cmd_vel'),
        ]
    )

    # Processing node
    processing_node = Node(
        package='pc_core',
        executable='processing_node',
        name='processing_node',
        output='screen',
        parameters=[{
            'debug': LaunchConfiguration('debug'),
            'buffer_size': 10,
            'publish_processed': False
        }],
        remappings=[
            ('/scan', '/scan'),
        ]
    )

    return LaunchDescription([
        debug_arg,
        config_file_arg,
        subscriber_node,
        processing_node,
    ])