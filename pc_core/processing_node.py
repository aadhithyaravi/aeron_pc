"""
PC-side ROS 2 processing node for LiDAR data analysis.
Maintains a buffer of recent scans and computes statistics.
"""

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy
from collections import deque
from sensor_msgs.msg import LaserScan


class ProcessingNode(Node):
    """Processing node that analyzes LiDAR data and maintains a buffer."""

    def __init__(self):
        super().__init__('processing_node')

        # Declare parameters
        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('processed_topic', '/processed_scan')
        self.declare_parameter('buffer_size', 10)
        self.declare_parameter('publish_processed', False)
        self.declare_parameter('debug', True)

        scan_topic = self.get_parameter('scan_topic').value
        processed_topic = self.get_parameter('processed_topic').value
        self.buffer_size = self.get_parameter('buffer_size').value
        self.publish_processed = self.get_parameter('publish_processed').value
        self.debug = self.get_parameter('debug').value

        # Initialize buffer
        self.scan_buffer = deque(maxlen=self.buffer_size)
        self.stats = {
            'min_distance': float('inf'),
            'max_distance': 0.0,
            'total_points': 0,
            'frames_received': 0
        }

        # QoS profile for sensor data
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )

        # Subscriber
        self.scan_sub = self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            qos_profile
        )

        # Publisher (optional)
        if self.publish_processed:
            self.scan_pub = self.create_publisher(LaserScan, processed_topic, qos_profile)
        else:
            self.scan_pub = None

        self.get_logger().info(f'Processing node started (buffer_size={self.buffer_size})')
        self.get_logger().info(f'Subscribing to: {scan_topic}')

    def scan_callback(self, msg: LaserScan):
        """Process and analyze incoming LaserScan messages."""
        # Add to buffer
        self.scan_buffer.append(msg)
        self.stats['frames_received'] += 1

        # Compute statistics on current frame
        valid_ranges = [r for r in msg.ranges if r != float('inf') and r > 0.0]

        if valid_ranges:
            frame_min = min(valid_ranges)
            frame_max = max(valid_ranges)
            frame_points = len(valid_ranges)

            # Update running statistics
            self.stats['min_distance'] = min(self.stats['min_distance'], frame_min)
            self.stats['max_distance'] = max(self.stats['max_distance'], frame_max)
            self.stats['total_points'] += frame_points

            # Log stats
            if self.debug:
                self.get_logger().debug(
                    f'Scan stats: min={frame_min:.3f}m, max={frame_max:.3f}m, '
                    f'points={frame_points}, buffer_size={len(self.scan_buffer)}'
                )

        # Publish processed scan if enabled
        if self.scan_pub:
            self.scan_pub.publish(msg)

    def get_stats(self):
        """Return current statistics."""
        return {
            **self.stats,
            'buffer_fill_level': len(self.scan_buffer),
            'avg_points_per_frame': (
                self.stats['total_points'] / self.stats['frames_received']
                if self.stats['frames_received'] > 0 else 0
            )
        }


def main(args=None):
    rclpy.init(args=args)
    executor = rclpy.executors.SingleThreadedExecutor()
    node = ProcessingNode()
    executor.add_node(node)

    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        stats = node.get_stats()
        node.get_logger().info(
            f'Processing node shutting down - '
            f'Frames: {stats["frames_received"]}, '
            f'Min dist: {stats["min_distance"]:.3f}m, '
            f'Max dist: {stats["max_distance"]:.3f}m'
        )
    finally:
        node.destroy_node()
        executor.shutdown()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()