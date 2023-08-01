import mmh3


class ConsistentHashRing(object):
    def __init__(self, replicas=3, nodes=None, ):
        self.replicas = replicas
        self.ring = dict()
        self._sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)
        self.nodes = nodes

    def add_node(self, node):
        """
        Adds a `node` to the hash ring (including a number of replicas)
        """
        for i in range(self.replicas):
            virtual_node = f"{node}#{i}"
            key = self.gen_key(virtual_node)
            self.ring[key] = node

            # print(self.ring)
            # print(self._sorted_keys)

            self._sorted_keys.append(key)
            # print(f"{virtual_node} --> {key} --> {node}")

        self._sorted_keys.sort()
        # print(self.ring)
        # print(self._sorted_keys)
        # print([self.ring[key] for key in self._sorted_keys])

    def remove_node(self, node):
        """
        Removes `node` from the hash ring and its replicas
        """
        for i in range(self.replicas):
            key = self.gen_key(f"{node}#{i}")
            del self.ring[key]
            self._sorted_keys.remove(key)

    def get_node(self, string_key):
        """
        Given a string key a corresponding node in the hash ring is returned.

        If the hash ring is empty, `None` is returned.
        """
        return self.get_node_pos(string_key)[0]

    def get_node_pos(self, string_key):
        """
        Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring.

        If the hash ring is empty, (`None`, `None`) is returned.
        """
        if not self.ring:
            return None, None

        key = self.gen_key(string_key)
        nodes = self._sorted_keys
        for i in range(len(nodes)):
            node = nodes[i]
            if key < node:
                return self.ring[node], i

        # 如果key > node，那么让这些key落在第一个node上就形成了闭环
        return self.ring[nodes[0]], 0

    def gen_key(self, string_key):
        """
        Given a string key it returns a long value, this long value represents
        a place on the hash ring
        """
        return mmh3.hash(string_key, 32, signed=False)


if __name__ == '__main__':
    """
    # 第一次 
    [obj=a][target_node=1.1.1.4:9090]
    [obj=b][target_node=1.1.1.1:9090]
    [obj=c][target_node=1.1.1.1:9090]
    [obj=d][target_node=1.1.1.4:9090]
    [obj=e][target_node=1.1.1.1:9090]
    [obj=f][target_node=1.1.1.2:9090]

    # 第二次， 1节点下线
    [obj=a][target_node=1.1.1.4:9090]
    [obj=b][target_node=1.1.1.4:9090]
    [obj=c][target_node=1.1.1.4:9090]
    [obj=d][target_node=1.1.1.4:9090]
    [obj=e][target_node=1.1.1.3:9090]
    [obj=f][target_node=1.1.1.2:9090]
    
    # 第三次，1上线，4下线
    [obj=a][target_node=1.1.1.1:9090]
    [obj=b][target_node=1.1.1.1:9090]
    [obj=c][target_node=1.1.1.1:9090]
    [obj=d][target_node=1.1.1.3:9090]
    [obj=e][target_node=1.1.1.1:9090]
    [obj=f][target_node=1.1.1.2:9090]
    """
    nodes = [
        "1.1.1.1:9090",
        "1.1.1.2:9090",
        "1.1.1.3:9090",
        "1.1.1.4:9090",
    ]

    # 分片数 3
    c = ConsistentHashRing(3, nodes)
    # c = ConsistentHashRing(500, nodes)

    objs = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
    ]
    for i in objs:
        target_node = c.get_node(i)
        msg = "[obj={}][target_node={}]".format(
            i,
            target_node
        )
        print(msg)
