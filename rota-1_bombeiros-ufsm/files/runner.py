from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa

import traci

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
        
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumoCmd = [sumoBinary, "-c", "osm.sumocfg"]
    
    traci.start(sumoCmd)
    
    busstops = traci.busstop.getIDList()
    
    step = 0
    while step < 1000:
        traci.simulationStep()
        
        for i in busstops:
           
            if(traci.busstop.getPersonCount(i)>0):
                print("busStopId:" + i + 
                    " name:" + str(traci.busstop.getName(i)) +
                    " pessoas na parada:" + str(traci.busstop.getPersonCount(i))
                    )
            
                 
        step += 1
    traci.close()


    
     
