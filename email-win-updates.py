'''Script to check for windows updates and send mail with results.

Modify the cfg dictionary below to configure the script.'''


__docformat__ = 'ReStructuredText'
__author__ = 'Andreas Schroeder <andreas@a-netz.de>'


from email.mime.text import MIMEText
import logging
import os
import smtplib
import textwrap
import win32com.client as win32
import yaml


cfg = None

def get_updates(search_crit):
    '''Get a list of available windows updates.'''
    
    updateSession = win32.gencache.EnsureDispatch("Microsoft.Update.Session")
    updateSearcher = updateSession.CreateUpdateSearcher()
    
    searchResult = updateSearcher.Search(search_crit)

    return searchResult.Updates


def send_no_updates_mail():
    '''Send mail with info about no available updates.'''
    
    body = 'Checking for updates was successful. \n' \
           'There are currently no updates to install.'

    send_mail(body)


def send_updates_list_mail(updates):
    '''Send mail with list of available updates.'''
    
    body = 'The following windows updates are available:\n\n'

    for update in updates:
        body += '* {sev]: {title}\n'.format(
            sev=update.MsrcSeverity.upper(),
            title=update.Title)
        body += textwrap.fill(
            update.Description,
            width=70,
            initial_indent='  ',
            subsequent_indent='  ')
        body += '\n\n'

    send_mail(body)

    
def send_update_check_error_mail(ex):
    '''Send mail with update check error info.'''
    
    body = 'Failed to check for windows updates:\n'
    body += str(ex)
    
    send_mail(body)
    

def send_mail(body):
    '''Compose and send the info mail.'''
    
    global cfg
    
    title = 'Windows Update check for {dom}\{comp}\n\n'.format(
        dom=os.getenv('USERDOMAIN'),
        comp=os.getenv('COMPUTERNAME'))

    text = title
    text += body
    text += '\n\nSee http://github.com/motlib/email-win-updates for more info.'
    
    msg = MIMEText(text)

    msg['Subject'] = title
    msg['From'] = cfg['from']
    msg['To'] = cfg['to']

    s = smtplib.SMTP(cfg['server'], port=cfg['port'])
    s.send_message(msg)
    s.quit()
    

def main():
    '''Program entry point. 

    Search for updates and send out mail with result.'''
    
    global cfg

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: win_update_check: %(message)s')
    
    logging.info('Searching for updates...')

    try:
        with open('cfg.yaml', 'r') as f:
            cfg = yaml.load(f)
        
        # Check for updates
        updates = get_updates(cfg['search_criteria'])

        if len(updates) == 0 and cfg['no_updates_mail']:
            # Send mail to tell about no updates available.
            send_no_updates_mail()
        else:
            # send list of updates
            send_updates_list_mail(updates)
            
    except Exception as ex:
        send_update_check_error_mail(ex)
        logging.exception('Failed to check for windows updates')

    logging.info('Check for updates completed.')
    
        
if __name__ == '__main__':
    main()
