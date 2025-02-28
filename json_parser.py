import numpy as np
class JSONGraph:

    def __init__(self, js: dict):
        self.js = js
        self.roots = list(js.keys())
        queue = [self.add_vert(item, None) for item in self.roots]

        endpoints = {}
        endpoint_parents = {}
        while len(queue) > 0:
            node = queue.pop(0)
            node_path = node.get_path()
            node_val = self.get_item(js, node_path)
            #Handling endpoints
            if type(node_val) == dict:
                children = node_val.keys()
                for child in children:
                    queue.append(self.add_vert(child, node))                
            elif type(node_val) == list:
                for ind, item in enumerate(node_val):
                    if type(item) == dict:
                        children = item.keys()
                        for child in children:
                            queue.append(self.add_vert([ind, child], node))
                    else: 
                        endpoint = self.add_endpoint([ind, item], node)
                        endpoints[endpoint] = node_val         
            else:
                endpoint = self.add_endpoint(node_val, node)
                endpoints[endpoint] = node_val
        self.endpoints = endpoints
        return

    def add_vert(self, name, parent: "JSONVertex | None") -> "JSONVertex":
        return JSONVertex(name, parent)

    def add_endpoint(self, value: any, parent: "JSONVertex") -> "JSONEndpoint":
        return JSONEndpoint(value, parent)

    def get_id(self, name: str, ids: list[int]) -> str:
        id = np.random.choice(0,1000)
        while id in ids:
            id = np.random.choice(0,1000)
        return f'{name}_*{id}'
    
    def get_item(self, item_dict, path):
        #path = [x.split('_*')[0] for x in path]
        current = item_dict
        while len(path) > 0:
            ind = path.pop(0)
            if type(ind) == list:
                current = current[ind[0]][ind[1]]
            else:
                current = current[ind]
        return current
    
    def get_endpoints(self) -> dict["JSONEndpoint", any]:
        return self.endpoints
    
    def find_all(self, query: any) -> dict[str, any]:
        """Returns the location and value of all data containing the query"""
        matches = {}
        for endpoint, val in self.endpoints.items():
            if type(val) in [list, str]:
                if query in val:
                    path = endpoint.get_path()
                    matches[endpoint] = val
            elif type(query) in [float, int]:
                if query == val:
                    path = endpoint.get_path()
                    matches[f'Location: root{path}'] = val
        return matches
    
    def find_tags(self, query: str, return_endpoints=False) -> dict[str, any]:
        matches = {}
        for endpoint in self.endpoints:
            path = endpoint.get_path()
            if query in path:
                node = endpoint.parent
                while True:
                    if type(node.name) == list:
                        tag = node.name[1]
                    else:
                        tag = node.name
                    if tag == query:
                        break
                    node = node.parent
                
                matches[node] = self.get_item(self.js, node.get_path())
        return matches
    
    def find_neighbors_tag(self, query):
        endpoints = self.find_tags(query)
        neighbors = {}
        for endpoint in endpoints:
            if isinstance(endpoint, JSONVertex):
                neighbors[endpoint.parent] = self.get_item(self.js, endpoint.parent.get_path())
            else:
                neighbors[endpoint.parent.parent] = self.get_item(self.js, endpoint.parent.parent.get_path())
        return neighbors
    
    def find_neighbors_content(self, query):
        endpoints = self.find_all(query)
        neighbors = {}
        for endpoint in endpoints:
            neighbors[endpoint.parent.parent] = self.get_item(self.js, endpoint.parent.parent.get_path())
        return
    
    def find_neighbors(self, vertex: "JSONVertex | JSONEndpoint") -> dict:
        if isinstance(vertex, JSONVertex):
            return self.get_item(self.js, vertex.parent.get_path())
        elif isinstance(vertex, JSONEndpoint):
            return self.get_item(self.js, vertex.parent.parent.get_path())
        else:
            raise TypeError('Vertex Must be a JSONVertex or JSONEndpoint instance')


class JSONVertex:
    children: list[str]
    parent: "JSONVertex | None"
    name: str | list[int, str]
    def __init__(self, name, parent: "JSONVertex | None"):
        self.parent = parent
        self.name = name
        pass

    def get_path(self):
        path = [self.name]
        node = self
        while node.parent is not None:
            parent_name = node.parent.name
            if type(parent_name) == list:
                path = parent_name + path 
            else:
                path = [parent_name] + path
            node = node.parent
        return path
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        path = self.get_path()
        return f"JSONEndpoint(root{path})"


class JSONEndpoint:
    parent: JSONVertex
    value: any
    def __init__(self, value, parent):
        self.parent = parent
        self.value = value
        pass

    def get_path(self):
        path = []
        node = self
        while node.parent is not None:
            parent_name = node.parent.name
            if type(parent_name) == list:
                path = parent_name + path 
            else:
                path = [parent_name] + path
            node = node.parent
        return path

    def __str__(self):
        return f'{self.parent.name}: {self.value}'
    
    def __repr__(self):
        path = self.get_path()
        return f"JSONEndpoint(root{path})"