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
from MyReport import MyReport

no_gui = True


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=no_gui, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


if __name__ == "__main__":

    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]

    traci.start(sumo_cmd)

    simulation: MySimulation = MySimulation(traci)
    report: MyReport = MyReport("report.csv")
    step = 0
    while step <= 1000:
        traci.simulationStep()
        if(step % 60 == 0):
            simulation.change_max_speed_bus(
                10.0, 0.1, ['flow_bombeiros-ufsm.1', 'flow_bombeiros-ufsm.3', 'flow_bombeiros-ufsm.5', 'flow_bombeiros-ufsm.7'])
            simulation.get_all_people_on_simulation_buses(step)
        step += 1
    report.write_file(simulation.get_report_person_by_bus())
    # print(report.get_head_register_csv(50))
    # print(report.get_tail_register_csv(50))
    # print(report.get_value_counts("bus_id"))
    # print(report.get_shape())
    # print(report.get_info())
    # print(report.get_describe())

    report2 = MyReport("report2.csv")
    print(report.get_group_mean("bus_id", "step_log"))

    traci.close()
