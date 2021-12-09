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


def concatenate_zeros_when_less_than_100(itemCol):
    text = itemCol.split('.')[0]
    number = itemCol.split('.')[1]
    if(number.__len__() == 1):
        return text + ".00" + str(number)
    else:
        if(number.__len__() == 2):
            return text + ".0" + str(number)
    return itemCol


def reorder_strings_as_integers(col):
    return (concatenate_zeros_when_less_than_100(col[0]), col[1], col[2])

def format_in_3dimensional_array(matrix_multi_dimension):

    matriz3d = []
    for x in matrix_multi_dimension:
        for y in x:
            matriz3d.append(y)
    
    return matriz3d

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
    while step <= 8500:
        traci.simulationStep()
        if(step % 600 == 0):
            #if(step > 2000):
            #        simulation.change_max_speed_bus(
            #        20.0, 0.1, ['flow_bombeiros-ufsm.1', 'flow_bombeiros-ufsm.3', 'flow_bombeiros-ufsm.5', 'flow_bombeiros-ufsm.7'])
            simulation.get_all_people_on_simulation_buses(step)
        step += 1

    dataset = format_in_3dimensional_array(simulation.get_report_person_by_bus())

    dataset_rearranged = map(reorder_strings_as_integers, dataset)

    report.write_file(dataset_rearranged)
    response = report.get_group_mean("bus_id", "step_log")
    print("Media de pessoas por ônibus e intervalo de tempo: \n")
    print(response)
    print("-------------------")
    response2 = report.get_group_mean("bus_id")
    print("Media de pessoas por ônibus: \n")
    print(response2)

    # print(report.get_head_register_csv(50))
    # print(report.get_tail_register_csv(50))
    # print(report.get_value_counts("bus_id"))
    # print(report.get_shape())
    # print(report.get_info())
    # print(report.get_describe())

    traci.close()
