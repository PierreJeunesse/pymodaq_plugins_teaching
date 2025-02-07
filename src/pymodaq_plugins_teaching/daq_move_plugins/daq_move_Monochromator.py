from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main, DataActuatorType,\
    DataActuator  # common set of parameters for all actuators
from pymodaq.utils.daq_utils import ThreadCommand # object used to send info back to the main thread
from pymodaq.utils.parameter import Parameter


#class PythonWrapperOfYourInstrument:
    #  TODO Replace this fake class with the import of the real python wrapper of your instrument
   # pass

from pymodaq_plugins_teaching.hardware.spectrometer import Spectrometer
class DAQ_Move_Monochromator(DAQ_Move_base):
    """Plugin for the Template Instrument

    This object inherits all functionality to communicate with PyMoDAQ Module through inheritance via DAQ_Move_base
    It then implements the particular communication with the instrument

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library
    # TODO add your particular attributes here if any

    """
    _controller_units = 'whatever'  # TODO for your plugin: put the correct unit here
    is_multiaxes = True  # TODO for your plugin set to True if this plugin is controlled for a multiaxis controller
    axes_names = ['Axis1', 'Axis2']  # TODO for your plugin: complete the list
    _epsilon = 0.1  # TODO replace this by a value that is correct depending on your controller
    data_actuator_type = DataActuatorType['DataActuator']  # wether you use the new data style for actuator otherwise set this
    # as  DataActuatorType['float']  (or entirely remove the line)

    params = [  {'title' : 'Grating' , 'name' : 'gratinglist', 'type':'list', 'limits':Spectrometer.gratings},
                {'title' : 'Tau', 'name' : 'tauvalue', 'type':'int', 'value': '2',}
                ] + comon_parameters_fun(is_multiaxes, axes_names, epsilon=_epsilon)

    # _epsilon is the initial default value for the epsilon parameter allowing pymodaq to know if the controller reached
    # the target value. It is the developer responsibility to put here a meaningful value

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: Spectrometer = None


        #TODO declare here attributes you want/need to init with a default value
        self.controller.__init__(self)
        pass

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        pos = DataActuator(data=self.controller.get_wavelength())  # when writing your own plugin replace this line
        pos = self.get_position_with_scaling(pos)
        return pos

    def close(self):
        """Terminate the communication protocol"""
        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        self.controller.close_communication()  # when writing your own plugin replace this line

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "gratings":
           self.controller.grating = param.value()
        else:
            pass
        if param.name() == "tau":
            self.controller.tau = param.value()
        else:
            pass


    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        #raise NotImplemented  # TODO when writing your own plugin remove this line and modify the one below
        self.controller = self.ini_stage_init(old_controller=controller,
                                              new_controller=Spectrometer())

        info = "Whatever info you want to log"
        initialized = self.controller.open_communication()
        # todo
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  #if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        self.controller.set_wavelength (value.value())  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        self.controller.set_wavelength (value.value(),'rel')  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def move_home(self):
        """Call the reference method of the controller"""

        ## TODO for your custom plugin
        #raise NotImplemented  # when writing your own plugin remove this line
        self.controller.set_wavelength (value.value(),'532')  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def stop_motion(self):
      """Stop the actuator and emits move_done signal"""

      ## TODO for your custom plugin
      #raise NotImplemented  # when writing your own plugin remove this line
      #self.controller.your_method_to_stop_positioning()  # when writing your own plugin replace this line
      self.emit_status(ThreadCommand('Update_Status', ['Not possible to stop']))


if __name__ == '__main__':
    main(__file__)
