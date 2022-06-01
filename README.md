<h1>Advanced Protein Analysis Library</h1>
<p>A library to provide tools useful for advanced protein analysis.</p>
<p>Note that this README is temporary, and only contains limited information while
while everything is still in development.</p>

<h2>Required Packages:</h2>
<ul>
 <li>numpy</li>
</ul>
<h2>Top Level Methods</h2>
<h3>apalib.VectorPair(residue1, residue2)</h3>
<p>Returns a tupule containing the z_difference for two residues, the x_intercept in 3D space for the first residue, and
the x_intercept in 3D space for the second residue.</p>
<p>Example</p>
<pre><code>import apalib
pdb = apalib.PDB()
pdb.Fetch('5u59')
res_one = pdb.Contents().GetPeptideChains()['A'][1]
res_two = pdb.Contents().GetPeptideChains()['A'][2]
val = apalib.VectorPair(res_one, res_two)
</code></pre>
<h3>apalib.GetCentAngle(residue1, residue2, rad = True)</h3>
<p>Returns the angle made by <code>residue1.centroid</code> --> <code>residue1.CA</code> --> <code>residue2.CA</code>.
If <code>rad</code> is set to <code>True</code>, then the result will be in radians. Otherwise it will be in degrees</p>
<h3>apalib.CheckIsForward(residue, point)</h3>
<p>Returns true if a residue-vector points forwards towards a point. In other words, given a vector v = k&lt a,b,c > made from
<code>residue.CA --> residue.centroid</code> and some point p = (x,y,z), this method will return true if k is positive.</p>
<h3>GetDist(atom1, atom2)</h3>
<p>Returns the distance between two atoms</p>
<h2>PDB class</h2>
<p>Class used for reading and parsing <code>.pdb</code> files. Because other similar file extensions exist, there is
no check that a file is a <code>.pdb</code> file.</p>

<h3>Methods</h3>
<h4>pdb.Read(<em>filepath</em>)</h4>
<p>Reads and parses a pdb file from your local computer. Stores information in the 
pdb object's <code>container</code></p>
<p>Example:</p>
<pre><code>import apalib
pdb = apalib.PDB()
pdb.Read(r"C:\Users\username\Documents\1j1j.pdb")</code></pre>
<h4>pdb.Fetch(<em>pdb_code</em>)</h4>
<p>Fetches and parses a pdb file directly from the <em>Protein Databank</em>. Stores
information in the pdb object's <code>container</code></p>
<p>Example:</p>
<pre><code>import apalib
pdb = apalib.PDB()
pdb.Fetch("5u59")</code></pre>
<h4>pdb.Contents()</h4>
<p>Gets the pdb object's <code>Container</code>.</p>

<h2>Container class</h2>
<p>Class used for storing fetched or read information from a <code>.pdb</code> file.</p>
<p>This class contains several useful variables and is primarily paired with the above <code>pdb</code>class</p>
<table>
  <tr>
    <th>Variable</th>
    <th>Description</th>
    <th>Getter Method</th>
    <th>Setter Method</th>
    <th>Clear Method</th>
  </tr>
  <tr>
    <td>Fetch</td>
    <td>Contains the raw input string from a fetch or read.</td>
    <td>Container.GetFetch()</td>
    <td>Container.SetFetch()</td>
    <td>Container.ClearFetch()</td>
  </tr>
  <tr>
    <td>PeptideChains</td>
    <td>Contains a dictionary of all amino acid residues from a fetch</td>
    <td>Container.GetPeptideChains()</td>
    <td>Container.SetPeptideChains()</td>
    <td>Container.ClearPeptideChains()</td>
  </tr>
  <tr>
    <td>DNAChains</td>
    <td>Contains a dictionary of all DNA residues from a fetch</td>
    <td>Container.GetDNAChains()</td>
    <td>Container.SetDNAChains()</td>
    <td>Container.ClearDNAChains()</td>
  </tr>
  <tr>
    <td>RNAChains</td>
    <td>Contains a dictionary of all RNA residues from a fetch</td>
    <td>Container.GetRNAChains()</td>
    <td>Container.SetRNAChains()</td>
    <td>Container.ClearRNAChains()</td>
  </tr>
  <tr>
    <td>HETATMChains</td>
    <td>Contains a dictionary of all HETATM residues from a fetch</td>
    <td>Container.GetHETATMChains()</td>
    <td>Container.SetHETATMChains()</td>
    <td>Container.ClearHETATMChains()</td>
  </tr>
</table>
<h3>Other Methods</h3>
<h4>Container.ClearAll()</h4>
<p>Clears all data from and reinitializes a <code>Container</code> object</p>
<h4>Container.AsList(ordered=True)</h4>
<p>Returns a list containing all residues from all chains stored in a <code>Container</code> object. If <code>
ordered</code> is set to <code>True</code>, then the returned list will be ordered numerically from the residue
number as it appears in its associated PDB file.</p>