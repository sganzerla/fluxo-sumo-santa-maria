from __future__ import absolute_import
from __future__ import print_function
import optparse
import os
import sys
import requests as request
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
no_gui = False


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


def convert_in_matrix_3d(matrix_multi):
    matrix = []
    for x in matrix_multi:
        for y in x:
            matrix.append(y)
    return matrix




        # request.patch(url_api_base + '/bus_stops/' +
        #               i[0], data={'people_on_bus': count})


if __name__ == "__main__":

    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    sumo_cmd = [sumoBinary, "-c", "osm.sumocfg"]

    traci.start(sumo_cmd)
    simulation: MySimulation = MySimulation(traci)
    header_name_columns = ['bus_id', 'people_on_bus', 'step_log']
    report: MyReport = MyReport(header_name_columns)
    step = 0
    buses_to_delay = ['flow_bombeiros-ufsm.2', 'flow_bombeiros-ufsm.4',
                      'flow_bombeiros-ufsm.6', 'flow_bombeiros-ufsm.8']
    bus_stops_list = simulation.get_all_bus_stops()

    while step <= 5200:
        traci.simulationStep()
        # log de pessoas em todas as paradas a cada 10 passos
        if(step % 10 == 0):
            simulation.log_count_people_in_bus_stop(bus_stops_list)
        # a partir de 1800 passos inicio o delay em alguns onibus
        if(step > 1800):
            simulation.change_max_speed_bus(
                speed=20.0, accel=0.1, bus_ids_delay=buses_to_delay, color=(255, 0, 0))
        # log de pessoas nos ônibus a cada 600 passos
        if(step % 600 == 0):
            simulation.get_all_people_on_simulation_buses(step)
        step += 1

    dataset = convert_in_matrix_3d(simulation.get_report_person_by_bus())
    dataset_rearranged = map(reorder_strings_as_integers, dataset)
    traci.close()

    report.write_file(dataset_rearranged)

    group_columns = ['bus_id']
    select_columns = ['people_on_bus']
    functions_pandas = ['mean', 'count', 'std', 'min', 'max']
    report.extract_information(
        columns_to_group_by=group_columns,
        columns_to_select_by=select_columns,
        functions_name_pandas=functions_pandas,
        print_log=True,
        show_plot=True,
        create_file=True,
        kind_plot_name='bar'
    )
