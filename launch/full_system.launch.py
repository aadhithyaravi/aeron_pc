from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction


def generate_launch_description():

    # 1️⃣ Start Gazebo
    gazebo = ExecuteProcess(
        cmd=['ros2', 'launch', 'pc_core', 'gazebo.launch.py'],
        output='screen'
    )

    # 2️⃣ Start clock bridge
    clock_bridge = TimerAction(
        period=5.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
                    '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
                ],
                output='screen'
            )
        ]
    )

    # 3️⃣ Load controllers
    # 3️⃣ Load controllers (CONFIGURE them)
    load_controllers = TimerAction(
        period=8.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
                output='screen'
            ),
            ExecuteProcess(
                cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'diff_drive_controller'],
                output='screen'
            ),
        ]
)

    # 4️⃣ Activate controllers
    activate_controllers = TimerAction(
        period=10.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'control', 'set_controller_state', 'joint_state_broadcaster', 'inactive']
            ),
            ExecuteProcess(
                cmd=['ros2', 'control', 'set_controller_state', 'diff_drive_controller', 'inactive']
            ),
            ExecuteProcess(
                cmd=['ros2', 'control', 'set_controller_state', 'joint_state_broadcaster', 'active']
            ),
            ExecuteProcess(
                cmd=['ros2', 'control', 'set_controller_state', 'diff_drive_controller', 'active']
            ),
        ]
    )

    # 5️⃣ Start cmd_vel bridge
    cmd_vel_bridge = TimerAction(
        period=13.0,
        actions=[
            ExecuteProcess(
                cmd=['ros2', 'run', 'pc_core', 'cmd_vel_bridge'],
                output='screen'
            )
        ]
    )

    # 🔥 6️⃣ TF (LiDAR frame)
    tf_node = TimerAction(
        period=14.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'run', 'tf2_ros', 'static_transform_publisher',
                    '0', '0', '0', '0', '0', '0',
                    'base_link', 'laser_frame'
                ],
                output='screen'
            )
        ]
    )

    # 🔥 7️⃣ RViz
    rviz = TimerAction(
        period=15.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'run', 'rviz2', 'rviz2'
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        clock_bridge,
        load_controllers,
        activate_controllers,
        cmd_vel_bridge,
        tf_node,
        rviz
    ])