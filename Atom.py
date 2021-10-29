class Atom:
    def __init__(self, **kwargs):
        self.flags = dict()
        extract = True
        if 'extract' in kwargs:
            extract = kwargs['extract']
        if 'number' in kwargs:
            self.SetNumber(kwargs['number'])
        if 'coordinates' in kwargs:
            self.SetCoordinates(kwargs['coordinates'])
        if 'id' in kwargs:
            self.SetID(kwargs['id'], extract)
        if 'occupancy' in kwargs:
            self.SetOccupancy(kwargs['occupancy'])
        if 'b_factor' in kwargs:
            self.SetBFactor(kwargs['b_factor'])
        if 'element' in kwargs:
            self.SetElement(kwargs['element'])
        if 'residue' in kwargs:
            self.SetResidue(kwargs['residue'])

    def SetNumber(self, num):
        self.number = num

    def GetNumber(self):
        if 'number' in self.__dict__:
            return self.number
        return None

    def SetCoordinates(self, coor):
        self.coordinates = [coor[0], coor[1], coor[2]]

    def GetCoordinates(self):
        if 'coordinates' in self.__dict__:
            return self.coordinates
        return None

    def SetID(self, id, extract):
        self.id = id
        if extract:
            self.__ExtractElement(id)

    def GeID(self):
        if 'id' in self.__dict__:
            return self.id
        return None

    def SetOccupancy(self, occ):
        self.occupancy = occ

    def GetOccupancy(self):
        if 'occupancy' in self.__dict__:
            return self.occupancy
        return None

    def SetBFactor(self, bfact):
        self.b_factor = bfact

    def GetBFactor(self):
        if 'b_factor' in self.__dict__:
            return self.b_factor
        return None

    def SetElement(self, ele):
        self.element = ele

    def GetElement(self):
        if 'element' in self.__dict__:
            return self.element
        return None

    def SetResidue(self, res):
        #TODO Set rotation based off of parameter. Add a bool parameter
        if len(res) == 4:
            self.rotation = res[0]
            self.residue = res[1:]
            return
        self.residue = res

    def GetResidue(self):
        if 'residue' in self.__dict__:
            return self.residue
        return None

    #In case the element informatin is missing
    def __ExtractElement(self, id):
        if 'C' in id:
            self.SetElement('C')
        elif 'S' in id:
            self.SetElement('S')
        elif 'O' in id:
            self.SetElement('O')
        elif 'N' in id:
            self.SetElement('N')
        elif 'P' in id:
            self.SetElement('P')
        elif 'ZN' in id:
            self.SetElement('ZN')
        elif 'CU' in id:
            self.SetElement('CU')
        elif 'SE' in id:
            self.SetElement('SE')
        elif 'MG' in id:
            self.SetElement('MG')
        elif 'H' in id:
            self.SetElement('H')
        else:
            import sys
            sys.exit("SOMETHING WENT WRONG! CHECK WHAT HAPPENED")

    def __repr__(self):
        return f"ATOM: NUMBER: {self.number}, " \
               f"TAG: {self.id}, RESIDUE: {self.residue}, " \
               f"COORDINATES: {self.coordinates}, OCCUPANCY: {self.occupancy}," \
               f" B_FACTOR: {self.bfactor}, ELEMENT: {self.element}"

    def __str__(self):
        return f"{self.id} {self.residue} {self.coordinates}"