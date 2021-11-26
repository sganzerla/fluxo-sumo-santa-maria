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
from MySimulation import MySimulation

no_gui = True


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=no_gui, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


def get_count_persons_in_bus(bus_speed: int):
    txt = ""
    for bus in get_all_bus_ids():
        if traci.vehicle.getTypeID(bus) == "bus":
            if bus == "flow_bombeiros-ufsm.2" or bus == "flow_bombeiros-ufsm.3" or bus == "flow_bombeiros-ufsm.4":
                traci.vehicle.setSpeed(bus, bus_speed)

        txt += ", " + bus + ":" + str(traci.vehicle.getPersonNumber(bus))
    return txt


# def print_persons_in_bus_stop(step_value):
#     txt = "busStops " + str(step_value)
#     aux = 0
#     for i in ordered_bus_stops:
#         if 5 <= aux <= 30:
#             # txt += " busStopName: " + \
#             txt += " " + \
#                    str(traci.busstop.getName(
#                        # i[0])) + " personCount: " + str(traci.busstop.getPersonCount(i[0]))
#                        i[0])) + " : " + str(traci.busstop.getPersonCount(i[0]))
#         aux += 1

#     print(txt)


def generate_report_header():
    head_bus_ids = ""
    aux = 0
    amount_bus = len(get_all_bus_ids())
    while aux < amount_bus:
        head_bus_ids += "bus_" + str(aux) + ","
        aux += 1

    head_bus_ids += "bus_" + str(amount_bus)

    return head_bus_ids


def generate_simulation_with_change_speed_bus(new_speed: int, total_time_in_seconds: int, time_interval_between_logs: int):
    new_file = open("./dist/bus_persons_change_speed_" + str(new_speed) +
                    "_km_in_" + str(total_time_in_seconds) + "_steps.csv", "w")
    step = 0
    while step <= total_time_in_seconds:
        traci.simulationStep()

        if step % time_interval_between_logs == 0:
            new_file.write(
                str(step) + get_count_persons_in_bus(new_speed) + "\n")

        step += 1

    head_bus_ids = generate_report_header()

    new_file.write("step," + head_bus_ids + "\n")
    new_file.close()


if __name__ == "__main__":

    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]

    traci.start(sumo_cmd)

    # ordered_bus_stops = order_bus_stop_by_name()

    # generate_simulation_with_change_speed_bus(
    #     new_speed=50,
    #     total_time_in_seconds=3600,
    #     time_interval_between_logs=60
    # )

    simulation = MySimulation(traci)

    step = 0
    while step < 2000:
        traci.simulationStep()
        if(step % 100 == 0):
            # simulation.change_bus_speed(
            #     10.0, ['flow_bombeiros-ufsm.1', 'flow_bombeiros-ufsm.3', 'flow_bombeiros-ufsm.5', 'flow_bombeiros-ufsm.7'])
            print(str(step) + '-' + str(simulation.get_all_bus()))
            print(str(step) + '-' + str(simulation.get_all_people_on_bus()))
        step += 1

    # print(simulation.all_bus_stops)

    traci.close()
