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

This module give you some command for check urls, domains and other things in automatic way.

All config and data are save as dotfiles on your home directory and it works on Windows, Mac e Linux system if you have Python installed.

# Command

This is a partial table of command. For the complete one we suggest to launch the --help command

|        Command        | Option   | Explanation                              |
|:---------------------:|----------|------------------------------------------|
| servergrimoire --help |          | Print the help of the program            |
| servergrimoire run    | --u, --c | Run the command for the url described    |
| servergrimoire add    | --u      | Add the url into the file for running    |
| servergrimoire remove | --u      | Remove the url from the file for running |
| servergrimoire stats  | --u,--c  | Print the stats of the last run made     |

For now we have the following commands

| Command     | What does it?                                   |
|-------------|-------------------------------------------------|
| ssl_check   | Check if the domain has a valid certificate SSl |
| dns_lookup  | Save the DNS lookup for the domain              |
| dns_checker | Make a whois and save the domain expiration day |

# Files

Server Grimoire has two file to work with:

* A config file .servergrimoire_config
* A data file .servergrimoire_data

They are .json file if you want to edit them.
