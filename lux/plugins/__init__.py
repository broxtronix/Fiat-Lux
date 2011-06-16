import traceback
import sys

try:

    # -----------------------------------------
    
    # List plugins to be imported here
    import simple


    # -----------------------------------------


    
except ImportError as inst:
    print '-'*60
    print "Error: plugin generated an exception."
    traceback.print_exc(file=sys.stdout)
    print '-'*60
    sys.exit(0)
