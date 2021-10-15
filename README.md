#Advanced Protein Analysis Library
This library was created to provide tools useful for advanced protein analysis.
##Methods and Classes
###Library Methods:
####Parse(fd)
***Input:*** File descriptor to a pdb file  
***Output:*** None  
***Description:*** Parses a user-provided PDB (or similar) file.
Will work generally for .ent or .mmol extensions, but full
functionality is not guaranteed. Populates the CONTAINER object's
RNAChains, DNAChains, proteinChains, and HETATMChains dictionaries.    
####ParsePDB('PDBCode')
***Input:*** 4-letter PDB code of type *str*  
***Output:*** None  
***Description:*** Wrapper method for the Parse() function. Downloads a 
PDB file from the RCSB PDB and performs the Parse() function
on the retrieved file.
####ClearAll()
***Input:*** None  
***Output:*** None  
***Description:*** Clears the stored RNAChains, DNAChains, proteinChains,
 HETATMChains, and currently fetched PDB.
####SetFetch(fetch)
***Input:*** PDB info as string  
***Output:*** None  
***Description:*** CONTAINER current_fetch setter
####ClearFetch()
**Input:** None  
**Output:** None  
**Description:** Empties the buffer holding any fetched PDB
information. Not required for repeat fetches
####GetFetch()
**Input:** None  
**Output:** current_fetch  
**Description:** CONTAINER current_fetch getter
####SetProteinChains(protChains)
**Input:** Python dictionary containing protein chains  
**Output:** None  
**Description:** CONTAINER proteinChains setter
####GetProteinChains()
**Input:** None  
**Output:** proteinChains  
**Description:** CONTAINER proteinChains getter
####SetDNAChains(dnaChains)
**Input:** Python dicitonary containing DNA chains  
**Output:** None  
**Description:** CONTAINER DNAChains setter
####GetDNAChains()
**Input:** None  
**Output:** DNAChains  
**Description:** CONTAINER DNAChains getter
####SetRNAChains(dnaChains)
**Input:** Python dicitonary containing RNA chains  
**Output:** None  
**Description:** CONTAINER RNAChains setter
####GetRNAChains()
**Input:** None  
**Output:** RNAChains  
**Description:** CONTAINER RNAChains getter
####SetHETATMChains(hetatmChains)
**Input:** Python dicitonary containing HETATM chains  
**Output:** None  
**Description:** CONTAINER HETATMChains setter
####GetHETATMChains()
**Input:** None  
**Output:** HETATMChains  
**Description:** CONTAINER HETATMChains getter
###CONTAINER Class
A class used to store useful information and keep data somewhat abstracted. Stored variables, as
well as their getters/setters are listed below. A single instance of this
class is created when the module is loaded. Though not required, in order to guarantee full functionality,
it is recommended that the CONTAINER object is not interacted with directly, and instead interacted with
using the provided methods:

Variable  |Description| Getter method | Setter method
--- | --- | --- | ---
current_fetch | Stores text of a PDB file (or related file, such as .mmol or .ent) | GetFetch() | SetFetch(*fetch*)
ProteinChains | Stores protein chains as listed in a PDB file as a Python dictionary.  ProteinChains[chain][index]-->residue|  GetProteinChains()| SetProteinChains(*proteinChains*)
DNAChains | Stores DNA chains as listed in a PDB file as a Python dictionary.  DNAChains[chain][index]-->residue | GetDNAChains() | SetDNAChains(*dnaChains*)
RNAChains | Stores RNA chains as listed in a PDB file as a Python dictionary.  RNAChains[chain][index]-->residue| GetRNAChains() | SetRNAChains(*rnaChains*)
HETATMChains | Stores HETATM chains as listed in a PDB file as a Python dictionary.  HETATMChains[chain][index]-->residue | GetHETATMChains() | SetHETATMChains(*hetatmChains*)
###Atom Class
A class used to store information about a single atom
####Initialization
Atom(**kwargs)  
kwargs:
 * **number** : *int* Atom number as provided from PDB file. Set using **Atom.SetNumber(num)**
 * **coordinates** *list\<*int(x)* *int(y)* *int(z)*>* XYZ coordinates of atom. Stored as
a Python dictionary as __atomName['x'], __atomName['y'], and __atomName['z']
. Set using **Atom.SetCoordinates(coordinates[3])**
 * **id** : *str* Atom ID as provided from PDB file. Set using **Atom.SetID(id)**
 * **occupancy** : *float* Atom occupancy as provided from PDB file. Set using **Atom.SetOccupancy(occ)**
 * **b_factor** : *float* Atom b_factor as provided from PDB file. Set using **Atom.SetBFactor(bfac)**
 * **element** : *str* Atom element as provided from PDB file. Set using **Atom.SetElement(ele)**
 * **residue** : *str* Atom's parent residue code. Set using **Atom.SetResidue(res)**
 * **extract** : *Bool* Optional argument. When set to false, Atom.element will not be
used to extrapolate the element species. Defaults to True

####Setter notes
***Atom.SetID(id)*** will extrapolate the element species and also set Atom.element
accordingly. This can be prevented by setting the optional argument **extract** to False. Not all
PDB files contain elemental species information.  
*e.g.*  
```
newAtom = Atom.Atom(name='GLY', number='50',id='CA', extract=False)  
#or
newAtom.SetID(newID, **extract=False**)
```
###AminoAcid Class
A class used to organize a group of atoms as an amino acid and provide useful methods.
####Initialization
AminoAcid(**kwargs)  
kwargs:
 * **name** : *str* 3-letter residue code. Set using **AminoAcid.SetName(name)**
 * **number** : *int* residue number as listed in the PDB file. Set using **AminoAcid.SetNumber(num)**
 * **atoms** : *list\<Atom>*list of atoms in the residue. Set using **AminoAcid.SetAtoms(atomList)**

####Setter notes
***AminoAcid.SetName(name)*** will fail and the BAD_NAME flag will be raisedif provided 2 letters or if a 3-letter amino acid code cannot be found.
In order to accommodate rotamers or other situations where the occupancy of several atoms is not 1.00, 3+ letters
are allowed. According to naming conventions, a rotamer must be labeled with some symbol followed a the 3-letter code.   
*e.g.* 
```
AminoAcid.SetName(AGLY)
AminoAcid.SetName(BGLY)<br><br>
```
If a 1-letter code is provided, the name will be converted to a 3-letter code. This is only
possible when editing the name of an amino acid, and not upon initialization (to avoid conflict with
RNA residues). This feature can be disabled by setting the optional argument **set_name** to False, but 
note that functionality of some methods may be lost if a bad name is given  
*e.g.* 
```
1. newAA = AminoAcid(**list_of_kwargs)
2. newAA.SetName(R, set_name=False)
```
If the full name of an amino acid is provided, then the name will be converted to a 3-letter code.
This is only possible when editing the name of an amino acid, and not upon initialization. This feature
can be disabled by setting the optional argument **set_name** to false, but 
note that functionality of some methods may be lost if a bad name is given  
*e.g.*
```
1. newAA = AmindoAcid(**list_of_kwargs)
2. newAA.SetName(Arginine, set_name=False
```
####AminoAcid Methods
#####InsertAtom(atom)
**Input:** Atom object  
**Output:** None  
**Description:** Inserts an atom to to AminoAcid.atoms

#####Flags
Flags can be accessed using *AminoAcid.flags*. The possible flags are as follows:

Flag | Description | Clearing
--- | --- | ---
BAD_NAME | Raised if there is an attempt to name a residue something non-standard | Use AminoAcid.SetName() to assign a valid name
ROT_RES | Raised if a residue has rotamer conformations | Should not be cleared
###RNA Class
A class used to organize a group of atoms as RNA and provide useful methods.
####Initialization
RNA(**kwargs)  
kwargs:
 * **name** : *str* 1-letter residue code. Set using **RNA.SetName(name)**
 * **number** : *int* residue number as listed in the PDB file. Set using **RNA.SetNumber(num)**
 * **atoms** : *list\<Atom>*list of atoms in the residue. Set using **RNA.SetAtoms(atomList)**
####Setter notes
 If the full name of a nucleotide is provided, then the name will be converted to a 1-letter code.
 This is only possible when editing the name of an RNA residue, and not upon initialization. This feature
 can be disabled by setting the optional argument **set_name** to False, but 
 note that functionality of some methods may be lost if a bad name is given  
###DNA Class
A class used to organize a group of atoms as DNA and provide useful methods.
####Initialization
DNA(**kwargs)  
kwargs:
 * **name** : *str* 2-letter residue code. Set using **DNA.SetName(name)**
 * **number** : *int* residue number as listed in the PDB file. Set using **DNA.SetNumber(num)**
 * **atoms** : *list\<Atom>*list of atoms in the residue. Set using **DNA.SetAtoms(atomList)**

####Setter notes
According to the PDB standard, DNA residues are to be listed using the letter "D" plus the 1-letter
residue code. Thus when storing the name of a nucleotide residue in DNA, the letter "D" should
be prepended. If not, the letter "D" will automatically be prepended. This feature can be disabled by 
setting the optional argument **set_name** to False, but note that functionality of some methods may be lost  
*e.g.*
```
newDNAResidue = DNA.DNA(name='G', set_name=False)
newDNAResidue.set_name(G, set_name=False)
```
 If the full name of a nucleotide is provided, then the name will be converted to a 1-letter code.
 This is only possible when editing the name of an RNA residue, and not upon initialization. This feature
 can be disabled by setting the optional argument **set_name** to False, but 
 note that functionality of some methods may be lost if a bad name is given  
###HETATM Class
A class used to organize a group of atoms as a HETATM and provide useful methods.
####Initialization
HETATM(**kwargs)  
kwargs:
 * **name** : *str* HETATM code as provided by PDB. Set using **HETATM.SetName(name)**
 * **number** : *int* group number as listed in the PDB file. Set using **HETATM.SetNumber(num)**
 * **atoms** : *list\<Atom>*list of atoms in the group. Set using **HETATM.SetAtoms(atomList)**




