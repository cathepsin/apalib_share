global FULL_NAME
global ONE_LETTER

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
        #TODO set_name functionality

    def SetN(self):
        global ONE_LETTER
        ONE_LETTER = {
            'A': 'ADENINE',
            'C': 'CYTOSINE',
            'G': 'GUANINE',
            'T': 'THYMINE',
            'U': 'URACIL',
            'I': 'INOSINE'
        }
        global FULL_NAME
        FULL_NAME = {
            'ADENINE': 'A',
            'CYTOSINE': 'C',
            'GUANINE': 'G',
            'THYMINE': 'T',
            'URACIL': 'U',
            'INOSINE': 'I'
        }
