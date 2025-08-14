Documentation
=============
This is the documentation for the [MATLAB](https://github.com/RascalSoftware/RAT) and [Python](https://github.com/RascalSoftware/python-RAT) versions of the RAT project. The installation instruction provided here, assumes [conda](https://docs.conda.io/) is used to manage python packages, please adapt as needed for a different package manager.

Build docs
----------
The documentation should be built using the provided Sphinx make file. The reStructuredText source is in the source 
folder while the build will be placed in a build folder. The build requires a python executable and the python packages 
in the requirements.txt. You need MATLAB version and python version or RAT software installed in your system.

```bash
   conda create -n RAT python=3.9
   conda activate RAT
   pip install -r requirements.txt
```

You also must have `pandoc` installed to build the Python example Jupiter notebooks. See the installation instructions [here](https://pandoc.org/installing.html). If not previously installed system-wide, install [pandoc](https://pandoc.org/) using [conda](https://docs.conda.io/) as described in their [installation manual](https://pandoc.org/installing.html#conda-forge)
depending on [conda](https://docs.conda.io/) flavour you are using.

If you do not have RAT code on your machine, download the appropriate version of RAT from the GitHub [release](https://github.com/RascalSoftware/RAT/releases) page, and unzip the contents into a folder called API (This folder should be located within RAT-documentation directory, alongside the **source** folder and main `make.bat` file (see below)). For example on a Linux machine, the nightly can be downloaded as shown:

```bash
    cd path_to_rat_docs_folder
    wget https://github.com/RascalSoftware/RAT/releases/download/nightly/Linux.zip
    unzip Linux.zip -d API/
```

Where `path_to_rat_docs_folder` is the location where documentation is cloned or unpacked.
If RAT is already present, you may create symbolic link to the existing` RAT` directory, e.g.:

for Windows:

    cd path_to_rat_docs_folder  
    mklink /j API path_to_matlab_rat_folder
    
for linux/macOS:

```bash
   cd path_to_rat_docs_folder
   ln -s path_to_matlab_rat_folder  API
```

Where `path_to_rat_docs_folder` is the path to the RAT documentation repository and `path_to_matlab_rat_folder` is the path to the downloaded MATLAB RAT release
    
[Python RAT API](https://github.com/RascalSoftware/python-RAT)  should be installed on the same python virtual environment created earlier. Build process adds modules necessary for generating python documentation to the python modules search path. Look at [Python RAT repository](https://github.com/RascalSoftware/python-RAT/blob/main/README.md) for more information on how to build python API.

To build the HTML docs, type the following into a terminal with access to the Python executable:  

    make html

[`matlabengine`](https://pypi.org/project/matlabengine/) is required to generate MATLAB code snippet outputs. If `matlabengine` is not installed, the outputs will be omitted and the following warning will be printed in the terminal:

    UserWarning: Could not create output as MATLAB engine was not available

If the MATLAB code outputs are needed, install the appropriate `matlabengine` for your installed MATLAB

    pip install matlabengine
