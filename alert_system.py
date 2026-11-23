
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix, Temperature, FluidPressure
from std_msgs.msg import String
import math


class AlertSystem(Node):
    """Monitor sensors and publish anomaly alerts."""

    def __init__(self):
        super().__init__('alert_system')

        self.alert_pub = self.create_publisher(String, '/alerts', 10)

        self.create_subscription(
            Temperature, '/temperature', self.check_temp, 10)
        self.create_subscription(
            FluidPressure, '/barometer', self.check_pressure, 10)
        self.create_subscription(
            Imu, '/imu/data', self.check_imu, 10)
        self.create_subscription(
            NavSatFix, '/gps/fix', self.check_gps, 10)

        self.get_logger().info('Alert System started')

    def send_alert(self, message):
        """Publish an alert and log a warning."""
        msg = String()
        msg.data = message
        self.alert_pub.publish(msg)
        self.get_logger().warn(message)

    def check_temp(self, msg):
        """Detect abnormal temperatures."""
        if msg.temperature > 28.0:
            self.send_alert('HIGH TEMPERATURE!')
        elif msg.temperature < 22.0:
            self.send_alert('LOW TEMPERATURE!')

    def check_pressure(self, msg):
        """Detect abnormal atmospheric pressure."""
        if not 91800.0 <= msg.fluid_pressure <= 92200.0:
            self.send_alert('ABNORMAL PRESSURE!')

    def check_imu(self, msg):
        """Detect unusually high acceleration."""
        a = msg.linear_acceleration
        magnitude = math.sqrt(a.x**2 + a.y**2 + a.z**2)
        if magnitude > 11.0 or magnitude < 8.5:
            self.send_alert('ABNORMAL ACCELERATION!')

    def check_gps(self, msg):
        """Detect GPS coordinates outside the expected area."""
        if not (31.94 <= msg.latitude <= 31.96 and
                35.92 <= msg.longitude <= 35.94):
            self.send_alert('GPS OUT OF RANGE!')


def main(args=None):
    """Start the alert system."""
    rclpy.init(args=args)
    node = AlertSystem()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
