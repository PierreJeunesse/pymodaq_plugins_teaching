import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter
import sys
import time
from pymodaq_plugins_teaching.hardware.arduino_MPC9600_wrapper import ThermocoupleWrapper

from serial.tools import list_ports
ports = [str(port.name) for port in list_ports.comports()]
port = 'COM7'

class DAQ_0DViewer_MCP9600_arduino(DAQ_Viewer_base):
    """
    """
    params = comon_parameters+[{'title': 'Axis:', 'name': 'axis', 'type': 'int', 'value': 1.00},
        {'title': 'Com port:', 'name': 'comport', 'type': 'str', 'limits': ports, 'value': port,'tip': 'The serial COM port'},

        ## TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
        ]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller = ThermocoupleWrapper()


        #TODO declare here attributes you want/need to init with a default value

        self._temp = None



    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        if param.name() == 'comport':
            self.temperature = param.value()

        elif param.name() == 'axis':
            self.axis = param.value()

        ## TODO for your custom plugin
        #if param.name() == "a_parameter_you've_added_in_self.params":
        #self.controller.your_method_to_apply_this_param_change()  # when writing your own plugin replace this line
        #elif ...
        ##

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        #raise NotImplemented  # TODO when writing your own plugin remove this line and modify the one below
        self.ini_detector_init(old_controller=controller, new_controller=ThermocoupleWrapper())
        self.controller.open_communication(self.settings.child('comport').value())
        self.controller.mpc9600_setup()

        # TODO for your custom plugin (optional) initialize viewers panel with the future type of data

        info = "Connected"
        initialized = True  # todo
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        #  self.controller.your_method_to_terminate_the_communication()  # when writing your own plugin replace this line

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin

        # synchrone version (blocking function)
        #raise NotImplemented  # when writing your own plugin remove this line
        #
        #self.dte_signal.emit(DataToExport(name='myplugin',
        #                                 data=[DataFromPlugins(name='Mock1', data=data_tot,
        #                                                       dim='Data0D', labels=['dat0', 'data1'])]))
        #########################################################

        # asynchrone version (non-blocking function with callback)
        #raise NotImplemented  # when writing your own plugin remove this line

        #data = []

          # when writing your own plugin replace this line
        #########################################################


        def the_callback(data):
            _temp = self.controller.the_callback(data)


            self.dte_signal.emit(DataToExport(name='Temperature',
                                          data=[DataFromPlugins(name='Temp', data=_temp,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))
        self.controller.grab_MPC9600(the_callback)



    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        self.controller.close_communication()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Communication closed']))
        ##############################
        return ''


if __name__ == '__main__':
    main(__file__)
