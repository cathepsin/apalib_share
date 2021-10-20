import sys
import AminoAcid
import DNA
import RNA
import apalibExceptions
import Atom
import HETATM

global current_fetch
current_fetch = None

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


def Fetch(prot):
    print("Fetching ", prot)
    import urllib.request
    url = r'https://files.rcsb.org/download/' + prot.strip() + '.pdb'
    try:
        with urllib.request.urlopen(url) as f:
            SetFetch(f.read().decode('utf-8'))
    except:
        sys.stderr.write("The requested pdb code could not be retrieved or does not exist\n")

#Clears the fetched protein
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

#TODO get this to work with DNA and RNA domains https://pdb101.rcsb.org/learn/guide-to-understanding-pdb-data/primary-sequences-and-the-pdb-format
#Parsing DNA/RNA should be essentially the same as an amino acid atom-group, with some intricacies. 1pyi is a good example
#TODO Check other PDB standards
#TODO Ensure functionality with symmetry pairs
def ParsePDB(pdbFile):
    proteinChains = dict()
    DNAChains = dict()
    RNAChains = dict()
    HETATMChains = dict()
    for line in pdbFile:
        if line[0:4] == "ATOM" or line[0:6] == 'HETATM':
            #Create a new chain if needed
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
            newAtom = Atom.Atom(number=atomNumber, coordinates=coordinates, id=id, occupancy=occupancy, b_factor=bfactor, element=element, residue=groupName)

            #RNA atom
            if line[0:6] == "HETATM":
                if chain not in HETATMChains:
                    HETATMChains[chain] = dict()
                if groupNumber not in HETATMChains[chain]:
                    HETATMChains[chain][groupNumber] = HETATM.HETATM(name=groupName, number=groupNumber)
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

    #Postparsing functions
    SetProteinChains(proteinChains)
    SetDNAChains(DNAChains)
    SetRNAChains(RNAChains)
    SetHETATMChains(HETATMChains)

    for chain in GetProteinChains():
        for index in GetProteinChains()[chain]:
            GetProteinChains()[chain][index].GetCentroid(GetProteinChains()[chain][index].atoms)

#TODO Complete the below functions before pushing version 1.0.0
def SurfaceArea(**kwargs):
    if 'domain' not in kwargs:
        sys.stderr.write("No domain provided. Specify using SurfaceArea(domain=val)\n")
    if 'num_dots' not in kwargs:
        sys.stderr.write("Number of dots not provided. Specify using SurfaceArea(num_dots=val)\n")
    if 'solvent_radius' not in kwargs:
        sys.stderr.write("Solvent radius not provided. Specify using SurfaceArea(solvent_radius=val)\n")
    print("stub")

def GetDistance(object1, object2):
    print("stub")

def CheckBridge(object1, object2):
    print("stub")
