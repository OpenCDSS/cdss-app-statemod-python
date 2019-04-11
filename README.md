## StateMod-Python ##

CDSS prototype of StateMod written in Python

* [Introduction](#introduction)
* [Repository Contents](#repository-contents)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [Maintainers](#maintainers)
* [License](#license)
* [Contact](#contact)

## Introduction ## 

## Repository Contents ##

The following folder structure is recommended for development.
Top-level folders should be created as necessary.
The following folder structure clearly separates user files (as per operating system),
development area (`cdss-dev`), product (`StateMod-Python`), repositories for product (`git-repos`),
and specific repositories for the product.
Repository folder names should agree with GitHub repository names.
Scripts in repository folders that process data should detect their starting location
and then locate other folders based on the following convention.

```
C:\Users\user\                                 User's home folder for Windows.
/c/Users/user/                                 User's home folder for Git Bash.
/cygdrive/C/Users/user/                        User's home folder for Cygwin.
/home/user/                                    User's home folder for Linux.
  owf-cdss/                                    Projects that are part of Colorado's Decision Support Systems.
    StateMod-Python/                               StateMod C# product folder.
                                               (name of this folder is not critical).
      ---- below here folder names should match exactly ----
      git-repos/                               Git repositories for the Angular portal web application.
        cdss-app-statemod-python/              Statemod Python main application code (this repo).
        cdss-lib-cdss-python/                  Library shared between CDSS components.
        cdss-lib-common-python/                Library of core utility code used by multiple repos.
        cdss-lib-models-python/                Library to read/write CDSS StateCU and StateMod  model files.
```

This repository contains the following:
```
cdss-app-statemod-cs
   .git/                                       Standard Git software folder for repository (DO NOT TOUCH).
   .gitattributes/                             Standard Git configuration file for repository (for portability).
   .gitignore/                                 Standard Git configuration file to ignore dynamic working files.
   README.md                                   This readme file
   LICENSE.md                                  StateMod Java license file.
```

## Getting Started ##

## Contributing ##

Contributions to this project can be submitted using the following options:

1. StateMod Python software developers with commit privileges can write to this repository
  as per normal OpenCDSS development protocols.
2. Post an issue on GitHub with suggested change.  Provide information using the issue template.
3. Fork the repository, make changes, and do a pull request.
  Contents of the current master branch should be merged with the fork to minimize
  code review before committing the pull request.

See also the [OpenCDSS / StateMod protocols](http://learn.openwaterfoundation.org/cdss-website-opencdss/statemod/statemod/).

## Maintainers ##

* Justin Rentie, Open Water Foundation ([@jurentie](https://github.com/jurentie))
* Steve Malers, Open Water Foundation ([@Smalers](https://github.com/smalers))

## License ##

Copyright Colorado Department of Natural Resources.

The software is licensed under GPL v3+. See the [LICENSE.md](LICENSE.md) file.

## Contact ##

See the [OpenCDSS StateMod information for product contacts](http://learn.openwaterfoundation.org/cdss-website-opencdss/statemod/statemod/#product-leadership).