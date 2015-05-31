#!/usr/bin/env python

"""
notifymail

Send emails to a preconfigured address.
"""

import codecs
from email.mime.text import MIMEText
from getpass import getpass
import json
from optparse import OptionParser
import os.path
import smtplib
import sys

try:
    # Fix Python 2.x
    input = raw_input
    bytes = str
except NameError:
    pass

# -----------------------------------------------------------------------------

def probe(_test_config=None):
    """
    Attempts to login to the configured mail server.
    Returns silently upon success.
    
    Raises an exception if the mail server could not be reached or
    if there was an authentication failure.
    """
    
    send('', '', _test_config=_test_config or _config)

def send(subject, body, from_name=None, _test_config=None):
    """
    Sends a notification email with the specified subject, body, and (optional)
    sender name.
    
    Arguments:
    * subject : unicode|bytes<utf-8>    Subject of the email to send.
    * body : unicode|bytes<utf-8>       Body of the email to send.
    * from_name : unicode|bytes<utf-8>  Sender name to use.
                                        Overrides configuration options.
    """
    
    # Force arguments to Unicode
    subject = _force_to_unicode(subject)
    body = _force_to_unicode(body)
    from_name = _force_to_unicode(from_name)
    
    # Load configuration
    if _test_config is None:
        config = _config        # global
    else:
        config = _test_config
    
    # Extract configuration elements
    hostname = config['smtp_hostname']
    port = config['smtp_port']
    tls = config['smtp_uses_tls']
    username = config['smtp_username']
    password = config['smtp_password']
    from_address = config['from_address']
    if from_name is None:
        from_name = config['from_name']
        if len(from_name) == 0:
            from_name = from_address
    to_address = config['to_address']
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = u'%s <%s>' % (from_name, from_address)
    msg['To'] = to_address
    msg['Subject'] = subject
    
    smtp = smtplib.SMTP(hostname, port)
    if tls:
        smtp.starttls()
    
    smtp.ehlo()
    smtp.login(username, password)
    if _test_config is None:
        smtp.sendmail(from_address, to_address, msg.as_string())
    smtp.quit()

def _force_to_unicode(bytes_or_unicode):
    if type(bytes_or_unicode) == bytes:
        bytes_or_unicode = bytes_or_unicode.decode('utf-8')
    return bytes_or_unicode

# -----------------------------------------------------------------------------

def _load_config(interactive=False, force_setup=False):
    home_dirpath = os.path.expanduser('~')
    config_filepath = os.path.join(home_dirpath, '.notifymailrc')
    
    # Ensure configured
    if not os.path.exists(config_filepath) or force_setup:
        if not interactive and not force_setup:
            raise ImportError(
                'notifymail has not been configured. ' +
                'Please run "notifymail setup".')
        
        config = {}
        config['smtp_hostname'] = _input_string(
            'SMTP Server Hostname: ')
        config['smtp_port'] = _input_int(
            'SMTP Server Port [465]: ', 465)
        config['smtp_uses_tls'] = _input_bool(
            'SMTP Server Uses TLS (y/n) [n]: ', False)
        config['smtp_username'] = _input_string(
            'SMTP Username: ')
        config['smtp_password'] = _input_string(
            'SMTP Password: ', password=True)
        config['from_address'] = _input_string(
            'From Address [%s]: ' % config['smtp_username'],
            config['smtp_username'])
        config['from_name'] = _input_string(
            'From Name (optional) []: ', '')
        config['to_address'] = _input_string(
            'To Address: ')
        
        print('')
        sys.stdout.write('Verifying connection to SMTP server... ')
        sys.stdout.flush()
        try:
            probe(_test_config=config)
        except:
            print('')
            raise
        print('OK')
        
        with codecs.open(config_filepath, 'w', 'utf-8') as config_file:
            json.dump(config, config_file, sort_keys=True, indent=4,
                separators=(',', ': '))
    
    # Load and return configuration
    with codecs.open(config_filepath, 'r', 'utf-8') as config_file:
        return json.load(config_file)

def _input_string(prompt, default='', password=False):
    if password:
        line = getpass(prompt)
    else:
        line = input(prompt)
    if len(line) == 0:
        return default
    else:
        return line

def _input_int(prompt, default):
    try:
        return int(input(prompt))
    except ValueError:
        return default

def _input_bool(prompt, default):
    line = input(prompt)
    if len(line) == 0:
        return default
    if line.lower()[0] == 'y':
        return True
    if line.lower()[0] == 'n':
        return False
    return default

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    # Run as a command-line program
    
    # Parse arguments
    parser = OptionParser(
        usage='%prog --setup | -s SUBJECT [-b BODY] [--from-name NAME] | --probe')
    parser.add_option(
        '--setup', action="store_true", dest="setup",
        help='setup mail server configuration')
    parser.add_option(
        '--probe', action="store_true", dest="probe",
        help='check whether mail server is reachable')
    parser.add_option(
        '-s', '--subject', dest='subject',
        help='subject line. Required.',
        metavar='SUBJECT')
    parser.add_option(
        '-b', '--body', dest='body',
        help='body. Read from standard input if omitted.',
        metavar='BODY')
    parser.add_option(
        '--from-name', dest='from_name',
        help='sender name. Overrides the default sender name.',
        metavar='NAME')
    (options, args) = parser.parse_args()
    
    if options.setup:
        try:
            _load_config(force_setup=True)
        except KeyboardInterrupt:
            # Ignore
            print('')
    elif options.probe:
        _config = _load_config(interactive=sys.stdin.isatty())
        probe()
    elif args != [] or options.subject is None:
        parser.print_help()
    else:
        # More argument parsing
        if options.body is None:
            options.body = sys.stdin.read()
        
        _config = _load_config(interactive=sys.stdin.isatty())
        send(options.subject, options.body, from_name=options.from_name)
else:
    # Imported from Python script
    _config = _load_config(interactive=False)
