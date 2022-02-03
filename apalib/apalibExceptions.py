class NoFetchError(Exception):
    #Used when a fetched pdb file is required but not provided
    def __init__(self):
        self.message = 'No fetched protein. Use method Fetch(PDB_CODE) to fetch a protein.\n'

    def __str__(self):
        return self.message