from __future__ import absolute_import
from __future__ import print_function

import optparse
import os
import sys

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa

import traci


def no_gui():
    return True


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=no_gui(), help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


def order_bus_stop_by_name():
    row = len(bus_stops_ids)
    col = 2
    order_bus_stops_by_name = [[0 for j in range(col)] for i in range(row)]

    i = 0
    for bus in bus_stops_ids:
        order_bus_stops_by_name[i][0] = bus
        order_bus_stops_by_name[i][1] = traci.busstop.getName(bus).split("p")[1]
        i += 1

    # ordenar as paradas pelo nome
    order_bus_stops_by_name.sort(key=lambda x: (int(x[1]), int(x[0])))

    return order_bus_stops_by_name


def print_persons_in_bus(step_value, bus_speed):
    all_bus = get_all_bus_ids()
    txt = str(step_value)
    for bus in all_bus:
        if traci.vehicle.getTypeID(bus) == "bus":
            if bus == "flow_bombeiros-ufsm.2" or bus == "flow_bombeiros-ufsm.3" or bus == "flow_bombeiros-ufsm.4":
                traci.vehicle.setSpeed(bus, bus_speed)

        txt += ", " + str(traci.vehicle.getPersonNumber(bus))

    print(txt)
    return txt + "\n"


def get_all_bus_ids():
    all_bus = traci.vehicle.getIDList()
    return all_bus


def print_persons_in_bus_stop(step_value):
    txt = "busStops " + str(step_value)
    aux = 0
    for i in ordered_bus_stops:
        if 5 <= aux <= 30:
            # txt += " busStopName: " + \
            txt += " " + \
                   str(traci.busstop.getName(
                       # i[0])) + " personCount: " + str(traci.busstop.getPersonCount(i[0]))
                       i[0])) + " : " + str(traci.busstop.getPersonCount(i[0]))
        aux += 1

    print(txt)


if __name__ == "__main__":

    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]

    traci.start(sumo_cmd)

    bus_stops_ids = traci.busstop.getIDList()

    ordered_bus_stops = order_bus_stop_by_name()

    # traci.trafficlight.setPhaseDuration("GS_637770324", 200)

    newFile = open("bus_persons20.csv", "w")
    step = 0
    while step <= 2000:
        traci.simulationStep()

        if step % 50 == 0:
            newFile.write(print_persons_in_bus(step, 20.0))

        step += 1
    newFile.seek(0)
    head_bus_ids = ""
    aux = 0
    for i in get_all_bus_ids():
        aux += 1
        is_last_item = aux == len(get_all_bus_ids())
        head_bus_ids += i + (", " if not is_last_item else "")

    newFile.write("step," + head_bus_ids + "\n")
    newFile.close()

    traci.close()
