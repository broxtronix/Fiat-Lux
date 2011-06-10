

# PluginMount Class
#
class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "plugins"):
            # If the class has no plugins list, then this must be the
            # plugin mount itself, so we add one for plugins to be
            # registered later.
            cls.plugins = []
        else:
            # Since the plugin attribute already exists, this is an
            # individual plugin instance and we register it here.
            cls.plugins.append(cls)

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

    def draw():
        pass


# Mount your plugins below.
#from plugins
