import smbus
from time import sleep

class mpu6050:

    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    i2c = smbus.SMBus(1)

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers address
    PWR_MGMT_1  = 0x6B
    PWR_MGMT_2  = 0x6C
    SMPRT_DIV   = 0x19
    CONFIG      = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG= 0x1C
    INT_ENABLE  = 0x38

    SELF_TEST_X = 0x0D
    SELF_TEST_Y = 0x0E
    SELF_TEST_Z = 0x0F
    SELF_TEST_A = 0x10

    ACCEL_XOUT0 = 0x3B
    ACCEL_XOUT1 = 0x3C
    ACCEL_YOUT0 = 0x3D
    ACCEL_YOUT1 = 0x3E
    ACCEL_ZOUT0 = 0x3F
    ACCEL_ZOUT1 = 0x40

    TEMP_OUT0   = 0x41
    TEMP_OUT1   = 0x42

    GYRO_XOUT0 = 0x43
    GYRO_XOUT1 = 0x44
    GYRO_YOUT0 = 0x45
    GYRO_YOUT1 = 0x46
    GYRO_ZOUT0 = 0x47
    GYRO_ZOUT1 = 0x48

    def __init__(self, address):
        # initialize mpu6050
        self.address = address # set device address
        self.i2c.write_byte_data(self.address, self.PWR_MGMT_1, 0x01) # set power management
        self.i2c.write_byte_data(self.address, self.SMPLRT_DIV, 0x07) # set sample rate
        self.i2c.write_byte_data(self.address, self.CONFIG,     0x00) # set configuration reg
        self.i2c.write_byte_data(self.address, self.GYRO_CONFIG,0x24) # set gyro configuration
        self.i2c.write_byte_data(self.address, self.INT_ENABLE ,0x01) # set interrupt enable

    # i2c_dev read
    def read_i2c_word(self, register):

        high = self.i2c.read_byte_data(self.address, register)
        low = self.i2c.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    # MPU6050 functions

    def get_temp(self): # read MPU6050 built-iin temperature sensor (in Celcius)
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)
 
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340) + 36.53

        return actual_temp

    def set_accel_range(self, accel_range): # set accelerator range
 
        self.i2c.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00) # clear it to 0
        self.i2c.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range) # set new range
 
    def read_accel_range(self, raw = False): # read accelerator range
        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        
        raw_data = self.i2c.read_byte_data(self.address, self.ACCEL_CONFIG) # get raw value
 
        if raw is True: # if True, return raw_data read from MPU6050
            return raw_data
        elif raw is False: # if False, return 2,4,8,16 per ACCEL_RANGE parameter, or -1 when error
            if raw_data == self.ACCEL_RANGE_2G:
                return 2
            elif raw_data == self.ACCEL_RANGE_4G:
                return 4
            elif raw_data == self.ACCEL_RANGE_8G:
                return 8
            elif raw_data == self.ACCEL_RANGE_16G:
                return 16
            else:
                return -1
 
    def get_accel_data(self, g = False): # get accelerometer X,Y,Z value
        # Read the data from the MPU-6050
        x = self.read_i2c_word(self.ACCEL_XOUT0)
        y = self.read_i2c_word(self.ACCEL_YOUT0)
        z = self.read_i2c_word(self.ACCEL_ZOUT0)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return {'x': x, 'y': y, 'z': z}
        elif g is False:
            x = x * self.GRAVITIY_MS2
            y = y * self.GRAVITIY_MS2
            z = z * self.GRAVITIY_MS2
            return {'x': x, 'y': y, 'z': z}


    def set_gyro_range(self, gyro_range): # set gyroscope range
        self.i2c.write_byte_data(self.address, self.GYRO_CONFIG, 0x00) # clear to 0
        self.i2c.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range) # set new range

    def read_gyro_range(self, raw = False): # read gyroscope range
        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        # Get the raw value
        raw_data = self.i2c.read_byte_data(self.address, self.GYRO_CONFIG)

        if raw is True: #if True, return raw data
            return raw_data
        elif raw is False: #if False, return 250,500,1000,2000 per GYRO_RANGE parameter, or -1 when error
            if raw_data == self.GYRO_RANGE_250DEG:
                return 250
            elif raw_data == self.GYRO_RANGE_500DEG:
                return 500
            elif raw_data == self.GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == self.GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1

    def get_gyro_data(self): # get gyroscope data
        # Read the raw data from the MPU-6050
        x = self.read_i2c_word(self.GYRO_XOUT0)
        y = self.read_i2c_word(self.GYRO_YOUT0)
        z = self.read_i2c_word(self.GYRO_ZOUT0)
 
        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)
 
        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
 
        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier
 
        return {'x': x, 'y': y, 'z': z}
 
    def get_all_data(self): # get all data (accelero & gyro)
        temp = get_temp()
        acc  = get_accel_data()
        gyro = get_gyro_data()
 
        return [acc, gyro, temp]
 
if __name__ == "__main__":
    while(1):
        mpu = mpu6050(0x68)
        print("Temperature (C): ", mpu.get_temp())
        acc_data = mpu.get_accel_data()
        print("Acceleration x (m/s^2): ", acc_data['x'])
        print("Acceleration y (m/s^2): ", acc_data['y'])
        print("Acceleration z (m/s^2): ", acc_data['z'])
        gyro_data = mpu.get_gyro_data()
        print("Gyroscope x (deg/s): ", gyro_data['x'])
        print("Gyroscope y (deg/s): ", gyro_data['y'])
        print("Gyroscope z (deg/s): ", gyro_data['z'])
        print("Ax=%.2f (m/s^2)" % acc_data['x'], "\tAy=%.2f (m/s^2)" % acc_data['y'], "\tAz=%.2f (m/s^2)" % acc_data['z'],"\tGx=%.2f (m/s^2)" % gyro_data['x'], "\tGy=%.2f (m/s^2)" % gyro_data['y'], "\tGz=%.2f (m/s^2)" % gyro_data['z'])
        sleep(1)
