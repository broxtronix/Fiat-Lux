import colorsys
import random
import pylase as ol
from settings import LuxSettings
import math

# PluginMount Class
#
class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "plugins"):
            # If the class has no plugins list, then this must be the
            # plugin mount itself, so we add one for plugins to be
            # registered later.
            cls.plugins = {}
            cls.plugin_keys = []
        else:
            # Since the plugin attribute already exists, this is an
            # individual plugin instance and we register it here.
            cls.plugin_keys = cls.name
            cls.plugins[cls.name] = cls

# LuxPlugin Class
#
class LuxPlugin(object):
    """
    Plugins that inherit from this class will automatically be
    registered with Fiat Lux.  This class also provides default
    implementations for important methods that you may override in
    your plugins.
    """
    __metaclass__ = PluginMount

    name = "(unnamed plugin)"
    
    description = "No Description"

    def draw(self):
        pass

    # Override this method if you want to set parameters yourself in
    # your plugin.  The default behavior is that the plugin uses the
    # current parameters set in the GUI (regardless of whether the
    # override button is pressed.
    def setParameters(self):
        self.setParametersToGuiValues()

    def setParametersToGuiValues(self):
        settings = LuxSettings()
        params = ol.getRenderParams()
        params.rate = settings['calibration'].olRate
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/settings['calibration'].olOnSpeed
        params.off_speed = 1.0/settings['calibration'].olOffSpeed
        params.start_wait = settings['calibration'].olStartWait
        params.start_dwell = settings['calibration'].olStartDwell
        params.curve_dwell = settings['calibration'].olCurveDwell
        params.corner_dwell = settings['calibration'].olCornerDwell
        params.curve_angle = math.cos(30.0*(math.pi/180.0)); # 30 deg
        params.end_dwell = settings['calibration'].olEndDwell
        params.end_wait = settings['calibration'].olEndWait
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)


# ColorDriftPlugin
#
# Mixin class useful for giving plugins some color.  Call
# color_cycle() here to return an rgb tuple that automatically
# evolves.
class ColorDriftPlugin(object):
    def __init__(self):
        self.current_hue = random.random()
        self.hue_target = random.random()
        self.hue_step = 1.0/10000.0

    # Slow, random evolution of hue. 
    def color_cycle(self):
        if (abs(self.hue_target - self.current_hue) < self.hue_step):
            self.hue_target = random.random()
        
        if (self.hue_target > self.current_hue):
            self.current_hue = self.current_hue + self.hue_step
        else:
            self.current_hue = self.current_hue - self.hue_step
            
        return colorsys.hsv_to_rgb(self.current_hue, 1.0, 1.0)

