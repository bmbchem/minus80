# minus80

## Project overview
This project monitors Minus 80 freezer status on a Raspberry Pi and sends email alerts when an alarm or recovery event occurs.

The program watches a GPIO pin for state changes, looks up the freezer mapping from a CSV file, and sends notification emails to the appropriate contact. If the freezer lookup fails, the IT group is notified instead.

The current implementation uses the RPi.GPIO package for GPIO monitoring and Python's standard library for CSV and SMTP handling.

## Installation
1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. If you are running this on a Raspberry Pi, make sure the GPIO libraries are available for your system.

## Configuration
### Mail settings
The mail configuration lives in app/mail_data.py.

For UMass MailHub, the current defaults use mailhub.oit.umass.edu on port 25 with no authentication. If your SMTP server requires authentication, set the MAIL_PASSWORD environment variable before running the program.

This version uses the sender email configured in app/mail_data.py and is set up for MailHub access by the project maintainer, Xia Huang.

### CSV file
The main freezer mapping file is app/freezer_info.csv by default, but for deployment to multiple Pis it is better to keep the freezer mapping as local per-device data.

You can override the CSV path by setting the FREEZER_CSV environment variable, for example:

```bash
export FREEZER_CSV=/path/to/local/freezer_info.csv
```

This makes it easy to keep the repo public while copying a private or site-specific CSV file manually onto each Pi.

The file tests/freezer_test.csv is a sample fixture used by the unit tests.

## Running
Run the main program with:

```bash
python3 minus80_main.py
```

The program runs continuously until interrupted.

## Tests
Run the test suite with:

```bash
python3 -m unittest discover -s tests
```

To test email sending manually, run:

```bash
python3 app/Email.py your.email@example.com
```

## Repository layout
- app/ contains the main application modules and the default freezer CSV.
- tests/ contains the unit tests and sample CSV data.
- requirements.txt lists the Python dependencies.

## Contact
Developer: Nikki Tebaldi

Email: ntebaldi@umass.edu

## Changelog
- Version 2.0: Refactor of the Minus 80 monitor into an object-oriented Python program.
