All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 * Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.

 * Neither the name of the Natural Capital Project nor the names of
   its contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description: .. default-role:: code
        
        RIOS: Resource Investment Optimization System |build_image|
        ===========================================================
        
        .. |build_image| image:: http://builds.naturalcapitalproject.org/buildStatus/icon?job=natcap.rios
          :target: http://builds.naturalcapitalproject.org/view/Bitbucket%20builds/job/natcap.rios/
        
        This repository is for RIOS 1.1.4 and later which replaces our Google Code project formerly located at http://code.google.com/p/invest-natcap.water-funds.
        
        About RIOS
        ==========
        
        RIOS (Resource Investment Optimization System)  is a free and open source
        software tool that supports the design of cost-effective investments in
        watershed services.
        
        RIOS provides a standardized, science-based approach to watershed management in
        contexts throughout the world. It combines biophysical, social, and economic
        data to help users identify the best locations for protection and restoration
        activities in order to maximize the ecological return on investment, within the
        bounds of what is socially and politically feasible.
        
        RIOS was developed through an extensive stakeholder engagement process,
        including input from more than 11 water funds (watershed investment programs)
        across Latin America. The tool has been tested in diverse ecological, social and
        political contexts. Early applications in the Cauca Valley of Colombia resulted
        in RIOS-designed watershed investments up to six times more effective than
        typical investment approaches. RIOS enables watershed investors to use a
        replicable, transparent, and stakeholder-driven approach to evaluate projects
        within a region or between regions, making it easier to track the places where
        their investments are most needed and most effective.
        
        Questions RIOS can answer
        -------------------------
        
        * Which set of watershed investments (in which activities, and where) will yield the greatest returns towards multiple objectives?
        
        * What change in ecosystem services can I expect from these investments?
        
        * How do the benefits of these investments compare to what would have been achieved under an alternate investment strategy?
        
        RIOS Dependencies
        ===================
        RIOS relies on the following python packages:
          * numpy
          * scipy>=0.13.0
          * gdal
          * pygeoprocessing>=0.3.0a3
          * pyqt4
        
        
        Release History
        ===============
        
        1.1.8 (2015/08/11)
        ------------------
        
        * Fixed a bug that causes a PORTER crash when no ag or restoration transitions occur in IPA.
        * Fixed internal import and pyinstaller errors that caused headaches when working on a local source branch.
        
        1.1.7 (2015/08/07)
        ------------------
        
        * Validating lulc coefficients table to ensure there is a field called 'description'.  If left out this caused a case where IPA ran normally but PORTER would crash looking for that field.
        
        1.1.6 (2015/07/30)
        ------------------
        
        * Patch to fix an issue where RIOS PORTER didn't launch and possibly an ImportError on "_superlu" on some machines.
        
        1.1.5 (2015/07/17)
        ------------------
        
        * Hotfix to rearrange references to RIOS Preprocessing tools on select RIOS IPA objective models.
        
        1.1.4 (2015/07/17)
        ------------------
        
        Previous releases of InVEST were from a Google Code site but was migrated in June 2015.  This is the first release of RIOS in less than ad hoc project structure.
        
        * Restructured and refactored this repository from the one we used to have on
          Google code.
        * Uses paver to handle builds, distribution, and archival of sample data.
        * Uses pyinstaller to build frozen exes.
        * Removed ArcGIS preprocessing toolbox and documentation from the installer since it was awkward for users to visit C:\Program Files\rios
        * Updates to user interface for documentation and ArcGIS preprocessing links.
        * Created a single command line interface to launch IPA and PORTER named rios_cli_{version}.exe
        * Updated shortcut links in start menu to show the version of RIOS to be launched.
        
Keywords: RIOS
Platform: UNKNOWN
Classifier: Intended Audience :: Developers
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Science/Research
Classifier: Natural Language :: English
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft
Classifier: Operating System :: POSIX
Classifier: Programming Language :: Python :: 2 :: Only
Classifier: Topic :: Scientific/Engineering :: GIS
