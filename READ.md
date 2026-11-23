
# Multi-Sensor Data Fusion System

## Week 3 ROS2 Project
University of Petra  
Course: Robotics Programming  
ROS2 Jazzy | Ubuntu 24.04 | Python 3.12

## 1. Project Overview

This project implements a simulated robot sensor monitoring and data fusion system using ROS2.

The system collects simulated IMU, GPS, temperature, and barometric pressure data. It logs readings, detects abnormal conditions, and combines sensor information to estimate the robot's state.

No physical sensors are required.

## 2. System Architecture

The system contains four ROS2 nodes:

```text
                  Sensor Publisher
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Data Logger    Alert System   Sensor Fusion
          |              |              |
      Statistics       /alerts      /fused_state
```

All three processing nodes subscribe to the sensor publisher's topics.

## 3. Topic Communication Diagram

```text
Sensor Publisher
    |
    +-- /imu/data -----------+
    +-- /gps/fix ------------+
    +-- /temperature --------+
    +-- /barometer ----------+
                             |
                +------------+------------+
                |            |            |
           Data Logger  Alert System  Sensor Fusion
                |            |            |
           Statistics     /alerts     /fused_state
```

## 4. Node Documentation

### sensor_publisher.py

Publishes simulated sensor data with random noise.

- IMU: 10 Hz
- GPS: 1 Hz
- Temperature: 2 Hz
- Barometer: 2 Hz

Functions:
- `publish_imu()`: Publishes acceleration.
- `publish_gps()`: Publishes GPS position and altitude.
- `publish_temperature()`: Publishes temperature.
- `publish_pressure()`: Publishes atmospheric pressure.

### data_logger.py

Subscribes to all four sensor topics.

Functions:
- `record()`: Logs timestamped sensor readings.
- `temp_callback()`: Receives temperature.
- `pressure_callback()`: Receives pressure.
- `imu_callback()`: Receives acceleration.
- `gps_callback()`: Receives GPS altitude.
- `print_summary()`: Prints minimum, maximum, and average every 5 seconds.

### alert_system.py

Monitors sensor readings for abnormal conditions.

Alert conditions:
- Temperature above 28 C or below 22 C.
- Pressure outside 91800-92200 Pa.
- Acceleration magnitude outside 8.5-11.0 m/s2.
- GPS outside the expected coordinate range.

Functions:
- `send_alert()`: Publishes warnings to `/alerts`.
- `check_temp()`: Checks temperature.
- `check_pressure()`: Checks pressure.
- `check_imu()`: Checks acceleration.
- `check_gps()`: Checks GPS position.

### sensor_fusion.py

Combines sensor readings to estimate robot state.

Functions:
- `imu_callback()`: Stores acceleration magnitude.
- `gps_callback()`: Stores GPS coordinates and altitude.
- `temp_callback()`: Stores temperature.
- `pressure_callback()`: Stores barometric pressure.
- `fuse_data()`: Calculates fused altitude and publishes robot state.

The altitude estimate combines 70% GPS altitude with 30% barometric altitude calculated using a standard-atmosphere approximation.

This is a simple weighted fusion method, not a Kalman filter.

## 5. ROS2 Topics

| Topic | Message Type | Publisher |
|---|---|---|
| /imu/data | sensor_msgs/Imu | sensor_publisher |
| /gps/fix | sensor_msgs/NavSatFix | sensor_publisher |
| /temperature | sensor_msgs/Temperature | sensor_publisher |
| /barometer | sensor_msgs/FluidPressure | sensor_publisher |
| /alerts | std_msgs/String | alert_system |
| /fused_state | std_msgs/String | sensor_fusion |

## 6. Installation

Requirements:
- Ubuntu 24.04
- ROS2 Jazzy
- Python 3.12

Build the package:

```bash
cd ~/ros2_ws
colcon build --packages-select sensor_fusion_system --symlink-install
source install/setup.bash
```

## 7. Running the System

Open four terminals. In each terminal, source the workspace:

```bash
source ~/ros2_ws/install/setup.bash
```

Run one node per terminal:

Terminal 1:
```bash
ros2 run sensor_fusion_system sensor_publisher
```

Terminal 2:
```bash
ros2 run sensor_fusion_system data_logger
```

Terminal 3:
```bash
ros2 run sensor_fusion_system alert_system
```

Terminal 4:
```bash
ros2 run sensor_fusion_system sensor_fusion
```

## 8. Testing

List active topics:

```bash
ros2 topic list
```

Check published alerts:

```bash
ros2 topic echo /alerts
```

Check fused sensor data:

```bash
ros2 topic echo /fused_state
```

Verify that:
1. Sensor readings are published continuously.
2. The logger displays statistics every 5 seconds.
3. Abnormal readings generate warnings.
4. The fusion node publishes estimated altitude and robot state.

## 9. Conclusion

The project demonstrates ROS2 publisher-subscriber communication, simulated sensor monitoring, anomaly detection, statistical logging, and basic multi-sensor fusion.

All four nodes can operate simultaneously and communicate through ROS2 topics.
