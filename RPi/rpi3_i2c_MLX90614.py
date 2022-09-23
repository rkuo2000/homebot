#!/usr/bin/python

import time
import MLX90614

# Create a VL53L0X object
mlx = MLX90614.MLX90614()

amb_temp = mlx.get_amb_temp()
print("ambient temperature = ",amb_temp)

obj_temp = mlx.get_obj_temp()
print("object temperature = ",obj_temp)
