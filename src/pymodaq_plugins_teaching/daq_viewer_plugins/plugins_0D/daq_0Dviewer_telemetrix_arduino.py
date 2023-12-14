import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter
import sys
import time
from telemetrix import telemetrix



#class PythonWrapperOfYourInstrument:
    #  TODO Replace this fake class with the import of the real python wrapper of your instrument
    #pass


class DAQ_0DViewer_telemetrix_arduino(DAQ_Viewer_base):
    """
    """
    #params = comon_parameters+[
        ## TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
    #]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: telemetrix = None

        #TODO declare here attributes you want/need to init with a default value
        self.controller.__init__(self)
        pass
        self.temp = None
    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """


        ## TODO for your custom plugin
        #if param.name() == "a_parameter_you've_added_in_self.params":
           #self.controller.your_method_to_apply_this_param_change()  # when writing your own plugin replace this line
#        elif ...
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
        self.ini_detector_init(old_controller=controller,
                               new_controller=telemetrix())

        # TODO for your custom plugin (optional) initialize viewers panel with the future type of data

        controller.i2c_write(96,[5, 4])
        controller.i2c_write(96,[6, 1<<7])
        controller.i2c_write(96,[6, 1<<5])
        controller.i2c_write(96, [6, 0 << 2])
        controller.i2c_write(96, [6, 0])

        info = "Whatever info you want to log"
        initialized = self.controller.set_pin_mode_i2c()  # TODO
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
        callback=[]


        self.controller.i2c_read_restart_transmission(96, 0, 2, callback, i2c_port=0, write_register=True)  # when writing your own plugin replace this line
        #########################################################


    def callback(self, data):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        first_byte = data[5]
        sec_byte = data[6]
        data_tot = ((first_byte << 8) | sec_byte) / 16

        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        self.controller.your_method_to_stop_acquisition()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        ##############################
        return ''


if __name__ == '__main__':
    main(__file__)
