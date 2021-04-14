==========================
Accessing the Raspberry Pi
==========================

Using SSH
=========

Since the Raspberry Pi computer is used headless (without a monitor) to 
control the animatronic cougar, one of the easier ways to access the files 
on the Pi is to use SSH. There are various client programs that can be 
used to SSH. Using the SSH extension on VS Code is a good option for this 
because it provides the ability to edit files within VS Code instead of 
having to use a terminal text editor such as VIM or nano.

Using the installed SSH client, the connection can be made with the 
following information: domain, username, and password. How exactly this 
information is used depends on the SSH client.

The domain is the IP address of the Pi on the network it is on. Most likely, 
this will be the IP address of the Pi on BYU's public WiFi. This address 
can be found by pressing on the up arrow of the Pi-Top case until the WiFi 
section is reached. This option will display the Pi's current IP address, 
which takes the form of four numbers separated by periods. Such as: 
"10.37.49.83".

The default username on all Raspberry Pis is "pi". This has not been changed 
on the Pi used for Cosmotron.

The password for the Raspberry Pi being used for Cosmotron is currently 
"pi-top".

Unless the SSH client provides specific fields to enter the needed information 
into, the command to make an SSH connection takes the following form:

``ssh username@ip_address``

Here is an example of what this command could look like for accessing 
Cosmotron's Raspberry Pi:

``ssh pi@10.37.49.83``

The user will be prompted to enter the password following a successful connection.

Using a Monitor
===============

An alternative method that is more user friendly, but requires a bit more hardware 
than what is provided (and assumed to be owned by the user), is to connect the 
Raspberry Pi to monitor and use it as a normal computer. This requires an HDMI 
compatible monitor, an HDMI to Micro HDMI to connect the Pi to the monitor, a mouse, 
and a keyboard.

Ensure the Pi is connected to the monitor before powering it on or else it won't 
start up the user interface to display on the monitor. The keybaord and mouse can be 
plugged in either before or after the Pi is powered on.

After the Pi has been turned on, files can be editted using the local programs such 
as the programming IDE's (Geany and Thonny), the general text editor (Mousepad), 
and command line text editors (nano).