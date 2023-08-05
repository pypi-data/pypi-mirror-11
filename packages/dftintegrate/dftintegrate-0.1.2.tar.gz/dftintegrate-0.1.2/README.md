# dftintegrate

### Installation
Python3 support only. The way I do it that is easiest for me is to use a
virtual environment. If this is unfamiliar to you follow
[this link](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
At the command line I type: 
`mkvirtualenv --python=/usr/local/bin/python3 nameOfEnvironment`.
This is assuming you followed the virtualenvwrapper part of the link above.
The path to the python3 executable might be different for you. You can find out
what yours is by typing `which python3` at the command line. Doing all of this
creates an environment where python3 is default, so if I type python it launches
python 3.4.x. Now that I have and am working in this environment I type
`pip install dftintegrate` and I'm done!

### Basic Overview
If you have a directory that contains VASP output (or Quantum Espresso in the
future version), you can use dftintegrate to analyze data related to the electron
bands. The data that can be read includes the irreducible kpoints, corresponding
eigenvalues for all bands calculated, and symmetry operators with translations.
The electron bands can also be represented with a Fourier basis. That repersentation
can be integrated with rectangles or Gaussian quadrature. Convergence tests can be
run that compare the convergence of rectangles to Gauss.

### Examples
1. Fit VASP data with Fourier Series. ```dftintegrate -vasp -fit``` Note,
this will simply produce some json data files, namely data.json and fit.json.
Some intermediate files will also be created for the programs sake namely
kmax.dat, kpts\_eigenvals.dat, and symops\_trans.dat.
2. Integrate VASP data with rectangles and Gaussian Quadrature.
```dftintegrate -vasp -integrate``` Note, this will produce integral.json.
3. You only need to specify which DFT code was used if you need to create
a data.json. If the json files needed already exsist and a DFT code was
specified, the DFT code specifier will be ignored. ```dftintegrate -fit```
  1. Assuming I have a data.json I can just say -fit and it will use the
data.json. The only files that are over written are the ones that correspond
to a flag. If fit is specified, fit.json will be over written but data.json
will not be, if it exsists it is used.
  2. Assuming there is no data.json an error will be raised saying I need to
specify a DFT code.
  3. Look at Example 1, if there is already a data.json the vasp flag is ignored.
4. You can run a convergence test comparing integration with rectangles to
integration with Gaussian quadrature. ```dftintegrate -vasp -converge -points 10```
This will integrate the Fourier representation with 1 integration point,
2 points, 3, ..., 10. Then plot how fast each technique converges to the right answer.

### Note on kmax and KPOINTS
Because we are creating a fit out of data
points we run up against the Nyquist frequency, meaning we can only
have so high of a frequency in our Fourier representation based on how
many data points we have. For this this reason the kmax variable
exists. It is pulled from the KPOINTS file. The problem is the VASP
user has a few ways of formatting their KPOINTS file. If the fourth
line is the specification of the size of kgrid ie 12 12 12 then
everything will work fine. Note it can ONLY be the three numbers, no
comment after If not the user will need to make their KPOINTS file
look like that or they can make kmax.dat. If 12 12 12 was the grid
than kmax = ceil(12/(2*sqrt(3))). dftintegrate automatically uses
files if they exist so creating kmax.dat by hand will work.
