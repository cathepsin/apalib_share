global ONE_LETTER
global TWO_LETTER
global FULL_NAME


class DNA:
    def __init__(self, **kwargs):
        self.flags = dict()
        self.number = None
        self.atoms = list()
        self.name = None

        set_name = True
        # TODO Made set_name a thing everywhere
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
        if name in self.TWO_LETTER:
            self.name = name
            return
        if name in self.FULL_NAME:
            self.name = self.FULL_NAME[name]
        if name in self.ONE_LETTER:
            self.name = 'D' + name
            return

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
global TWO_LETTER
TWO_LETTER = {
    'DA': 'ADENINE',
    'DC': 'CYTOSINE',
    'DG': 'GUANINE',
    'DT': 'THYMINE',
    'DU': 'URACIL',
    'DI': 'INOSINE'
}
global FULL_NAME
FULL_NAME = {
    'ADENINE': 'DA',
    'CYTOSINE': 'DC',
    'GUANINE': 'DG',
    'THYMINE': 'DT',
    'URACIL': 'DU',
    'INOSINE': 'DI'
}
