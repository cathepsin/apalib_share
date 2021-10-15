class RNA:
    def __init__(self, **kwargs):
        self.flags = dict()
        self.number = None
        self.atoms = list()
        self.name = None

        self.SetN()
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
        self.GetCentroid(atoms)

    def InsertAtom(self, atom):
        self.atoms.append(atom)

    def SetName(self, name):
        self.name = name

    def SetN(self):
        self.ONE_LETTER = {
            'A': 'ADENINE',
            'C': 'CYTOSINE',
            'G': 'GUANINE',
            'T': 'THYMINE',
            'U': 'URACIL',
            'I': 'INOSINE'
        }
        self.FULL_NAME = {
            'ADENINE': 'A',
            'CYTOSINE': 'C',
            'GUANINE': 'G',
            'THYMINE': 'T',
            'URACIL': 'U',
            'INOSINE': 'I'
        }
