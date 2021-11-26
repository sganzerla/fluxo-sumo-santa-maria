class MySimulation:

    def __init__(self, traci_instance):
        self.traci = traci_instance
        self.all_bus_stops = self.get_all_bus_stops()
        self.all_buses_simulation = []
        self.all_buses_circulation = []

    def get_all_bus_stops(self):
        all_bus_stop = self.traci.busstop.getIDList()
        return self._sort_bus_stop_by_name(all_bus_stop)

    def get_all_bus(self):
        all_bus = self.traci.vehicle.getIDList()
        return self._sort_bus_by_name(all_bus)

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

    def _sort_bus_by_name(self, bus_ids):
        row = len(bus_ids)
        col = 2
        array_2d = [[0 for j in range(col)] for i in range(row)]

        i = 0
        for bus in bus_ids:
            array_2d[i][0] = bus
            array_2d[i][1] = bus.split(".")[1]
            i += 1

        array_2d.sort(key=lambda x: (int(x[1]), (x[0])))

        return array_2d
