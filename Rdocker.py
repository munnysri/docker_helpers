#! /usr/bin/env python
# this script creates a docker container to run R interactively
import     time
import     csv
import     sys
import     os.path
import     os
import     subprocess
from       argparse import ArgumentParser
from       datetime import datetime, timedelta

# init globals
version='1.0'
msgErrPrefix='>>> Error (' + os.path.basename(__file__) +')'
msgInfoPrefix='>>> Info (' + os.path.basename(__file__) +')'
debugPrefix='>>> Debug (' + os.path.basename(__file__) +')'

# def functions
def pInfo(msg):
    tmsg=time.asctime()
    print msgInfoPrefix+tmsg+": "+msg

def pError(msg):
    tmsg=time.asctime()
    print msgErrPrefix+tmsg+": "+msg

def pDebug(msg):
    if debug:
        tmsg=time.asctime()
        print debugPrefix+tmsg+": "+msg

def Summary(hdr):
    print(hdr)
    print( '\tVersion: ' + version)

    print( '\tDocker:' )
    print( '\t\tUse existing container: ' + str(existingcontainer) )
    print( '\t\tKeep container: ' + str(keepcontainer) )
    print( '\t\tContainer name: ' + name )
    print( '\t\tImage: ' + image )
    print( '\t\tCreate container opts: ' + createopts )
    print( '\t\tBind-mount local dir: ' + localdir )
    print( '\t\tBind-mount docker dir: ' + dockerdir )
    print( '\t\tDatamap: ' + datamap )
    tbegin=time.asctime()
    print( '\tTime: ' + tbegin + "\n" )

defCreateOpts = "-it"
defDockerImage = "uwgac/topmed-rstudio"
defName = "Rdocker"
defDockerDir = "/home/rstudio"
defDataMap = None

# command line parser
parser = ArgumentParser( description = "Helper function to run R in docker" )
parser.add_argument( "-L", "--localdir",
                     help = "full path of local work directory [default: current working directory]" )
parser.add_argument( "-D", "--dockerdir", default = defDockerDir,
                     help = "full path of docker work directory [default: " + defDockerDir +"]" )
parser.add_argument( "-d", "--datamap", default = defDataMap,
                     help = "local data directory map (e.g., /projects/data:/data) [default: " + str(defDataMap) +"]" )
parser.add_argument( "-I", "--image", default = defDockerImage,
                     help = "docker image to initiate pipeline execution [default: " + defDockerImage + "]")
parser.add_argument( "-c", "--createopts", default = defCreateOpts,
                     help = "docker create container options [default: " + defCreateOpts + "]")
parser.add_argument( "-e","--existingcontainer", action="store_true", default = False,
                     help = "start an existing container [default: False]" )
parser.add_argument( "-n","--name", default = defName,
                     help = "name of container [default: " + defName + "]" )
parser.add_argument( "-k", "--keepcontainer", action="store_true", default = False,
                     help = "Keep the container and do not stop it [default: False]" )
parser.add_argument( "-V", "--verbose", action="store_true", default = False,
                     help = "Turn on verbose output [default: False]" )
parser.add_argument( "-S", "--summary", action="store_true", default = False,
                     help = "Print summary prior to executing [default: False]" )
parser.add_argument( "--version", action="store_true", default = False,
                     help = "Print version of " + __file__ )

args = parser.parse_args()
# set result of arg parse_args
localdir = args.localdir
dockerdir = args.dockerdir
datamap = args.datamap
image = args.image
createopts = args.createopts
existingcontainer = args.existingcontainer
name = args.name
keepcontainer = args.keepcontainer
verbose = args.verbose
summary = args.summary
# version
if args.version:
    print(__file__ + " version: " + version)
    sys.exit()

if not keepcontainer:
    createopts = createopts + " --rm"
# if not using existing container, then process all the args
if not existingcontainer:
    # check localdir; if not passed using cwd
    if localdir == None:
        localdir = os.getenv('PWD')
    # check if datamap is specified
    if datamap == None:
        dockermap = ""
    else:
        if len(datamap.split(":")) == 2:
            dockermap = " -v " + datamap
        else:
            pError("Datamap (" + datamap + ") must be specified as lll:ddd")
            sys.exit(2)
else:
    localdir = "N/A"
    dockerdir = "N/A"
    image = "N/A"
    createopts = "N/A"
# summarize and check for required params
if summary or verbose:
    Summary("Summary of " + __file__)
    if summary:
        sys.exit()
print("=====================================================================")
pInfo("\n\tRunning R in docker image: " + image)
print("=====================================================================")
# create container
if not existingcontainer:
    createCMD = "docker create " + createopts + " --name " + name + \
                " -v " + localdir + ":" + dockerdir + dockermap + \
                " -w " + dockerdir + \
                " " + image + " R"
    if verbose:
        pInfo("Docker create container cmd:\n" + createCMD)
    process = subprocess.Popen(createCMD, shell=True, stdout=subprocess.PIPE)
    status = process.wait()
    pipe = process.stdout
    msg = pipe.readline()
    if status:
        pError("Docker create command failed: " + msg )
        sys.exit(2)
# just use existing container
else:
    if verbose:
        pInfo("Use existing container named: " + name)

# start the container
startCMD = "docker start -i " + name
if verbose:
    pInfo("Docker start cmd: " + startCMD)
process = subprocess.Popen(startCMD, stdout=sys.stdout, stderr=sys.stderr, shell=True)
status = process.wait()
if status:
    pError("Docker start command failed:\n\t" + str(status) )
    sys.exit(2)

if verbose:
    pInfo("Python script " + __file__ + " completed without errors")
