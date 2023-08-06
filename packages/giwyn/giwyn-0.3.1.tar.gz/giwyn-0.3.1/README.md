# Giwyn

Giwyn (for *Giwyn is what you need*) is a software to manage all your git clones, stored in your own computer.  
Giwyn will scan your computer to search all ```.git``` directories, to list them in an hidden configuration file (```.git_project.txt```, in your **HOME** directory) and allows you to manage all of them with one simple command.

# Usage

Steps:

0.  First time, let ```giwyn``` scan your computer **from a specific directory** (like *~* for your **HOME** directory) by this command : ```giwyn --scan the_directory_you_want_to_scan```.  *This step can take a while...*  
1.  After that, you can use some commands to specify what ```giwyn``` has to do : list all your git projects and their properties, to verify if your commits has to be push, etc...  

If you don't ask to Giwyn to scan your repository again, Giwyn will work only on git repositories saved in the hidden configuration file.  
Also, if Giwyn see that a git repository is deleted, he will automatically remove the link from the hidden configuration file.

# Options

* ```--help```, ```-h``` : print the help
* ```--scan```, ```-s``` : scan your entire repository from your **HOME** directory, or another specified directory, and append the result of this command in the hidden configuration file
* ```--rescan```, ```'rs``` : **replace** data in your hidden configuration file by the result of the scan from your **HOME** directory, or another specified directory
* ```--list```, ```-l``` : list all your git repositories, stored in the hidden configuration file
* ```--push```, ```-p``` : push all your clean git repositories
* ```--version```, ```-v``` : version of the software (for pip)
* ```--debug```, ```-d``` : allow the debug mod

# Installation

With pip3 : ```sudo pip3 install giwyn```

# Main developer

Carette Antonin

# Contributors

* John Doe

# Contact

Carette Antonin - antonin.carette[at]gmail[dot]com
