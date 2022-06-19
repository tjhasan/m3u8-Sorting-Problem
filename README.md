# Sorting m3u8 File
This respository holds the source code in order that, when run, will download and sort a target .m3u8 file given a valid attribute to sort by.

## Prerequisites
In order to run this program, you must be using Python `3.9.x` or greater. 

## Usage

### Compliation
Python allows for compilation and execution of a `.py` file via the following command:
```console
foo@bar:~/m3u8-Sorting-Problem/$ python main.py
```

However, in the scenario in which you would like to compile the code without execution, please use the following command:
```console
foo@bar:~/m3u8-Sorting-Problem/$ python -m compileall
```

This will create a director called `__pycache__` which will contain a `.pyc` file. This is the compiled code for the `main.py` file.

If you would like to run the compile code, please use the following command:
```console
foo@bar:~/m3u8-Sorting-Problem/$ python .\__pycache__\<name of compile file>.pyc
```

### Using The Solution
After running the program, you will be prompted twice.

The first prompt will ask for a valid download link. For this program, a link is considered valid if the it would result in downloading a `.m3u8 file.` Any links provided that would *not* result in a `.m3u8` file will be caught and the program will exit after returning an error message.

The second prompt will ask for a valid attribute to conduct the sorting with. An attribute is considered valid if it is one of the following (**not** case-sensitive):
* GROUP-ID 
* NAME 
* LANGUAGE 
* BANDWIDTH 
* AVERAGE-BANDWIDTH 
* CODECS 
* RESOLUTION 
* FRAME-RATE

If an invalid attribute is given, then the program will return an error message and exit.