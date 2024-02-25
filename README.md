# tuya-smart-life-cli

A command-line interface for Smart Life


Usage:

smartlife.py [-v] on|off device_id

Smartlife with no arguments gets a list of all your devices.  It is recommended that you save the output in a file, since there is a limit on how often you can run this command.

Use an id from this file to turn a device on or off.  Scenes can be turned on to run them.

The python script needs to be personalized before running it:

The script needs to store an authorization file.  If you don't have a /tmp directory, change line 31 to specify the file location.

Specify the username and password that you use in the Smart Life app near line 65 in the script.

If you are not in the US, enter your country code near line 67.  Also globally change tuyaus.com to tuyaeu.com for the EU and tuyacn.com for China.  I don't know what is needed for other locations.
