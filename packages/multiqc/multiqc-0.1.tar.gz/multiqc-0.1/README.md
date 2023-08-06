# [<img src="multiqc/templates/default/assets/img/MultiQC_logo.png" width="300" title="MultiQC">](https://github.com/ewels/MultiQC)

**MultiQC is a tool to aggregate bioinformatics results across many samples into
a single report.**

[![Build Status](https://travis-ci.org/ewels/MultiQC.svg?branch=master)](https://travis-ci.org/ewels/MultiQC)

It is written in Python and contains modules for a number of common tools.
Currently, these include:

* [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
* [FastQ Screen](http://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/)
* [Cutadapt](https://code.google.com/p/cutadapt/)
* [Bismark](http://www.bioinformatics.babraham.ac.uk/projects/bismark/)
* [STAR](https://github.com/alexdobin/STAR)
* [Bowtie](http://bowtie-bio.sourceforge.net)
* [Subread featureCounts](http://bioinf.wehi.edu.au/featureCounts/)
* [Picard MarkDuplicates](http://broadinstitute.github.io/picard/)

More to come soon. Please suggest any ideas as a new
[issue](https://github.com/ewels/MultiQC/issues).

## Graphical Usage

MultiQC comes with a graphical app for OS X. To use, download `MultiQC.app.zip`
from the [releases page](https://github.com/ewels/MultiQC/releases)
and unzip the archive. Double click MultiQC.app to launch, then
drag your analysis directory onto the window.

The app can be run from anywhere, though we recommend copying to your
Applications directory.

A similar graphical utility for Windows is planned for a future release.

## Command Line Usage

You can install MultiQC using `pip` as follows: _(submission to PyPi soon!)_

```
pip install git+https://github.com/ewels/MultiQC.git
```

Then it's just a case of going to your analysis directory and running the script:

```
multiqc .
```

That's it! MultiQC will scan the specified directory (`.` is the current dir)
and produce a report detailing whatever it finds.

The report is created in `multiqc_report/multiqc_report.html` by default.
A zip file of the report is also generated to facilitate easy transfer and sharing.

Tab-delimited data files are also created in `multiqc_report/report_data/`,
containing extra information. These can be easily inspected using Excel.

For more detailed instructions, run `multiqc -h`

## Contributions & Support

Contributions and suggestions for new features are welcome, as are bug reports!
Please create a new [issue](https://github.com/ewels/MultiQC/issues) for any
of these, including example reports where possible.

Pull requests with new code are always gladly received, see the
[contributing notes](https://github.com/ewels/MultiQC/blob/master/CONTRIBUTING.md)
for details. These notes include extensive help with how to use the built in code.

If in doubt, feel free to get in touch with the author:
[@ewels](https://github.com/ewels) (phil.ewels@scilifelab.se)

## Version History

#### [v0.1](https://github.com/ewels/MultiQC/releases/tag/v0.1) - 2015-09-01
* The first public release of MultiQC, after a month of development. Basic
structure in place and modules for FastQC, FastQ Screen, Cutadapt, Bismark, 
STAR, Bowtie, Subread featureCounts and Picard MarkDuplicates. Approaching
stability, though still under fairly heavy development.

