import pkg_resources
import json

class Data:
    def __init__(self):
        _stream = pkg_resources.resource_stream(__name__, 'data/chemistry.json')
        self._jData = json.load(_stream)

    def GetJson(self):
        return self._jData

    def Map(self, dtype, val):
        return self._jData["Map"][dtype][val]

    def ValidateAA(self, res):
        check_res = self.Standardize(res)
        if check_res in self._jData["Map"]["Amino Acids"].keys():
            return True
        return False

    def ValidateDNA(self, res, no_u = False):
        check_res = self.Standardize(res)
        if check_res == "-" or check_res == ".":
            return False
        if no_u and (check_res == "U" or check_res == "DU"):
            return False
        if check_res in self._jData["Map"]["DNA Nucleotides"].keys():
            return True
        return False

    def ValidateRNA(self, res, no_t = False):
        check_res = self.Standardize(res)
        if check_res == "-" or res == ".":
            return False
        if no_t and check_res == "T":
            return False
        if check_res in self._jData["Map"]["DNA Nucleotides"].keys():
            return True
        return False

    def Standardize(self, res):
        ret_str = ""
        for i in range(len(res)):
            if i == 0:
                ret_str += res[i].upper()
            elif i == 1 and len(res) == 2:
                ret_str += res[i].upper()
            else:
                ret_str += res[i].lower()
        return ret_str
