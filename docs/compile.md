# Self-Compile Guide

## Install Python
Go to [python.org](https://www.python.org/downloads/) and Download any version over version 3.9.\
Anything before this version will cause errors due to one of the packages not supporting anything lower than `python3.9`.

If you are on Linux, you'll most likely need to deliberately install `python3.9` and `pip3`.

## Download Code
You may choose to `git clone` or directly download using your browser. Either way will work.

## Install Dependencies
Depending on your operating system, the installed python commmand can be different.\
Some systems use `pip` and some use `pip3`.

For most cases, `pip` is used on Windows while `pip3` is used on most Linux installations.\

Install requirements using the following command:\
`pip3 install -r requirements.txt` or `pip install -r requirements.txt`

## Running
You can now run `runner.py`.\
I would recommend building as this may improve resource usage.

## Building
To build, install `nuitka` using `pip` or `pip3`.\
After doing so, enter the following:

`nuitka --onefile runner.py`

This packages it into 1 executeable with no prior installation requirements.\
Keep in mind, compiling this may take some time but is ultimately based on your CPU.