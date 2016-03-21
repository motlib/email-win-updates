# email-win-updates

Python script to send notification mails for available Windows
updates.

Usually you will add a call to this script to the task scheduler. 

The script was tested with the standard anaconda 3 environment. A
standard python install should also be fine, if you add the `pyyaml`
package manually.


## Usage

Copy `cfg_template.yaml` to `cfg.yaml` and adapt the settings (sender
and receiver e-mail address, smtp server and port) to your needs.

Then, start the script like this:

  python email-win-updates.py

After a short while, you will receive a mail with the currently
available windows updates. 