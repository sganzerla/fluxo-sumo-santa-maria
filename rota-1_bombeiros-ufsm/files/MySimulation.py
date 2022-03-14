from sys import modules
import requests

class MySimulation:

    def __init__(self, traci_instance: modules, url_api_base):
        self.traci: modules = traci_instance
        self.people_on_each_bus_all_simulation: list = []
        self.url_api_base = url_api_base

    def get_report_person_by_bus(self):
        return self.people_on_each_bus_all_simulation

    def get_all_bus_stops(self):
        all_bus_stop: list[str] = self.traci.busstop.getIDList()
        return self._sort_bus_stop_by_name(all_bus_stop)

    def get_all_bus(self):
        all_vehicles: list[str] = self.traci.vehicle.getIDList()
        return self._sort_bus_by_name(self._filter_only_buses(all_vehicles))

    def get_all_people_on_simulation_buses(self, step: int):
        self._get_all_people_on_bus_by_interval_step(step)

    def change_max_speed_bus(self, speed: float, accel: float, bus_ids_delay, color):
        buses = self.get_all_bus()
        for bus in buses:
            if bus[0] in bus_ids_delay:
                self.traci.vehicle.setMaxSpeed(bus[0], speed)
                self.traci.vehicle.setAccel(bus[0], accel)
                self.traci.vehicle.setColor(bus[0], color)

    # metodos privados
    # pega todas as pessoas que estão nos veículos rodando na simulação naquele instante
    def _get_all_people_on_bus_by_interval_step(self, step):
        buses = self.get_all_bus()
        row = len(buses)
        col = 3
        all_people_on_bus_by_step = [[0 for j in range(col)] for i in range(row)]
        i = 0
        for bus in buses:
            all_people_on_bus_by_step[i][0] = bus[0]
            all_people_on_bus_by_step[i][1] = self.traci.vehicle.getPersonNumber(bus[0])
            all_people_on_bus_by_step[i][2] = step
            # adiciona lista daquele instante na lista de todas as pessoas que estão nos veículos rodando na simulação
            i += 1

        self.people_on_each_bus_all_simulation.append( all_people_on_bus_by_step)
        return all_people_on_bus_by_step

    def _sort_bus_stop_by_name(self, bus_stops_ids: list):
        row: int = len(bus_stops_ids)
        col: int = 2
        bus_stop_list_to_sort: list[str] = [
            [0 for j in range(col)] for i in range(row)]

        i = 0
        for bus_stop in bus_stops_ids:
            bus_stop_list_to_sort[i][0] = bus_stop
            bus_stop_list_to_sort[i][1] = self.traci.busstop.getName(bus_stop).split("p")[
                1]
            i += 1

        bus_stop_list_to_sort.sort(key=lambda x: (int(x[1]), int(x[0])))

        return bus_stop_list_to_sort

    def _sort_bus_by_name(self, vehicle_ids: list):
        row: int = len(vehicle_ids)
        col: int = 2
        array_2d: list = [
            [0 for j in range(col)] for i in range(row)]

        i = 0
        for bus in vehicle_ids:
            array_2d[i][0] = bus
            array_2d[i][1] = bus.split(".")[1]
            i += 1

        array_2d.sort(key=lambda x: (int(x[1]), (x[0])))

        return array_2d

    def _filter_only_buses(self, vehicle_ids):
        filtered: list = []
        for vehicle in vehicle_ids:
            if self.traci.vehicle.getTypeID(vehicle) == "bus":
                filtered.append(vehicle)
        return filtered
