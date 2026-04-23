"""
Stage 1. PID Controller for single variable
Copied and adapted from lab_1.py
"""

class PIDController:
    
    def __init__(self, kp=0.5, ki=0.01, kd=0.1, max_integral=0.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_integral = max_integral
        
        self.integral = 0.0
        self.last_error = 0.0
        self.last_time = None
        
    def reset(self):
        # Reset controller state
        self.integral = 0.0
        self.last_error = 0.0
        self.last_time = None
        
    def update(self, error, current_time):
        # Calculate PID control output
        if self.last_time is None:
            self.last_time = current_time
            self.last_error = error
            return self.kp * error
            
        dt = current_time - self.last_time
        if dt <= 0:
            return self.kp * error
            
        # P term
        p_term = self.kp * error
        
        # I term + anti-windup
        self.integral += error * dt
        self.integral = np.clip(self.integral, -self.max_integral, self.max_integral)
        i_term = self.ki * self.integral
        
        # D term
        derivative = (error - self.last_error) / dt
        d_term = self.kd * derivative
        
        # Update state
        self.last_error = error
        self.last_time = current_time
        
        return p_term + i_term + d_term