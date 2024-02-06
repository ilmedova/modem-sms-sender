# Configure to run on Ubuntu

Yes, running your script with a process manager like Supervisor is a recommended approach for running it as a background service. Supervisor provides features such as process control, automatic restarts, and managing script execution on system boot.

Here's an example configuration for running your Python script with Supervisor:

Install Supervisor (if not already installed):

```
sudo apt-get install supervisor
```
Create a Supervisor configuration file for your script. For example, create a file named your_script.conf in the /etc/supervisor/conf.d/ directory:

```
sudo nano /etc/supervisor/conf.d/your_script.conf
```
Add the following configuration to the file, replacing your_script.py with the actual filename and the path to your script:

```
[program:your_script]
command=python /path/to/your_script.py
directory=/path/to/your_script_directory
user=your_username
autostart=true
autorestart=true
stderr_logfile=/var/log/your_script.err.log
stdout_logfile=/var/log/your_script.out.log
Note: Replace your_username with the appropriate username.
```

Save the file and exit the text editor.

Update Supervisor to read the new configuration:

```
sudo supervisorctl reread
```
Start your script as a supervised process:

```
sudo supervisorctl start your_script
```
Supervisor will now manage your script as a background service. You can check the status of your script with the following command:

```
sudo supervisorctl status your_script
```
To stop the script, use the following command:

```
sudo supervisorctl stop your_script
```
Supervisor will automatically start your script on system boot and handle process management, ensuring that it keeps running even if it crashes or encounters errors.


# Running on Ubuntu for testing on your local machine

Create and activate a virtual environment:

```
python3 -m venv myenv         # Create a virtual environment
source myenv/bin/activate    # Activate the virtual environment
```
Install the required packages from the requirements.txt file:

```
pip install -r requirements.txt
```
Once the virtual environment is activated and the dependencies are installed, you can run your code:

```
python modem.py
```
