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

def orderBusStopByName(busstops):
    row = len(busstops)
    col = 2
    orderBusStops = [[0 for j in range(col)] for i in range(row)]
    
    i=0
    for bus in busstops:
        orderBusStops[i][0] = bus
        orderBusStops[i][1] = traci.busstop.getName(bus).split("p")[1]
        i+=1
    
    # for b in orderBusStops:
    #     print(b[0],b[1])
    # ordenar as paradas pelo nome
    orderBusStops.sort(key=lambda x: (int(x[1]), int(x[0])))
  
    # for b in orderBusStops:
    #     print(b[0],b[1])
    return orderBusStops

def getBus(step):
    allBus = traci.vehicle.getIDList()
    txt = "step: " + str(step)
    for bus in allBus:
        if traci.vehicle.getTypeID(bus) == "bus":
            # concatenar e printar numa linha unica
            txt += " bus: " + bus + " personNumber: " + str(traci.vehicle.getPersonNumber(bus))
           
    print(txt)
        
    

if __name__ == "__main__":
        
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumoCmd = [sumoBinary, "-c", "osm.sumocfg"]
    
    traci.start(sumoCmd)
    
    busstops = traci.busstop.getIDList()
    
    orderBusStops = orderBusStopByName(busstops)
        
    step = 0
    while step <= 1000:
        traci.simulationStep()
        
        # for i in orderBusStops:
           
        #     # if(traci.busstop.getPersonCount(i[0])>0):
        #         print(
        #             "step: " + str(step) + "    " +
        #             "busStopName: " + str(traci.busstop.getName(i[0])) + "    " +
        #             "busStopId: " + i[0] + "    " +
        #             "countPersons: " + str(traci.busstop.getPersonCount(i[0])) + "    " +
        #             ""
        #             )
                
        if (step % 50 == 0):    
            getBus(step)
                 
        step += 1
        
    traci.close()


    
     
