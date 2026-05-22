from setuptools import setup

package_name = 'pc_core'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        # ament index
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # 🔥 LAUNCH FILES
        ('share/' + package_name + '/launch', [
            'launch/pc.launch.py',
            'launch/gazebo.launch.py',
            'launch/full_system.launch.py',
            'launch/lidar_viz.launch.py',   # ✅ ADDED
        ]),

        # 🔥 RVIZ CONFIG
        ('share/' + package_name + '/rviz', [
            'rviz/lidar.rviz'
        ]),

        # CONFIG FILES
        ('share/' + package_name + '/config', [
            'config/params.yaml',
            'config/controllers.yaml'
        ]),

        # URDF FILES
        (
            'share/' + package_name + '/description/urdf',
            [
                'description/urdf/aeron.urdf.xacro',
                'description/urdf/aeron.urdf',
                'description/urdf/base.xacro',
                'description/urdf/drive_wheel.xacro',
                'description/urdf/caster.xacro',
            ],
        ),

        # ROS2 CONTROL FILE
        (
            'share/' + package_name + '/description/ros2_control',
            ['description/ros2_control/aeron.ros2_control.xacro'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='User',
    maintainer_email='user@example.com',
    description='PC-side ROS 2 system',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [
            'subscriber_node = pc_core.subscriber_node:main',
            'processing_node = pc_core.processing_node:main',
            'cmd_vel_bridge = pc_core.cmd_vel_bridge:main',
        ],
    },
)