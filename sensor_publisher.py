
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix, Temperature, FluidPressure
import random


class SensorPublisher(Node):
    """Simulate and publish four robot sensors."""

    def __init__(self):
        super().__init__('sensor_publisher')

        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.gps_pub = self.create_publisher(NavSatFix, '/gps/fix', 10)
        self.temp_pub = self.create_publisher(
            Temperature, '/temperature', 10)
        self.pressure_pub = self.create_publisher(
            FluidPressure, '/barometer', 10)

        self.create_timer(0.1, self.publish_imu)
        self.create_timer(1.0, self.publish_gps)
        self.create_timer(0.5, self.publish_temperature)
        self.create_timer(0.5, self.publish_pressure)

        self.get_logger().info('Sensor Publisher started')

    def publish_imu(self):
        """Publish simulated acceleration at 10 Hz."""
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'
        msg.linear_acceleration.x = random.gauss(0, 0.2)
        msg.linear_acceleration.y = random.gauss(0, 0.2)
        msg.linear_acceleration.z = random.gauss(9.81, 0.2)
        msg.orientation_covariance[0] = -1.0
        msg.angular_velocity_covariance[0] = -1.0
        self.imu_pub.publish(msg)

    def publish_gps(self):
        """Publish simulated GPS coordinates at 1 Hz."""
        msg = NavSatFix()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'gps_link'
        msg.latitude = 31.95 + random.gauss(0, 0.00001)
        msg.longitude = 35.93 + random.gauss(0, 0.00001)
        msg.altitude = 800.0 + random.gauss(0, 1.0)
        self.gps_pub.publish(msg)
        self.get_logger().info(f'GPS: {msg.latitude:.6f}, {msg.longitude:.6f}')

    def publish_temperature(self):
        """Publish simulated temperature at 2 Hz."""
        msg = Temperature()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'temperature_sensor'
        msg.temperature = random.gauss(25.0, 2.0)
        msg.variance = 4.0
        self.temp_pub.publish(msg)
        self.get_logger().info(f'Temperature: {msg.temperature:.2f} C')

    def publish_pressure(self):
        """Publish simulated barometric pressure at 2 Hz."""
        msg = FluidPressure()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'barometer_link'
        msg.fluid_pressure = random.gauss(92000.0, 40.0)
        msg.variance = 1600.0
        self.pressure_pub.publish(msg)
        self.get_logger().info(
            f'Pressure: {msg.fluid_pressure:.2f} Pa')


def main(args=None):
    """Start the ROS2 sensor publisher."""
    rclpy.init(args=args)
    node = SensorPublisher()
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
