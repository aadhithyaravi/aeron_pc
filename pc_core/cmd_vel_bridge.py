import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped


class CmdVelBridge(Node):

    def __init__(self):
        super().__init__('cmd_vel_bridge')

        # Subscribe to /cmd_vel (Twist)
        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.callback,
            10
        )

        # Publish to controller (TwistStamped)
        self.pub = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )

        self.get_logger().info("🔥 cmd_vel_bridge started")

    def callback(self, msg):

        stamped = TwistStamped()

        # Time stamp (VERY IMPORTANT)
        stamped.header.stamp = self.get_clock().now().to_msg()
        stamped.header.frame_id = 'base_link'

        # Copy values PROPERLY
        stamped.twist.linear.x = msg.linear.x
        stamped.twist.linear.y = msg.linear.y
        stamped.twist.linear.z = msg.linear.z

        stamped.twist.angular.x = msg.angular.x
        stamped.twist.angular.y = msg.angular.y
        stamped.twist.angular.z = msg.angular.z

        self.pub.publish(stamped)

        self.get_logger().info(
            f"Sent → lin.x={msg.linear.x:.2f}, ang.z={msg.angular.z:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()