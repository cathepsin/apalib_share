class HETATM:
    def __init__(self, **kwargs):
        self.flags = dict()
        self.number = None
        self.atoms = list()
        self.name = None

        if 'name' in kwargs:
            self.SetName(kwargs['name'])
        if 'number' in kwargs:
            self.SetNumber(kwargs['number'])
        if 'atoms' in kwargs:
            self.SetAtoms(kwargs['atoms'])

    def SetNumber(self, num):
        self.number = num

    def SetAtoms(self, atoms):
        self.atoms = atoms
        self.CalculateCentroid(atoms)

    def InsertAtom(self, atom):
        self.atoms.append(atom)

    def SetName(self, name):
        self.name = name
        #TODO set_name functionality

    def ClearFlags(self):
        self.flags.clear()

    def CalculateCentroid(self, atoms):
        n = 0
        x = 0
        y = 0
        z = 0
        for atom in atoms:
            n += 1
            x += atom.GetCoordinates()[0]
            y += atom.GetCoordinates()[1]
            z += atom.GetCoordinates()[2]
        self.centroid = [x/n, y/n, z/n]

    def GetCentroid(self):
        if 'centroid' in self.__dict:
            return self.centroid
        return None

    def ClearFlag(self, flag):
        try:
            self.flags.pop(flag)
        except:
            pass
