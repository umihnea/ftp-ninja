# ftp-ninja

Performs a simple Breath First Search to index a FTP server.
**Work in progress.**

- There are **no database** wrappers for simplicity.
- **The Logger** always picks a random color.
- Tested on a self-hosted `pyftpdlib` server and configured for its **defaults**.

Usage:
```sh
python crawler.py
```
Follow the on-screen prompts (created using the `click` module).