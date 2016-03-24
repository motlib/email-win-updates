email-win-updates
=================

This is a python script to send notification mails for available
Windows updates.

Usually you want to call this script from a task in the Windows task
scheduler.

The script was tested with the Anaconda Python 3.5 environment without
any additional packages installed. A plain python 3.5 install should
also be fine, if you add the `pyyaml` package manually.


License
=======

The script is licensed under the GPL version 3. See ``LICENSE`` file
for details. 


Usage
=====

Copy `cfg_template.yaml` to `cfg.yaml` and adapt the settings (sender
and receiver e-mail address, smtp server and port) to your needs.

Then, start the script like this::

  python email-win-updates.py

After a short while, you will receive a mail with the currently
available windows updates. 
