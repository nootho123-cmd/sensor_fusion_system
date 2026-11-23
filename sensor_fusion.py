
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, NavSatFix, Temperature, FluidPressure
from std_msgs.msg import String


class SensorFusion(Node):
    """Combine sensor readings to estimate robot state."""

    def __init__(self):
        super().__init__('sensor_fusion')

        self.gps = None
        self.pressure = None
        self.temperature = None
        self.acceleration = None

        self.publisher = self.create_publisher(
            String, '/fused_state', 10)

        self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10)
        self.create_subscription(
            NavSatFix, '/gps/fix', self.gps_callback, 10)
        self.create_subscription(
            Temperature, '/temperature', self.temp_callback, 10)
        self.create_subscription(
            FluidPressure, '/barometer', self.pressure_callback, 10)

        self.create_timer(1.0, self.fuse_data)
        self.get_logger().info('Sensor Fusion started')

    def imu_callback(self, msg):
        """Store acceleration magnitude."""
        a = msg.linear_acceleration
        self.acceleration = math.sqrt(a.x**2 + a.y**2 + a.z**2)

    def gps_callback(self, msg):
        """Store GPS coordinates and altitude."""
        self.gps = (msg.latitude, msg.longitude, msg.altitude)

    def temp_callback(self, msg):
        """Store temperature."""
        self.temperature = msg.temperature

    def pressure_callback(self, msg):
        """Store atmospheric pressure."""
        self.pressure = msg.fluid_pressure

    def fuse_data(self):
        """Combine available readings and publish robot state."""
        if any(x is None for x in (
            self.gps, self.pressure,
            self.temperature, self.acceleration
        )):
            self.get_logger().info('Waiting for sensor data...')
            return

        # Standard-atmosphere barometric altitude approximation
        baro_altitude = 44330.0 * (
            1.0 - (self.pressure / 101325.0)**0.1903
        )

        # Simple weighted altitude estimate
        fused_altitude = 0.7 * self.gps[2] + 0.3 * baro_altitude

        state = (
            f'GPS=({self.gps[0]:.6f}, {self.gps[1]:.6f}), '
            f'Altitude={fused_altitude:.2f}m, '
            f'Temperature={self.temperature:.2f}C, '
            f'Acceleration={self.acceleration:.2f}m/s2'
        )

        msg = String()
        msg.data = state
        self.publisher.publish(msg)
        self.get_logger().info(state)


def main(args=None):
    """Start the sensor fusion node."""
    rclpy.init(args=args)
    node = SensorFusion()
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
