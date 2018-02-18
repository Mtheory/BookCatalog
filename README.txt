Book Catalog is a RESTful web application using the Python framework Flask that provides a list of genre-categories that contain information about specific books. The application provides JSON endpoints.
Only logged users are able to add/edit/delete records.
User authentication is provided by third-party OAuth authentication by google.

Installation :

Python 2        https://www.python.org/download/releases/2.7/

Virtual Machine
VirtualBox		https://www.virtualbox.org/wiki/Downloads
VirtualBox is the software that runs the VM.
Install the *platform package* for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

**Ubuntu 14.04 Note:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a [reported bug](http://ubuntuforums.org/showthread.php?t=2227131), installing VirtualBox from the site may uninstall other software you need.

Vagrant			https://www.vagrantup.com/downloads.html
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Install the version for your operating system.

**Windows Note:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

Fetch the Source Code and VM Configuration

VM configuration files for vagrant directory:
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip

Clone the BookCatalog from https://github.com/Mtheory/BookCatalog.git


Running

Run the virtual machine
Using the terminal, then type **vagrant up** to launch your virtual machine.
Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.  Change to the /vagrant directory by typing **cd /vagrant**. This will take you to the shared folder between your virtual machine and host machine.

Ensure that you are inside the directory that contains project.py, database_setup.py, and two directories named 'templates' and 'static'

Now type **python database_setup.py** to initialize the database.

Type **python populate_catalog.py** to populate the database with.
(Optional)

Run your application within the VM (python /vagrant/Book Catalog/project.py)
Access and the application by visiting http://localhost:8000 locally

Type **python project.py** to run the Flask web server. In your browser visit **http://localhost:8000** to view the BookCatalog menu app.  You should be able to view, add, edit, and delete menu items and Book Catalog when you log in.
