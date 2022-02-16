import apalib.config as config
import apalib.apalibExceptions as apaExcept
import sys


class PDB:
    def Fetch(self, prot):
        print("Fetching ", prot)
        import urllib.request
        url = r'https://files.rcsb.org/download/' + prot.strip() + '.pdb'
        try:
            with urllib.request.urlopen(url) as f:
                config.Container.SetFetch(f.read().decode('utf-8'))
                self.Parse()
        except urllib.error.URLError:
            sys.stderr.write("The requested pdb code could not be retrieved or does not exist\n")

    # Wrapper for the ParsePDB file to allow functionality with a fetched protein
    def Parse(self):
        try:
            if config.Container.GetFetch() is None:
                raise apaExcept.NoFetchError
            return self.ParsePDB(config.Container.GetFetch().splitlines())
        except apaExcept.NoFetchError as e:
            sys.stderr.write(e.message)

    def ParsePDB(self, pdbFile):
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
                if line.find('ASN') != -1:
                    print('stop')
                groupNumber = int("".join(chr for chr in line[22:27] if chr.isdigit()))
                atomNumber = int(line[6:11])
                id = line[11:16].strip()
                groupName = line[16:20].strip()
                coordinates = [float(line[27:38]), float(line[38:46]), float(line[46:55])]
                occupancy = float(line[55:60])
                bfactor = float(line[60:67])
                element = line[77:].strip()
                newAtom = config.Atom(number=atomNumber, coordinates=coordinates, id=id, occupancy=occupancy,
                               b_factor=bfactor, element=element, residue=groupName)

                # RNA atom
                if line[0:6] == "HETATM":
                    if chain not in HETATMChains:
                        HETATMChains[chain] = dict()
                    if groupNumber not in HETATMChains[chain]:
                        HETATMChains[chain][groupNumber] = config.HETATM(name=groupName, number=groupNumber)
                    HETATMChains[chain][groupNumber].InsertAtom(newAtom)
                elif len(groupName) == 1:
                    if chain not in RNAChains:
                        RNAChains[chain] = dict()
                    if groupNumber not in RNAChains[chain]:
                        RNAChains[chain][groupNumber] = config.RNA(name=groupName, number=groupNumber)
                    RNAChains[chain][groupNumber].InsertAtom(newAtom)

                elif len(groupName) == 2:
                    if chain not in DNAChains:
                        DNAChains[chain] = dict()
                    if groupNumber not in DNAChains[chain]:
                        DNAChains[chain][groupNumber] = config.DNA(name=groupName, number=groupNumber)
                    DNAChains[chain][groupNumber].InsertAtom(newAtom)

                elif len(groupName) == 3 or len(groupName) == 4:
                    if chain not in proteinChains:
                        proteinChains[chain] = dict()
                    if groupNumber not in proteinChains[chain]:
                        proteinChains[chain][groupNumber] = config.AminoAcid(name=groupName, number=groupNumber)
                    proteinChains[chain][groupNumber].InsertAtom(newAtom)

        # Postparsing functions
        config.Container.SetProteinChains(proteinChains)
        config.Container.SetDNAChains(DNAChains)
        config.Container.SetRNAChains(RNAChains)
        config.Container.SetHETATMChains(HETATMChains)

        for chain in config.Container.GetPeptideChains():
            for index in config.Container.GetPeptideChains()[chain]:
                config.Container.GetPeptideChains()[chain][index].CalculateCentroid(config.Container.GetPeptideChains()[chain][index].atoms)
