import time
from settings import *

# --------------------------------------------------------------
#                  The Parameter Object
# --------------------------------------------------------------

class Parameter(object):

    # Constants
    CONTROL_AUTOMATE = 0
    CONTROL_OVERRIDE = 1

    # Constructor
    def __init__(self, name, description,
                 namespace = 'generic_parameters',
                 min_value = 0.0, max_value = 1.0,
                 default_value = 0.0,
                 automation_timeout = 120.0, # seconds
                 stateful = False):

        # Store a local instance of the settings class
        self.settings = LuxSettings()

        # Store the parameters specific to this parameter in the class
        # instance.
        self.name = name
        self.description = description
        self.namespace = namespace
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.automation_timeout = automation_timeout  
        self.stateful = stateful
        self.value = default_value

        # Automation parameters
        self.control_mode = self.CONTROL_AUTOMATE
        self.last_control_time = 0.0

        # If this is a stateful parameter, we attempt to refresh its
        # value here (falling back to the default value if necessary).
        if (self.stateful):
            self.value = self.settings[namespace].refreshWithDefault(self.name, self.default_value)

    def set_value(self, value):
        # If the we are in control override mode, then programmatic
        # value changes are ignored until the automation timeout has
        # elapsed.
        if (self.control_mode == self.CONTROL_OVERRIDE and
            time.time() - self.last_control_time > self.automation_timeout):
            self.control_mode = self.CONTROL_AUTOMATE

        # If no control override has occurred, then the value can be
        # set programmatically.
        if (self.control_mode == self.CONTROL_AUTOMATE):
            self._set_value(value)

    # Automation (e.g. OSC messages) use this method to set the value
    # of parameters.
    def set_control_value(self, value):
        self.control_mode = self.CONTROL_OVERRIDE
        self.last_control_time = time.time()
        self._set_value(value)

    # Private method for setting the value, checking the bounds, etc.
    def _set_value(self, value):
        if (value < self.min_value):
            self.value = self.min_value
        elif (value > self.max_value):
            self.value = self.max_value
        else:
            self.value = value

        if (self.stateful):
            self.settings[self.namespace].setValue(self.name, value)
        
            
    def get_value(self):
        return self.value

    def __unicode__(self):
        return "Parameter: " + self.name

# --------------------------------------------------------------
#        The LuxParameters Class and 'lux' Instance
#
# In the scripting environment, the 'lux' object gives access to
# phosphoressence parameters.  Parameters can be accessed directly
# 'attributes' (e.g. 'lux.time' or 'lux.decay'), or they can be set
# using the methods defined below.  Parameters are defined at the
# bottom of this file.
# --------------------------------------------------------------

class LuxParameters(object):

    def __init__(self):
        self.params = {}
        self.starting_time = time.time()
        self.__initialised = True  # for __setattr__

    # --------------------- Attribute Behavior ------------------------
    #
    # We jump through quite a few hoops here in order to expose the lux
    # parameters as attributes of the Fiat Lux class instance.
    # These functions forward lookups for unknown attributes along to
    # the 'self.params' dictionary.
    def __getattr__(self, item):
        # The time attribute is handled specially
        if (item == 'time'):
            return time.time() - self.starting_time
        
        try:
           # print 'falling back to params dict!'
            return self.__dict__['params'][item].get_value()
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        # this test allows attributes to be set in the __init__ method
        if not self.__dict__.has_key('_LuxParameters__initialised'):
            return dict.__setattr__(self, item, value)

        # any normal attributes are handled normally
        elif self.__dict__.has_key(item):
            dict.__setattr__(self, item, value)

        # the remaining attributes are delegated to the 'params' dictionary 
        elif  self.__dict__['params'].has_key(item): 
            self.__dict__['params'][item].set_value(value)

        else:
            raise AttributeError(item)        

    def lux_time(self):
        return time.time() - self.starting_time

    # ------------------ Parameter Control Methods --------------------

    # Register a new paramater.  This store the parameter in a
    # dictionary, and then creates a class property for its access.
    def register(self, parameter):
        self.params[parameter.name] = parameter

    # There are two flavors for setting parameter values.  The first,
    # set_value(), is equivelent to setting the attribute value
    # directly from the script.  This form of setting the value may be
    # overridden by the set_control_value() method below.
    def set_value(self, name, value):
        self.params[name].set_value(value)

    # Set the value of a parameter using a physical controller.  This
    # method of setting parameter values always takes precedence over
    # set_value(), and may leave the parameter at this value for a
    # certain amount of time before it reverts to being controllable
    # from the scripting environment.
    def set_control_value(self, name, value):
        self.params[name].set_control_value(value)

    # Reset all parameters to their default values
    def reset_all(self):
        for p in self.params.values():
            p.value = p.default_value

    # Returns True if we have a certain parameter
    def has_parameter(self, name):
        return self.params.has_key(name)

    # Returns a list of paramters
    def param_list(self):
        l = self.params.keys()
        l.append("time")
        return l
    
# Create the instance of the LuxParameters class.  Note: don't go
# creating your own instance.  This should be the only one!!  (TODO:
# Maybe it should be a singleton class?)
lux = LuxParameters()



