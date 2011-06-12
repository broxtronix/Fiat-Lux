import os
import SCons.Util

# -----------------------
# SETUP BUILD ENVIRONMENT
# -----------------------

env = Environment()
conf = Configure(env)

# Add osx include and lib paths (if they exist!)
if os.path.exists('/opt/local'):
    env.Append(CPPPATH=["/opt/local/include"])
    env.Append(LIBPATH=["/opt/local/lib"])

# AUTOCONFIGURATION

if not conf.CheckCXX():
    print('!! Your compiler and/or environment is not correctly configured.')
    Exit(0)

if not conf.CheckFunc('printf'):
    print('!! Your compiler and/or environment is not correctly configured.')
    Exit(0)

# check for math.h
if not conf.CheckLibWithHeader('m', 'math.h', 'c++'):
    print "You need libm to compile this program"
    Exit(1)

# Check for boost-system
if not conf.CheckLib('boost_system-mt'):
 conf.env['boost-system'] = "no"

env = conf.Finish()

# BASIC COMPILER FLAGS

env.Append(CXXFLAGS = ' -I. -I/usr/X11/include -O3')
env.Append(LINKFLAGS = ' -L/usr/X11/lib -O3')

# IMPORT ENVIRONMENT VARIABLES

if os.environ.has_key('HOME'):
    env['HOME'] = os.environ['HOME']
    print("\t--> Setting HOME : " + os.environ['HOME'])

if os.environ.has_key('CXX'):
    env.Replace(CXX = os.environ['CXX'])
    print("\t--> Using C++ compiler " + os.environ['CXX'])

if os.environ.has_key('CC'):
    env.Replace(CC = os.environ['CC'])
    print("\t--> Using C compiler " + os.environ['CC'])

if os.environ.has_key('CXXFLAGS'):
    env.Append(CXXFLAGS = os.environ['CXXFLAGS'])
    print("\t--> Appending custom CXXFLAGS : " + os.environ['CXXFLAGS'])

if os.environ.has_key('CFLAGS'):
    env.Append(CFLAGS = os.environ['CFLAGS'])
    print("\t--> Appending custom CFLAGS : " + os.environ['CFLAGS'])

if os.environ.has_key('LDFLAGS'):
    env.Append(LINKFLAGS = os.environ['LDFLAGS'])
    print("\t--> Appending custom LDFLAGS : " + os.environ['LDFLAGS'])

if os.environ.has_key('PATH'):
    env.Append(PATH = os.environ['PATH'])
    print("\t--> Appending custom PATH : " + os.environ['PATH'])

# SET UP BUILD DIRECTORY TARGET
env['PREFIX'] = GetLaunchDir() + "/build/"
env.Alias('stage', env['PREFIX'])
print("Staging directory: " + env['PREFIX'])

env['INSTALL_LIB_DIR'] = env['PREFIX'] + "/lib"
env['INSTALL_INC_DIR'] = env['PREFIX'] + "/include"
env['INSTALL_BIN_DIR'] = env['PREFIX'] + "/bin"

# ----------------------------
# BUILD INDIVIDUAL DIRECTORIES
# ----------------------------

# Add better depedencies using this techinque: http://www.scons.org/doc/HTML/scons-user/x3255.html#AEN3318
Export('env')
#SConscript('micromanager/SConscript')
SConscript('xenon/SConscript')
#SConscript('radon/SConscript')
