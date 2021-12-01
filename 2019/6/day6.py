DATA_FILEPATH = "data.txt"


class OrbitalBody:
    def __init__(self, name, parent):
        self.name = name
        self.parent: OrbitalBody = parent
        self.children = []
        self.orbital_distance = None


    def add_child(self, orbital_body):
        if (orbital_body not in self.children):
            self.children.append(orbital_body)


class OrbitalSystem:
    def __init__(self):
        self.bodies = {}
        self.root = None


    def insert(self, orbital_body):
        self.bodies[orbital_body.name] = orbital_body
        if (orbital_body.parent != None):
            self.bodies[orbital_body.parent.name].add_child(orbital_body)

    
    def get(self, name):
        return self.bodies.get(name)


    def count_direct_orbits(self):
        return len(self.bodies) - 1

    
    def count_indirect_orbits(self):
        def find_orbital_distance()

        indirect_orbits = 0
        for body in self.bodies.values():




def read_data(filepath):
    relationships = []

    with open(filepath) as fd:
        for line in fd.readlines():
            relationships.append(list(line.strip().split(')')))

    return relationships


if (__name__ == '__main__'):
    system = OrbitalSystem()

    for relationship in read_data(DATA_FILEPATH):
        parent_name = relationship[0]
        child_name = relationship[1]

        parent_body = system.get(parent_name)
        if (not parent_body):
            parent_body = OrbitalBody(parent_name, None)
            system.insert(parent_body)
            system.root = parent_body

        system.insert(OrbitalBody(child_name, parent_body))

    print(len(system.bodies))
