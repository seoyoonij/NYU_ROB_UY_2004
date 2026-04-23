# Lab6: Active Posture Stabilization

Active posture stabilization system for Pupper v3 quadruped robot using PID control and inverse kinematics.

## Overview

This project implements active posture stabilization to keep the robot level regardless of external disturbances. The system:

1. **Reads IMU data** to get current robot orientation (roll, pitch, yaw)
2. **Calculates errors** between target (level) and current orientation
3. **PID controllers** compute corrections for roll and pitch
4. **IK solver** converts foot position adjustments to joint angles
5. **Publishes joint commands** to maintain level posture

## Architecture

```
┌─────────────┐
│  IMU Sensor │──────┐
└─────────────┘      │
                     ▼
┌─────────────┐   ┌──────────────────┐
│ Joint States│──▶│ Posture          │
└─────────────┘   │ Stabilizer Node  │
                  │                  │
                  │ • PID Controller │
                  │ • IK Solver      │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Joint Commands  │
                  └─────────────────┘
```

## Files

- **posture_stabilization.py** - Main ROS2 node with PID + IK control loop
- **ik_solver.py** - Inverse kinematics solver (adapted from Lab3)
- **launch.py** - ROS2 launch file (starts robot hardware + controllers)
- **config.yaml** - Controller configuration + PID tuning parameters
- **README.md** - This file

## Installation / Setup

No additional installation needed if you've completed Lab3. The project uses:
- `rclpy` (ROS2 Python client)
- `numpy`
- `scipy` (for IK optimization)
- Standard ROS2 packages (controller_manager, robot_state_publisher, etc.)

## Usage

### Quick Start

**Terminal 1: Launch robot hardware and controllers**
```bash
cd ~/NYU_ROB_UY_2004/Labs/Lab6
ros2 launch launch.py
```

**Terminal 2: Run posture stabilization**
```bash
cd ~/NYU_ROB_UY_2004/Labs/Lab6
python3 posture_stabilization.py
```

The robot should now actively maintain a level posture. Try gently tilting the robot body and observe it correcting.

### Testing IK Solver

You can test the IK solver independently:
```bash
python3 ik_solver.py
```

This runs a simple test showing IK accuracy for a sample foot position.

## How It Works

### PID Controller

Two independent PID controllers stabilize roll and pitch:

```python
roll_correction = Kp * error + Ki * ∫error·dt + Kd * d(error)/dt
pitch_correction = Kp * error + Ki * ∫error·dt + Kd * d(error)/dt
```

Default gains (tunable in [config.yaml](config.yaml)):
- Kp = 0.5
- Ki = 0.01
- Kd = 0.1

### Foot Position Adjustment

The corrections translate to foot height adjustments:

- **Roll correction**: Right feet move opposite to left feet
- **Pitch correction**: Front feet move opposite to back feet

Example: If robot tilts right (+roll), the right feet lift up and left feet lower to compensate.

### Inverse Kinematics

The IK solver converts desired foot positions (x, y, z) in body frame to joint angles (θ₁, θ₂, θ₃) for each leg using numerical optimization (SLSQP).

## Tuning PID Parameters

Edit [config.yaml](config.yaml) under `posture_controller` section:

```yaml
posture_controller:
  ros__parameters:
    roll_pid:
      kp: 0.5    # Increase for faster response
      ki: 0.01   # Increase to eliminate steady-state error
      kd: 0.1    # Increase to reduce oscillations
      max_integral: 0.5  # Anti-windup limit
```

**Tuning tips:**
1. Start with just P (set Ki=0, Kd=0)
2. Increase Kp until oscillations appear
3. Add Kd to dampen oscillations
4. Add small Ki to eliminate steady-state error
5. Test with disturbances (tilt the robot manually)

## Control Loop Frequency

The control loop runs at **100 Hz** (configurable in `posture_stabilization.py`):

```python
self.control_timer = self.create_timer(0.01, self.control_loop)  # 0.01s = 100Hz
```

Higher frequency = smoother control but more CPU usage.

## Troubleshooting

**Problem: "Waiting for IMU and joint state data..."**
- Check that launch.py is running
- Verify topics: `ros2 topic list`
- Should see `/imu_sensor_broadcaster/imu` and `/joint_states`

**Problem: Robot oscillates/unstable**
- Reduce Kp gain
- Increase Kd gain
- Check that control frequency is high enough (100 Hz recommended)

**Problem: IK solver fails**
- Target foot positions may be unreachable
- Check that corrections aren't too large
- Verify robot geometry parameters in config.yaml

**Problem: Slow response**
- Increase Kp gain (but watch for oscillations)
- Check control loop frequency

## Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/imu_sensor_broadcaster/imu` | sensor_msgs/Imu | Robot orientation from IMU |
| `/joint_states` | sensor_msgs/JointState | Current joint positions |
| `/forward_command_controller/commands` | std_msgs/Float64MultiArray | Joint position commands (output) |

## Parameters

Key parameters in [config.yaml](config.yaml):

- **PID gains**: `kp`, `ki`, `kd` for roll and pitch
- **Control frequency**: Update rate in Hz
- **Robot geometry**: Leg offsets and default foot positions
- **Target orientation**: Desired roll/pitch (normally 0, 0)

## Extensions / Improvements

Possible enhancements:

1. **Adaptive gains** - Adjust PID gains based on disturbance magnitude
2. **Height control** - Add vertical stabilization (z-axis)
3. **Dynamic targets** - Follow a trajectory instead of staying level
4. **Feedforward control** - Predict disturbances from velocity/acceleration
5. **State estimation** - Kalman filter for better orientation estimates
6. **Torque control** - Switch from position to torque commands for compliance

## References

- Lab3 Inverse Kinematics implementation
- Pupper v3 robot description (pupper_v3_description package)
- ROS2 control tutorials: https://control.ros.org/

## License

Educational use for NYU ROB-UY 2004 course.

---

**Author**: Lab6 Template  
**Date**: April 2026  
**Course**: NYU ROB-UY 2004 Legged Robotics
