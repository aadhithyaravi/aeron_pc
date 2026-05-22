"""
PC-side ROS 2 subscriber node for receiving data from Raspberry Pi.
Subscribes to /scan (LaserScan) and /cmd_vel (Twist) topics.
"""

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy


class SubscriberNode(Node):
    """Subscriber node that receives LiDAR and velocity data from Pi."""

    def __init__(self):
        super().__init__('subscriber_node')

        # Declare parameters
        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('debug', True)

        scan_topic = self.get_parameter('scan_topic').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        self.debug = self.get_parameter('debug').value

        # QoS profile for sensor data (best effort for real-time)
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )

        # Subscribers
        self.scan_sub = self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            qos_profile
        )

        self.cmd_vel_sub = self.create_subscription(
            Twist,
            cmd_vel_topic,
            self.cmd_vel_callback,
            qos_profile
        )

        self.get_logger().info(f'Subscriber node started')
        self.get_logger().info(f'Subscribing to: {scan_topic} and {cmd_vel_topic}')

    def scan_callback(self, msg: LaserScan):
        """Process incoming LaserScan messages."""
        # Validate message integrity
        if len(msg.ranges) == 0:
            self.get_logger().warn('Received empty LaserScan message', throttle_duration_sec=5.0)
            return

        # Log basic info
        if self.debug:
            self.get_logger().debug(
                f'Scan: ranges={len(msg.ranges)}, '
                f'angle_min={msg.angle_min:.2f}, angle_max={msg.angle_max:.2f}, '
                f'frame_id={msg.header.frame_id}'
            )

    def cmd_vel_callback(self, msg: Twist):
        """Process incoming Twist messages."""
        # Log velocity commands
        if self.debug:
            self.get_logger().debug(
                f'CmdVel: linear=({msg.linear.x:.2f}, {msg.linear.y:.2f}, {msg.linear.z:.2f}), '
                f'angular=({msg.angular.x:.2f}, {msg.angular.y:.2f}, {msg.angular.z:.2f})'
            )


def main(args=None):
    rclpy.init(args=args)
    executor = rclpy.executors.SingleThreadedExecutor()
    node = SubscriberNode()
    executor.add_node(node)

    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        executor.shutdown()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()