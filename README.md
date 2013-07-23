# notifymail

`notifymail` allows scripts to send email to a preconfigured address. It is particularly useful for unattended and scheduled scripts to report their status to an administrator.

`notifymail` is designed to be very easy to install and use. I wrote it because I couldn't figure out how to configure the built-in `sendmail` command to forward emails appropriately and I couldn't get the similar `ssmtp` package to work.

## Requirements

* OS X or Linux
* Python 2.6 or 2.7
* An email account

## Installation

```
$ pip install notifymail
```

## Configuration

You must know the SMTP settings of your email provider, which can typically looked up on your provider's website. For example here are [Gmail's SMTP settings](https://support.google.com/mail/troubleshooter/1668960?hl=en#ts=1665119,1665162), obtained with a internet search for "gmail SMTP settings":

<table>
  <tr>
    <th>SMTP Server</th>
    <td>smtp.gmail.com</td>
  </tr>
  <tr>
    <th>SMTP Port</th>
    <td>587 (for TLS)</td>
  </tr>
  <tr>
    <th>SMTP Uses TLS?</th>
    <td>yes</td>
  </tr>
</table>

Usually your SMTP username will be the same as your email address, and your SMTP password will be the same as your email password.

Once you have the settings in hand, run the `notifymail --setup` command:

```
$ notifymail --setup
SMTP Server Hostname: smtp.gmail.com
SMTP Server Port [465]: 587
SMTP Server Uses TLS [no]: yes
SMTP Username: robot@gmail.com
SMTP Password: ********
From Address [robot@gmail.com]: robot@gmail.com
From Name (optional) []: notifymail
To Address: admin@example.com

Verifying connection to SMTP server... OK
```

## Usage

### From the Command Line

```
$ echo "Hello World" | notifymail -s "Subject"
```

`notifymail` will read the message body from standard input and allow you to specify a subject line with the `-s` option. You may also specify a custom sender name using the `--from-name` option.

The encoding of the message body and all arguments is assumed to be UTF-8.

Full usage information:

```
Usage: notifymail.py --setup | -s SUBJECT [-b BODY] [--from-name NAME]

Options:
  -h, --help            show this help message and exit
  --setup               
  -s SUBJECT, --subject=SUBJECT
                        subject line. Required.
  -b BODY, --body=BODY  body. Read from standard input if omitted.
  --from-name=NAME      sender name. Overrides the default sender name.
```

### From a Python Script

```
import notifymail
notifymail.send("Subject", "Hello World")
```

String arguments can be either Unicode strings or UTF-8 encoded bytestrings.

### From a Non-Python Script

Just execute the `notifymail` command using your language's normal API for running system commands.

For example, in Ruby:

```
Open3.popen3(['notifymail', '-s', 'Subject']) {|stdin, stdout, stderr, wait_thr|
  stdin.puts('Hello World!')
  stdin.close
  
  exit_code = wait_thr.value.to_i
  if exit_code != 0
    raise "notifymail exited with error code #{exit_code}."
  end
}
```

For example, in Java:

```
try {
    Process notifymail = Runtime.getRuntime().exec(new String[] {
        "notifymail", "-s", "Subject" });
    OutputStream stdin = new PrintStream(
        notifymail.getOutputStream(), /*autoFlush=*/false, "UTF-8");
    
    stdin.println("Hello World!");
    stdin.close();
    
    int exitCode = notifymail.waitFor();
    if (exitCode != 0) {
        throw new Exception("notifymail exited with error code " + exitCode + ".");
    }
} catch (Exception e) {
    throw new RuntimeException("Unable to send email.", e);
}
```

[FIXME: Verify both of the above code snippets]

### From cron

[FIXME: Write these instructions once I figure them out.]

## Limitations

* The configured SMTP settings are stored in plaintext, including the SMTP password.

## License

This code is provided under the MIT License.