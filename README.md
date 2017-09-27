# ftp-ninja

Performs a simple tree search to index a FTP server.
**Work in progress.**

## Changelog
- There are **no database** wrappers for the moment.
- **Logger** always picks a random color.
- Tested on a self-hosted `pyftpdlib` server and configured for its **defaults** (`0.0.0.0:2121`)

## Todo
- **The Logger**
  - has to select **a different** color for all consumers.
  - has to log erros from all consumers to a single file.
- **Tree**
  - store the index data in a tree
  - be able to pause the process (cache and restore the tree)
  - queries: ability to index the tree in real time

## Usage:
```sh
python ninja.py
```
To quit, use Ctrl-`\` as it sends a `SIGQUIT`.
