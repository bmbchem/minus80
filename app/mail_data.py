import os

mail_data = {
    "it_email": "net-l@chem.umass.edu",
    "sender": "chem-80@umass.edu",
    "mail_password": os.environ.get("MAIL_PASSWORD", ""),
    "imap_server": "mailhub.oit.umass.edu",
    "port": 25,
    "use_ssl": False,
}
