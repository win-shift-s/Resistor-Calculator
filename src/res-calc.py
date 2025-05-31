class Resistor:
    def __init__(self, label: str, node_a: str, node_b: str, resistance: str) -> None:
        self.label = label
        self.src = node_a
        self.dest = node_b
        self.res = int(resistance)

    def __str__(self) -> str:
        return f'{self.label}: {self.src.label} {self.dest.label} ({self.res})'

class Circuit:
    def __init__(self, num_resistors: int, nodes: list) -> None:
        self.num_res = num_resistors
        self.num_nodes = len(nodes)
        self.adj_list = {}
        for node in nodes:
            self.adj_list[node] = []

    def __str__(self) -> str:
        return f'adjacency list: {self.adj_list}'

    def add_resistor(self, resistor: Resistor) -> None:
        self.adj_list[resistor.src].append(resistor)
        self.adj_list[resistor.dest].append(resistor)

    def parallel(self, res_a: Resistor, res_b: Resistor) -> bool:
        if (res_a.src == res_b.src or res_a.src == res_b.dest) and (res_a.dest == res_b.src or res_a.dest == res_b.dest):
            return True
        else:
            return False

    def calculate_parallel(self, res_a, res_b) -> int:
        return (res_a * res_b) / (res_a + res_b)

    def series(self, res_a: Resistor, res_b: Resistor, path=[]) -> list:
        start = res_a.dest
        end = res_b.src
        path = path + [start]
        if len(self.adj_list[start]) == 2:
            if start == end:
                return path
            try:
                for resistor in self.adj_list[start]:
                    next_node = resistor.dest
                    if next_node not in path:
                        return self.series(resistor, res_b, path)
            except:
                return True

    def series_or_parallel(self, res_a: Resistor, res_b: Resistor) -> str:
        if self.parallel(res_a, res_b) == True:
            return 'PARALLEL'
        elif self.series(res_a, res_b):
            return 'SERIES'
        else:
            return 'NEITHER'

    def connections(self, res_list) -> list:
        parallel = []
        parallel_sum = 0
        series = []
        series_sum = 0
        connected = []
        while res_list:
            current_resistor = res_list.pop(0)
            current_res = current_resistor.label
            for resistor in res_list:
                res = resistor.label
                if res not in connected:
                    connection = self.series_or_parallel(current_resistor, resistor)
                    if connection == 'PARALLEL':
                        if current_res in parallel and res not in parallel:
                            parallel.append(res)
                            parallel_sum = self.calculate_parallel(parallel_sum, resistor.res)
                        elif current_res not in parallel:
                            parallel.append(current_res)
                            parallel.append(res)
                            parallel_sum = self.calculate_parallel(current_resistor.res, resistor.res)
                        connected.append(res)
                    elif connection == 'SERIES':
                        if current_res in series and res not in series:
                            series_sum += resistor.res
                            series.append(res)
                        elif current_res not in series:
                            series_sum = current_resistor.res + resistor.res
                            series.append(current_res)
                            series.append(res)
                        connected.append(res)
        parallel.sort()
        series.sort()
        return [parallel, int(parallel_sum)], [series, int(series_sum)]

if __name__ == '__main__':
    n = int(input())

    node_list = []
    resistor_list = {}

    for resistor in range(n):
        label, node_a, node_b, resistance = [x for x in input().split()]
        if node_a not in node_list:
            node_list.append(node_a)
        if node_b not in node_list:
            node_list.append(node_b)
        resistor_list[label] = Resistor(label, node_a, node_b, resistance)

    num_res = len(resistor_list)
    circuit = Circuit(num_res, node_list)
    for resistor in resistor_list.values():
        circuit.add_resistor(resistor)

    groups = sorted(circuit.connections([*resistor_list.values()]), key=lambda x:(x, str.casefold))
    first = groups[0][0]
    second = groups[1][0]
    if first:
        first_list = ', '.join(first)
        print(f'[{first_list}] {groups[0][1]}')
    if second:
        second_list = ', '.join(second)
        print(f'[{second_list}] {groups[1][1]}')

'''
References:
- https://colab.research.google.com/drive/1st36PdGYt3yGefdThVqxTpOuhMz8E19I?usp=sharing
- https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
- https://docs.python.org/3/tutorial/datastructures.html#dictionaries
- https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
- answer by zwol from https://stackoverflow.com/questions/4581646/how-to-count-all-elements-in-a-nested-dictionary
'''