"""
Demo Wrapper to illustrate the plugin developpement. This Mock wrapper will emulate communication with an instrument
"""

from time import perf_counter, sleep
import time
import math

from serial.tools import list_ports
ports = [port.name for port in list_ports.comports()]

from telemetrix import telemetrix
class ThermocoupleWrapper:
    units = 'degree (Celsius)'
    def __init__(self):
        self.board = None


    def open_communication(self, port):
        """
        fake instrument opening communication.
        Returns
        -------
        bool: True is instrument is opened else False
        """
        self.board=telemetrix.Telemetrix(com_port=port,arduino_wait=4)
        return True

    def the_callback(self,data):
        """

        :param data: [Device address, device read register, data]
        :return:
        """

        first_byte = data[5]
        sec_byte = data[6]
        _temp = ((first_byte << 8) | sec_byte) / 16
        return _temp

    def grab_MPC9600(self, callback):
        self.board.i2c_read_restart_transmission(96, 0, 2, callback, i2c_port=0, write_register=True)
        time.sleep(0.5)

    def mpc9600_setup(self):
        # setup mpc9600
        # device address = 96
        self.board.set_pin_mode_i2c()  # #define DEFAULT_IIC_ADDR  0X60 (in Seeed_MCO9600.h)

        # err_t sensor_basic_config() {
        #     err_t ret = NO_ERROR;
        #     CHECK_RESULT(ret, sensor.set_filt_coefficients(FILT_MID)); (in Seeed_MCO9600.cpp)
        #           IIC_read_byte(THERM_SENS_CFG_REG_ADDR, &therm_cfg_data) (in Seeed_MCO9600.cpp)
        #               THERM_SENS_CFG_REG_ADDR : 0X5 => 5 (in Seeed_MCO9600.h)
        #               FILT_MID : 4 (in Seeed_MCO9600.h)
        self.board.i2c_write(96, [5, 4])
        time.sleep(1)

        #     CHECK_RESULT(ret, sensor.set_cold_junc_resolution(COLD_JUNC_RESOLUTION_0_25));
        #           same logic as above
        self.board.i2c_write(96, [6, 1 << 7])
        time.sleep(1)

        #     CHECK_RESULT(ret, sensor.set_ADC_meas_resolution(ADC_14BIT_RESOLUTION));
        self.board.i2c_write(96, [6, 1 << 5])
        time.sleep(1)

        #     CHECK_RESULT(ret, sensor.set_burst_mode_samp(BURST_32_SAMPLE));
        self.board.i2c_write(96, [6, 0 << 2])
        time.sleep(1)

        #     CHECK_RESULT(ret, sensor.set_sensor_mode(NORMAL_OPERATION));
        self.board.i2c_write(96, [6, 0])
        time.sleep(1)

    def close_communication(self):
        self.board.shutdown()
        return f'Board disconnected:'






