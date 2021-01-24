# Server Grimoire

Server grimoire is a python terminal app for checking Urls, Domains, DNS records and other things in an automated way.

For now we only have four command but we are thinking of adding more.

## Command

This is a partial table of commands. For the complete one we suggest you to launch the --help command

|        Task           | Option   | Explanation                              |
|:---------------------:|----------|------------------------------------------|
| servergrimoire        | --help   | Print the help of the program            |
| servergrimoire run    | --u, --c | Run the command for the url described    |
| servergrimoire add    | --u      | Add the URL into the file for running    |
| servergrimoire remove | --u      | Remove the url from the file for running |
| servergrimoire stats  | --u,--c  | Print the stats of the last run made     |
| servergrimoire info   | --u,--c  | Print the info of all the command        |

Unless using --c with an operation, all the command launch the taks with/on all the operation
