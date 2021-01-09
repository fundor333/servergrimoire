```
.d8888b.
d88P  Y88b
Y88b.
 "Y888b.    .d88b.  888d888 888  888  .d88b.  888d888
    "Y88b. d8P  Y8b 888P"   888  888 d8P  Y8b 888P"
      "888 88888888 888     Y88  88P 88888888 888
Y88b  d88P Y8b.     888      Y8bd8P  Y8b.     888
 "Y8888P"   "Y8888  888       Y88P    "Y8888  888



 .d8888b.          d8b                        d8b
d88P  Y88b         Y8P                        Y8P
888    888
888        888d888 888 88888b.d88b.   .d88b.  888 888d888 .d88b.
888  88888 888P"   888 888 "888 "88b d88""88b 888 888P"  d8P  Y8b
888    888 888     888 888  888  888 888  888 888 888    88888888
Y88b  d88P 888     888 888  888  888 Y88..88P 888 888    Y8b.
 "Y8888P88 888     888 888  888  888  "Y88P"  888 888     "Y8888
```

[![Maintainability](https://api.codeclimate.com/v1/badges/4aece0d4c29b48cfcea4/maintainability)](https://codeclimate.com/github/fundor333/servergrimoire/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4aece0d4c29b48cfcea4/test_coverage)](https://codeclimate.com/github/fundor333/servergrimoire/test_coverage)
![PyPI - License](https://img.shields.io/pypi/l/servergrimoire)
![PyPI](https://img.shields.io/pypi/v/servergrimoire)
![PyPI - Status](https://img.shields.io/pypi/status/servergrimoire)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/servergrimoire)

This module gives you some command to check URLs, domains and other things in an automatied way.

All config and data are saved as dotfiles in your home directory and it works on Windows, Mac, and Linux systems granted
you have Python installed.

# Command

This is a partial table of commands. For the complete one we suggest you to launch the --help command

|        Command        | Option   | Explanation                              |
|:---------------------:|----------|------------------------------------------|
| servergrimoire --help |          | Print the help of the program            |
| servergrimoire run    | --u, --c | Run the command for the url described    |
| servergrimoire add    | --u      | Add the URL into the file for running    |
| servergrimoire remove | --u      | Remove the url from the file for running |
| servergrimoire stats  | --u,--c  | Print the stats of the last run made     |

For now we have the following commands

| Command     | What does it?                                   |
|-------------|-------------------------------------------------|
| ssl_check   | Check if the domain has a valid SSL certificate |
| dns_lookup  | Save the DNS lookup for the domain              |
| dns_checker | Make a whois and save the domain expiration day |

# Files

Server Grimoire has two file to work with:

* A config file .servergrimoire/config.json
* A data file .servergrimoire/data.json

They are .json file if you want to edit them.
