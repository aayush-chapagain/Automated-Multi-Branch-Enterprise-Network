# Dijkstra's Shortest Path Algorithm
# Applied to Enterprise Network Topology
import heapq
import pymysql

class EnterpriseNetwork:
    def __init__(self):
        self.graph = {
            'HQ-CR1': {'HQ-CR2': 1, 'HQ-DSW1': 1, 'HQ-DSW2': 1, 'HQ-DSW3': 1, 'HQ-DSW4': 1, 'A-CR1': 10},
            'HQ-CR2': {'HQ-CR1': 1, 'HQ-DSW1': 1, 'HQ-DSW2': 1, 'HQ-DSW3': 1, 'HQ-DSW4': 1, 'B-CR1': 10},
            'A-CR1': {'HQ-CR1': 10, 'A-DSW1': 1, 'A-DSW2': 1},
            'B-CR1': {'HQ-CR2': 10, 'B-DSW1': 1, 'B-DSW2': 1},
            'HQ-DSW1': {'HQ-CR1': 1, 'HQ-CR2': 1, 'HQ-DSW2': 1},
            'HQ-DSW2': {'HQ-CR1': 1, 'HQ-CR2': 1, 'HQ-DSW1': 1},
            'HQ-DSW3': {'HQ-CR1': 1, 'HQ-CR2': 1, 'HQ-DSW4': 1},
            'HQ-DSW4': {'HQ-CR1': 1, 'HQ-CR2': 1, 'HQ-DSW3': 1},
            'A-DSW1': {'A-CR1': 1, 'A-DSW2': 1},
            'A-DSW2': {'A-CR1': 1, 'A-DSW1': 1},
            'B-DSW1': {'B-CR1': 1, 'B-DSW2': 1},
            'B-DSW2': {'B-CR1': 1, 'B-DSW1': 1},
        }

    def dijkstra(self, source, destination):
        pq = [(0, source)]
        distances = {node: float('inf') for node in self.graph}
        distances[source] = 0
        previous = {node: None for node in self.graph}
        visited = set()

        while pq:
            current_cost, current_node = heapq.heappop(pq)
            if current_node in visited:
                continue
            visited.add(current_node)
            if current_node == destination:
                break
            for neighbor, weight in self.graph[current_node].items():
                cost = current_cost + weight
                if cost < distances[neighbor]:
                    distances[neighbor] = cost
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (cost, neighbor))

        path = []
        node = destination
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()

        return {'path': path, 'cost': distances[destination]}

    def save_to_db(self, source, destination, path, cost):
        conn = pymysql.connect(
            host='localhost', user='netadmin',
            password='cisco123', database='enterprise_network'
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO monitoring_logs (device_id, metric_type, metric_value)
            VALUES (1, %s, %s)
        """, (f'path_{source}_to_{destination}', ' -> '.join(path)))
        conn.commit()
        conn.close()

    def run(self):
        print("=" * 60)
        print("Enterprise Network - Dijkstra's Shortest Path Algorithm")
        print("=" * 60)

        pairs = [
            ('HQ-CR1', 'A-CR1'),
            ('HQ-CR1', 'B-CR1'),
            ('A-CR1', 'B-CR1'),
            ('HQ-DSW1', 'A-DSW1'),
            ('HQ-DSW1', 'B-DSW1'),
        ]

        for source, destination in pairs:
            result = self.dijkstra(source, destination)
            path_str = ' -> '.join(result['path'])
            print(f"\nSource     : {source}")
            print(f"Destination: {destination}")
            print(f"Path       : {path_str}")
            print(f"Cost       : {result['cost']} hops")
            self.save_to_db(source, destination, result['path'], result['cost'])

        print("\n" + "=" * 60)
        print("All paths saved to MySQL database!")
        print("=" * 60)

if __name__ == '__main__':
    network = EnterpriseNetwork()
    network.run()
