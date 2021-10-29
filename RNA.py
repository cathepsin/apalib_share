global FULL_NAME
global ONE_LETTER

class RNA:
    def __init__(self, **kwargs):
        self.flags = dict()
        self.number = None
        self.atoms = list()
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
        self.atoms.append(atom)

    def SetName(self, name, set_name):
        if not set_name:
            self.name = name
            self.flags['NO_NAME_CHECK'] = 'The name of this residue was not checked and may not be standard'
            return
        else:
            try:
                self.flags.pop('NO_NAME_CHECK')
            except:
                pass
        global ONE_LETTER
        if name in ONE_LETTER:
            self.name = name
            return
        else:
            self.flags['BAD_NAME'] = 'The provided name is invalid and does not map to a residue'
        #TODO set_name functionality



    def ClearFlag(self, flag):
        try:
            self.flags.pop(flag)
        except:
            pass

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
