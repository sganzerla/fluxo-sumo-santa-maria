class MySimulation:

    def __init__(self, traci_instance):
        self.traci = traci_instance
        self.all_bus_stops = self.get_all_bus_stops()
        self.all_buses_simulation = []
        self.all_buses_circulation = []
        self.all_people_on_bus = []

    def get_all_bus_stops(self):
        all_bus_stop = self.traci.busstop.getIDList()
        return self._sort_bus_stop_by_name(all_bus_stop)

    def get_all_bus(self):
        all_vehicles = self.traci.vehicle.getIDList()
        return self._sort_bus_by_name(self._filter_once_buses(all_vehicles))

    def get_all_people_on_bus(self):
        buses = self.get_all_bus()
        row = len(buses)
        col = 2
        array_2d = [[0 for j in range(col)] for i in range(row)]
        i = 0
        for bus in self.get_all_bus():
            array_2d[i][0] = bus[0]
            array_2d[i][1] = self.traci.vehicle.getPersonNumber(
                bus[0])
            i += 1
        return array_2d

    # metodos privados

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
            if (self.traci.vehicle.getTypeID(v) == "bus"):
                filtered.append(v)
        return filtered
