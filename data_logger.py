
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix, Temperature, FluidPressure
from datetime import datetime


class DataLogger(Node):
    """Log sensor readings and calculate statistics."""

    def __init__(self):
        super().__init__('data_logger')
        self.data = {
            'temperature': [],
            'pressure': [],
            'acceleration': [],
            'altitude': []
        }

        self.create_subscription(
            Temperature, '/temperature', self.temp_callback, 10)
        self.create_subscription(
            FluidPressure, '/barometer', self.pressure_callback, 10)
        self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10)
        self.create_subscription(
            NavSatFix, '/gps/fix', self.gps_callback, 10)

        self.create_timer(5.0, self.print_summary)
        self.get_logger().info('Data Logger started')

    def record(self, name, value):
        """Record a timestamped sensor reading."""
        self.data[name].append(value)
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.get_logger().info(
            f'[{timestamp}] {name}: {value:.2f}')

    def temp_callback(self, msg):
        """Receive temperature data."""
        self.record('temperature', msg.temperature)

    def pressure_callback(self, msg):
        """Receive barometer data."""
        self.record('pressure', msg.fluid_pressure)

    def imu_callback(self, msg):
        """Receive IMU acceleration."""
        self.record('acceleration', msg.linear_acceleration.z)

    def gps_callback(self, msg):
        """Receive GPS altitude."""
        self.record('altitude', msg.altitude)

    def print_summary(self):
        """Print min, max, and average every five seconds."""
        self.get_logger().info('===== SENSOR SUMMARY =====')
        for name, values in self.data.items():
            if values:
                self.get_logger().info(
                    f'{name}: Min={min(values):.2f}, '
                    f'Max={max(values):.2f}, '
                    f'Avg={sum(values)/len(values):.2f}'
                )


def main(args=None):
    """Start the data logger."""
    rclpy.init(args=args)
    node = DataLogger()
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
