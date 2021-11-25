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
    from runner import My_Simulation

    s: My_Simulation = My_Simulation(traci)

    step = 0
    while step < 500:
        traci.simulationStep()
        step += 1

    print(s.get_all_bus())
    print(s.get_all_bus_stops())

    traci.close()


class My_Simulation:
    def __init__(self, traci):
        self.traci = traci

    all_bus_stop_simulation = []
    all_bus_simulation = []
    all_bus_simulation_running = []

    def get_all_bus_stops(self):  # retorna todas as paradas de onibus
        self.all_bus_stop_simulation = self._sort_bus_stops_by_name(
            self.traci.busstop.getIDList())
        return self.all_bus_stop_simulation

    def get_all_bus(self):
        self.all_bus_stop_simulation = sorted(
            self.traci.vehicle.getIDList(), key=lambda x: int(x.split(".")[1]))
        return self.all_bus_stop_simulation

    # metodos privados
    def _sort_bus_stops_by_name(self, bus_stops_ids):
        row = len(bus_stops_ids)
        col = 2
        array_2d = [[0 for j in range(col)] for i in range(row)]

        i = 0
        for bus in bus_stops_ids:
            array_2d[i][0] = bus
            array_2d[i][1] = self.traci.busstop.getName(bus).split("p")[1]
            i += 1

        # ordenar as paradas pelo nome
        array_2d.sort(key=lambda x: (int(x[1]), int(x[0])))

        return array_2d
