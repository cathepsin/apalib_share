import sys
import AminoAcid
import DNA
import RNA
import apalibExceptions
import Atom
import HETATM

global current_fetch
current_fetch = None


# TODO Move **ALL HARDCODED DATA** into a json

class container:
    def __init__(self):
        self.current_fetch = None
        self.ProteinChains = None
        self.DNAChains = None
        self.RNAChains = None
        self.HETATMChains = None


global CONTAINER
CONTAINER = container()


def ClearAll():
    global CONTAINER
    CONTAINER = container()


def SetFetch(fetch):
    global CONTAINER
    CONTAINER.current_fetch = fetch


def GetFetch():
    global CONTAINER
    return CONTAINER.current_fetch


def SetProteinChains(pchain):
    global CONTAINER
    CONTAINER.ProteinChains = pchain


def GetProteinChains():
    global CONTAINER
    return CONTAINER.ProteinChains


def SetDNAChains(dchain):
    global CONTAINER
    CONTAINER.DNAChains = dchain


def GetDNAChains():
    global CONTAINER
    return CONTAINER.DNAChains


def GetRNAChains():
    global CONTAINER
    return CONTAINER.RNAChains


def SetRNAChains(rchain):
    global CONTAINER
    CONTAINER.RNAChains = rchain


def GetHETATMChains():
    global CONTAINER
    return CONTAINER.HETATMChains


def SetHETATMChains(hchain):
    global CONTAINER
    CONTAINER.HETATMChains = hchain

#Return all residues from all chains as a single list
def AsList():
    global CONTAINER
    fullLst = []
    retLst = []
    lst = [CONTAINER.ProteinChains, CONTAINER.DNAChains, CONTAINER.RNAChains, CONTAINER.HETATMChains]
    for val in lst:
        if val is not None and len(val.keys()) != 0:
            fullLst = fullLst + list(val.values())
    for val in fullLst:
        retLst = retLst + list(val.values())
    return retLst




def Fetch(prot):
    print("Fetching ", prot)
    import urllib.request
    url = r'https://files.rcsb.org/download/' + prot.strip() + '.pdb'
    try:
        with urllib.request.urlopen(url) as f:
            SetFetch(f.read().decode('utf-8'))
    except urllib.error.URLError:
        sys.stderr.write("The requested pdb code could not be retrieved or does not exist\n")


# Clears the fetched protein
def ClearFetch():
    global CONTAINER
    CONTAINER.current_fetch = None


# Wrapper for the ParsePDB file to allow functionality with a fetched protein
def Parse():
    try:
        if GetFetch() is None:
            raise apalibExceptions.NoFetchError
        return ParsePDB(GetFetch().splitlines())
    except apalibExceptions.NoFetchError as e:
        sys.stderr.write(e.message)


# TODO get this to work with DNA and RNA domains https://pdb101.rcsb.org/learn/guide-to-understanding-pdb-data/primary-sequences-and-the-pdb-format
# Parsing DNA/RNA should be essentially the same as an amino acid atom-group, with some intricacies. 1pyi is a good example
# TODO Check other PDB standards
# TODO Ensure functionality with symmetry pairs
# TODO Make set_name a thing everywhere
def ParsePDB(pdbFile):
    proteinChains = dict()
    DNAChains = dict()
    RNAChains = dict()
    HETATMChains = dict()
    for line in pdbFile:
        if line[0:4] == "ATOM" or line[0:6] == 'HETATM':
            # Create a new chain if needed
            chain = line[20:22].strip()
            if chain == '':
                chain = '$'
            groupNumber = int("".join(chr for chr in line[22:27] if chr.isdigit()))
            atomNumber = int(line[6:11])
            id = line[11:16].strip()
            groupName = line[16:20].strip()
            coordinates = [float(line[27:38]), float(line[38:46]), float(line[46:55])]
            occupancy = float(line[55:60])
            bfactor = float(line[60:67])
            element = line[77:].strip()
            newAtom = Atom.Atom(number=atomNumber, coordinates=coordinates, id=id, occupancy=occupancy,
                                b_factor=bfactor, element=element, residue=groupName)

            # RNA atom
            if line[0:6] == "HETATM":
                if chain not in HETATMChains:
                    HETATMChains[chain] = dict()
                if groupNumber not in HETATMChains[chain]:
                    HETATMChains[chain][groupNumber] = HETATM.HETATM(name=groupName, number=groupNumber)
                HETATMChains[chain][groupNumber].InsertAtom(newAtom)
            elif len(groupName) == 1:
                if chain not in RNAChains:
                    RNAChains[chain] = dict()
                if groupNumber not in RNAChains[chain]:
                    RNAChains[chain][groupNumber] = RNA.RNA(name=groupName, number=groupNumber)
                RNAChains[chain][groupNumber].InsertAtom(newAtom)

            elif len(groupName) == 2:
                if chain not in DNAChains:
                    DNAChains[chain] = dict()
                if groupNumber not in DNAChains[chain]:
                    DNAChains[chain][groupNumber] = DNA.DNA(name=groupName, number=groupNumber)
                DNAChains[chain][groupNumber].InsertAtom(newAtom)

            elif len(groupName) == 3 or len(groupName) == 4:
                if chain not in proteinChains:
                    proteinChains[chain] = dict()
                if groupNumber not in proteinChains[chain]:
                    proteinChains[chain][groupNumber] = AminoAcid.AminoAcid(name=groupName, number=groupNumber)
                proteinChains[chain][groupNumber].InsertAtom(newAtom)

    # Postparsing functions
    SetProteinChains(proteinChains)
    SetDNAChains(DNAChains)
    SetRNAChains(RNAChains)
    SetHETATMChains(HETATMChains)

    for chain in GetProteinChains():
        for index in GetProteinChains()[chain]:
            GetProteinChains()[chain][index].CalculateCentroid(GetProteinChains()[chain][index].atoms)


#  Naive approach to calculating isoelectric point at a specific pH

def getIEP(pHofInterest):
    global CONTAINER
    curr_protein_chains = CONTAINER.ProteinChains

    # initialize dict of counts
    total_counts = {'NTERM': 0, 'CTERM': 0, 'CYS': 0, 'ASP': 0, 'GLU': 0, 'HIS': 0, 'LYS': 0, 'ARG': 0, 'TYR': 0}
    import copy
    test = copy.deepcopy(total_counts)
    for key, value in curr_protein_chains.items():
        current_chain = value
        #TODO Add check for termini (in case section of a protein is checked instead of a full protein)
        #TODO Are there pKas for nucleic acids?

        total_counts['NTERM'] += 1
        total_counts['CTERM'] += 1

        for key, value in current_chain.items():
            if value.name == "CYS":
                total_counts['CYS'] += 1
            elif value.name == "ASP":
                total_counts['ASP'] += 1
            elif value.name == "GLU":
                total_counts['GLU'] += 1
            elif value.name == "HIS":
                total_counts['HIS'] += 1
            elif value.name == "LYS":
                total_counts['LYS'] += 1
            elif value.name == "ARG":
                total_counts['ARG'] += 1
            elif value.name == "TYR":
                total_counts['TYR'] += 1



    print(total_counts)

    # TODO Add pKa values to JSON file
    # using "EMBOSS" pKa's

    sum_charges = 0

    if pHofInterest < 8.6:
        sum_charges += total_counts['NTERM']
    if pHofInterest > 3.6:
        sum_charges -= total_counts['CTERM']
    if pHofInterest > 8.5:
        sum_charges -= total_counts['CYS']
    if pHofInterest > 3.9:
        sum_charges -= total_counts['ASP']
    if pHofInterest > 4.1:
        sum_charges -= total_counts['GLU']
    if pHofInterest < 6.5:
        sum_charges += total_counts['HIS']
    if pHofInterest < 10.8:
        sum_charges += total_counts['LYS']
    if pHofInterest < 12.5:
        sum_charges += total_counts['ARG']
    if pHofInterest > 10.1:
        sum_charges -= total_counts['TYR']

    return sum_charges










# TODO in all GETTERS in each class, add a check to see if variable exists
# if var in self.__dict__:
#   return var
# return None


# TODO Complete the below functions before pushing version 1.0.0

# def SurfaceArea(**kwargs):
#     if 'domain' not in kwargs:
#         sys.stderr.write("No domain provided. Specify using SurfaceArea(domain=val)\n")
#     if 'num_dots' not in kwargs:
#         sys.stderr.write("Number of dots not provided. Specify using SurfaceArea(num_dots=val)\n")
#     if 'solvent_radius' not in kwargs:
#         sys.stderr.write("Solvent radius not provided. Specify using SurfaceArea(solvent_radius=val)\n")
#     print("stub")
#
# def GetDistance(coor1, coor2):
#     return ((coor1[0] - coor2[0])**2 + (coor1[1] - coor2[1])**2 + (coor1[2] - coor2[2])**2)**.5
#
# def VectorPair(self, AA1, AA2):
#     # Slope of line made from CA --> CENTROID
#     CA1 = AA1.GetCA()
#     CA2 = AA2.GetCA()
#     # XY orthogonal projection
#     m1 = (AA1.GetCentroid()[1] - CA1.GetCoordinates()[1]) / (AA1.GetCentroid()[0] - CA1.GetCoordinates()[0])
#     m2 = (AA2.GetCentroid()[1] - CA2.GetCoordinates()[1]) / (AA2.GetCentroid()[0] - CA2.GetCoordinates()[0])
#     # Intersection point
#     #
#     #               y_2 - y_1 + m_1x_1 - m_2x_2
#     #   x_int =    ------------------------------
#     #                       m_1 - m_2
#
#     x_int = (AA2.GetCentroid()[1] - AA1.GetCentroid()[1] + m1 * AA1.GetCentroid()[0] - m2 * AA2.GetCentroid()[0]) / (m1 - m2)
#     # Cast back into 3D
#     #
#     #        x - x_1
#     #   z = --------- * c + z_1
#     #           a
#
#     y1 = (x_int - AA1.GetCentroid()[0]) / AA1.vector[0] * AA1.vector[1] + AA1.GetCentroid()[1]
#     y2 = (x_int - AA2.GetCentroid()[0]) / AA2.vector[0] * AA2.vector[1] + AA2.centroid[1]
#
#     z1 = (x_int - AA1.GetCentroid()[0]) / AA1.vector[0] * AA1.vector[2] + AA1.GetCentroid()[2]
#     z2 = (x_int - AA2.GetCentroid()[0]) / AA2.vector[0] * AA2.vector[2] + AA2.GetCentroid()[2]
#     return abs(z1 - z2), [x_int, y1, z1], [x_int, y2, z2]
#
# def CheckBridge(object1, object2):
#     print("stub")

# TODO Make sure ALL flags are properly cleared automatically


########################################################################################################################

Fetch('3mzw')
Parse()
print(GetProteinChains()['A'][1])
print(getIEP(7.4))
# print(GetProteinChains()['A'][1].GetAtoms()[0].GetCoordinates(), GetProteinChains()['A'][1].GetAtoms()[2].GetCoordinates())
# print(GetDistance(GetProteinChains()['A'][1].GetAtoms()[0].GetCoordinates(), GetProteinChains()['A'][1].GetAtoms()[2].GetCoordinates()))
