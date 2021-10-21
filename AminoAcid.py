global ONE_LETTER
global THREE_LETTER
global FULL_NAME

class AminoAcid:
    def __init__(self, **kwargs):
        self.flags = dict()
        self.number = None
        self.atoms = list()
        self.name = None
        self.rotamer = None

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
        self.CalculateCentroid(atoms)

    def InsertAtom(self, atom):
        self.atoms.append(atom)

    def GetAtoms(self):
        return self.atoms

    def SetName(self, name, set_name):
        #TODO check the functionality of this
        if not set_name:
            self.name = name
        elif len(name) == 3 and name in THREE_LETTER:
            self.name = name
        elif len(name) == 3 and name not in THREE_LETTER:
            self.flags['BAD_NAME'] = "Three-letter code not recognized"
            self.name = None
        elif len(name) == 1:
            self.name = self.OneToThree(name)
        elif len(name) <= 4:
            if name[-3:] in THREE_LETTER:
                self.name = name[-3:]
                self.rotamer = name[:-3]
                self.flags['ROT_RES'] = "This residue has a rotamer conformation"
            else:
                self.flags['BAD_NAME'] = "Three-letter code not recognized"
                self.name = None
        elif len(name) == 2:
            self.flags['BAD_NAME'] = "Name cannot be two letters"
            self.name = None
        if self.name is not None:
            if 'BAD_NAME' in self.flags:
                self.flags.pop('BAD_NAME')

    def SetHeptad(self, heptad):
        self.heptad = heptad

    def InsertAtom(self, atom):
        self.atoms.append(atom)

    def CalculateCentroid(self, atoms):
        # *For Glycine, only the alpha carbon is considered
        # *For Alanine, only the beta carbon is considered
        AAs = {
            "SER": ['OG'],
            "CYS": ['SG'],
            "SEC": ['SE'],
            "GLY": ['CA'],
            "ALA": ['CB'],
            "THR": ['OG1', 'CG2'],
            "PRO": ['CG', 'CD'],
            "VAL": ['CG1', 'CG2'],
            "ASP": ['CG', 'OD1', 'OD2'],
            "ASN": ['CG', 'OD1', 'ND2'],
            "ILE": ['CG1', 'CG2', 'CD1'],
            "LEU": ['CG', 'CD1', 'CD2'],
            "MET": ['CG', 'SD', 'CE'],
            "LYS": ['CG', 'CD', 'CE', 'NZ'],
            "GLU": ['CG', 'CD', 'OE1', 'OE2'],
            "GLN": ['CG', 'CD', 'OE1', 'NE2'],
            "HIS": ['CG', 'ND1', 'CD2', 'CE1', 'NE2'],
            "ARG": ['CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'],
            "PHE": ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
            "TYR": ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'OH'],
            "TRP": ['CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2']
        }
        #TODO Deal with non-1 occupancy
        if len(self.name) == 3 and self.name in AAs:
            #If residue is not specified
            x_coord = 0
            y_coord = 0
            z_coord = 0
            num_atoms = 0
            for atom in [atom for atom in atoms if atom.id in AAs[self.name]]:
                if atom.element == 'H':
                    continue
                x_coord += atom.GetCoordinates()[0]
                y_coord += atom.GetCoordinates()[1]
                z_coord += atom.GetCoordinates()[2]
                num_atoms += 1
            self.centroid = list()
            try:
                self.centroid.append(x_coord / num_atoms)
                self.centroid.append(y_coord / num_atoms)
                self.centroid.append(z_coord / num_atoms)
            except ZeroDivisionError:
                self.centroid.clear()
                beta = [atom for atom in atoms if atom.id == 'CB']
                alpha = [atom for atom in atoms if atom.id == 'CA']
                if len(beta) != 0:
                    self.centroid.append(beta[0].coordinates[0])
                    self.centroid.append(beta[0].coordinates[1])
                    self.centroid.append(beta[0].coordinates[2])
                    self.flags['B_CENTROID'] = "This residue is missing information to get an accurate centroid" \
                                               "calculation. The coordinates of the beta carbon will be used"
                elif len(alpha) != 0:
                    self.centroid.append(alpha[0].coordinates[0])
                    self.centroid.append(alpha[0].coordinates[1])
                    self.centroid.append(alpha[0].coordinates[2])
                    self.flags['A_CENTROID'] = "This residue is missing information to get an accurate centroid" \
                                               "calculation. The coordinates of the alpha carbon will be used"
                else:
                    self.centroid = None
                    self.flags['BAD_CENTROID'] = "Too few atoms were included with this residue to calculate a centroid."


        elif len(self.name) == 4 and self.name[1:] in AAs:
            import sys
            sys.stderr.write("ROTAMER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            import sys
            sys.exit("UNKNOWN AMINO ACID YO")

    def GetCentroid(self):
        return self.centroid

    def OneToThree(self, oln):
        if oln in self.ONE_LETTER:
            try:
                self.name = self.ONE_LETTER[oln]
            except KeyError:
                self.flags['BAD_NAME'] = 'This residue was assigned a bad name. Check that the correct one-letter code was used'
                self.name = None

    def NameToThree(self, name):
        if name in self.FULL_NAME:
            try:
                self.name = self.FULL_NAME[name]
            except KeyError:
                self.flags['BAD_NAME'] = 'This residue was assigned a bad name. Check that the residue name was spelled correctly'
                self.name = None

    def __lt__(self, other):
        return self.number < other.number
    def __repr__(self):
        return f"RESIDUE: {self.name}, NUMBER: {self.number}"
    def __str__(self):
        return f"{self.name} {self.number}"




#Shoved down here for cleanliness
global ONE_LETTER
ONE_LETTER = {
    "R": 'ARG',
    "H": 'HIS',
    "K": 'LYS',
    "D": 'ASP',
    "E": 'GLU',
    "S": 'SER',
    "T": 'THR',
    "N": 'ASN',
    "Q": 'GLN',
    "C": 'CYS',
    "U": 'SEC',
    "G": 'GLY',
    "P": 'PRO',
    "A": 'ALA',
    "V": 'VAL',
    "I": 'ILE',
    "L": 'LEU',
    "M": 'MET',
    "F": 'PHE',
    "Y": 'TYR',
    "W": 'TRP',
    "O": 'PYL'
}
global THREE_LETTER
THREE_LETTER = {
    "ARG": 'R',
    "HIS": 'H',
    "LYS": 'K',
    "ASP": 'D',
    "GLU": 'E',
    "SER": 'S',
    "THR": 'T',
    "ASN": 'N',
    "GLN": 'G',
    "CYS": 'C',
    "SEC": 'U',
    "GLY": 'G',
    "PRO": 'P',
    "ALA": 'A',
    "VAL": 'V',
    "ILE": 'I',
    "LEU": 'L',
    "MET": 'M',
    "PHE": 'F',
    "TYR": 'Y',
    "TRP": 'W',
    "PYL": 'O'
}

global FULL_NAME
FULL_NAME = {
    "ALANINE": 'ALA',
    "CYSTEINE": 'CYS',
    "ASPARTIC ACID": 'ASP',
    "ASPARTATE" : 'ASP',
    "GLUTAMIC ACID" : 'GLU',
    "GLUTAMATE" : 'GLU',
    "PHENYLALANINE" : 'PHE',
    "GLYCINE" : 'GLY',
    "HISTIDINE" : 'HIS',
    "ISOLEUCINE" : 'ILE',
    "LYSINE" : 'LYS',
    "LEUCINE" : 'LEU',
    "METHIONINE": 'MET',
    "ASPARAGINE": 'ASN',
    "PYRROLYSINE": 'PYL',
    "PROLINE": 'PRO',
    "GLUTAMINE": 'GLN',
    "ARGININE": 'ARG',
    "SERINE": 'SER',
    "THREONINE": 'THR',
    "SELENOCYSTEINE": 'SEC',
    "VALINE": 'VAL',
    "TRYPTOPHAN": 'TRP',
    "TYROSINE": 'TYR',
}