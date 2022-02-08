# global FULL_NAME
# global ONE_LETTER
global FLAGS
FLAGS = {}

class RNA:
    def __init__(self, **kwargs):
        self.number = None
        self.atoms = None
        self.name = None

        set_name = True
        if 'set_name' in kwargs:
            set_name = kwargs['set_name']
        if 'name' in kwargs:
            self.SetName(kwargs['name'], set_name)
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
        if self.atoms is None:
            self.atoms = list()
        self.atoms.append(atom)

    def SetName(self, name, set_name):
        if not set_name:
            self.name = name
            self.RaiseFlag('NO_NAME_CHECK')
            self.ClearFlag('BAD_NAME')
            return
        else:
            self.ClearFlag('NO_NAME_CHECK')
        global ONE_LETTER
        if name in ONE_LETTER:
            self.name = ONE_LETTER[name]
        elif name in FULL_NAME:
            self.name = FULL_NAME[name]
        else:
            self.RaiseFlag('BAD_NAME')
            return
        self.ClearFlag('BAD_NAME')
        return

    @staticmethod
    def CheckFlag(f):
        global FLAGS
        if f in FLAGS:
            return FLAGS[f]
        return False

    @staticmethod
    def RaiseFlag(flag):
        global FLAGS
        FLAGS[flag] = True

    @staticmethod
    def ClearFlag(flag):
        global FLAGS
        FLAGS[flag] = False

    def __lt__(self, other):
        return self.number < other.number

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
