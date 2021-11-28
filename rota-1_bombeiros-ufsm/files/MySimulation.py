class MySimulation:

    def __init__(self, traci_instance):
        self.traci = traci_instance
        self.people_on_each_bus_all_simulation = []

    def get_all_bus_stops(self):
        all_bus_stop = self.traci.busstop.getIDList()
        return self._sort_bus_stop_by_name(all_bus_stop)

    def get_all_bus(self):
        all_vehicles = self.traci.vehicle.getIDList()
        return self._sort_bus_by_name(self._filter_once_buses(all_vehicles))

    def get_all_people_on_simulation_buses(self, total_step: int, step_interval: int):
        step = 0
        self.people_on_each_bus_all_simulation = []
        while step <= total_step:
            self.traci.simulationStep()
            if step % step_interval == 0:
                self._get_all_people_on_bus_by_interval_step(step)
            step += 1

        list_of_people_by_bus = []
        for all_people_each_interval in self.people_on_each_bus_all_simulation:
            for people_each_bus in all_people_each_interval:
                list_of_people_by_bus.append(people_each_bus)

        return list_of_people_by_bus

    def change_max_speed_bus(self, speed: float, accel: float,  bus_id: list[str]):
        buses = self.get_all_bus()
        for bus in buses:
            if bus[0] in bus_id:
                self.traci.vehicle.setMaxSpeed(bus[0], speed)
                self.traci.vehicle.setColor(bus[0], (255, 0, 242))
                self.traci.vehicle.setAccel(bus[0], accel)

    # metodos privados

    def _get_all_people_on_bus_by_interval_step(self, step):
        buses = self.get_all_bus()
        row = len(buses)
        col = 3
        all_people_on_bus_by_step = [[0 for j in range(col)] for i in range(row)]
        i = 0
        for bus in buses:
            all_people_on_bus_by_step[i][0] = bus[0]
            all_people_on_bus_by_step[i][1] = self.traci.vehicle.getPersonNumber(
                bus[0])
            all_people_on_bus_by_step[i][2] = step
            self.people_on_each_bus_all_simulation.append(all_people_on_bus_by_step)
            i += 1

        return all_people_on_bus_by_step

    def _sort_bus_stop_by_name(self, bus_stops_ids):
        row = len(bus_stops_ids)
        col = 2
        array_2d = [[0 for j in range(col)] for i in range(row)]

        i = 0
        for bus in bus_stops_ids:
            array_2d[i][0] = bus
            array_2d[i][1] = self.traci.busstop.getName(bus).split("p")[1]
            i += 1

        array_2d.sort(key=lambda x: (int(x[1]), int(x[0])))

        return array_2d

    def _sort_bus_by_name(self, vehicle_ids):
        row = len(vehicle_ids)
        col = 2
        array_2d = [[0 for j in range(col)] for i in range(row)]

        i = 0
        for bus in vehicle_ids:
            array_2d[i][0] = bus
            array_2d[i][1] = bus.split(".")[1]
            i += 1

        array_2d.sort(key=lambda x: (int(x[1]), (x[0])))

        return array_2d

    def _filter_once_buses(self, vehicle_ids):
        filtered = []
        for v in vehicle_ids:
            if self.traci.vehicle.getTypeID(v) == "bus":
                filtered.append(v)
        return filtered
