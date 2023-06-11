# Encrypt the code

expire after 30 days:
```
pyarmor gen -O dist4 -e 30 modem.py
```

expire date is 2020-12-31:
```
pyarmor gen -O dist4 -e 2020-12-31 modem.py
```


# Windows configs

In Windows, you can use the "Task Scheduler" feature to run your Python script as a background service. Here's a step-by-step guide on how to set it up:

Open the Task Scheduler by pressing "Win + R" to open the Run dialog, then type taskschd.msc and press Enter.

In the Task Scheduler, click on "Create Basic Task" or "Create Task" in the Actions pane on the right.

Follow the wizard to configure the task:

Give it a name and an optional description.
Choose "Run whether the user is logged on or not" and check the box for "Run with highest privileges" if required.
Select "Start a program" as the action.
In the Program/script field, provide the path to the Python interpreter (e.g., C:\Python39\python.exe).
In the "Add arguments" field, specify the path to your Python script (e.g., C:\path\to\your\script.py).
Configure any other settings as needed (e.g., triggers, schedules).

Click "Finish" to create the task.

The task will now be scheduled to run in the background according to the specified settings. You can further manage and modify the task using the Task Scheduler.

Note: Ensure that you have the correct Python interpreter installed on your Windows system and that the required modules are available for your script to run successfully.


# Ubuntu configs

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


#Running on ubuntu for test

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