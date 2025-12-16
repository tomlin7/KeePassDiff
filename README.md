> ## 💡 KeePassDiff 2 - Open beta available!
>
> I’m working on **KeePassDiff 2**, a desktop version with a modern UI and a git-like diff & merge experience for KeePass (`.kdbx`) databases. Designed for long-out-of-sync databases and real-world merge scenarios that the original version couldn’t handle.
>
> 👉 [Click if you want to try it out](https://github.com/tomlin7/KeePassDiff2)
> 
> <img width="1177" height="820" alt="image" src="https://github.com/user-attachments/assets/1119ba3a-7aeb-4307-87a5-af5e6960ce62" />


# KeePassDiff

I started using KeePass back in 2021 and I have been using it since then to store my passwords. But I didn't set up a proper way to sync the database between my devices. So I ended up with multiple databases with different passwords and entries. I wanted to sort of **diff the databases and merge them** into one, like git diff -- resolving conflicts, reverting, etc. Well, KeePass doesn't provide a way to diff two databases. Hence this project.

## Usage

1. Open two KeePass databases in diff.
2. See the differences and conflicting entries between the two databases.
3. Then using merge left, merge right options decide which entries or groups to keep and which to discard.
4. Finally, export the merged database.

## Installation

```bash
pip install keepassdiff
```

Run `kpd` or `kpdiff` to run the tool.

![image](https://github.com/user-attachments/assets/22cb63db-83fa-41af-ad1d-b757144cbe5d)

## Features

- [x] Support for KeePassXC databases
- [x] Uploading and unlocking two KeePass databases
- [x] Supports both password and keyfile authentication
- [x] Visual diff of entries and groups
- [x] Support for entry groups
- [x] Hierarchical view of database contents
- [x] Merging individual entries and groups between databases
- [x] Exporting the final merged database
- [ ] Resolving conflicting entries with preferred ones
- [ ] Command-line interface for batch processing
- [ ] Copying passwords to clipboard, clearing clipboard after timeout

## Security

All database handling is done locally and no data is stored or transmitted. Temporary files are securely deleted after use, passwords are not stored.

## Development

```bash
git clone https://github.com/tomlin7/KeePassDiff.git
cd KeePassDiff
pip install -e .
kpd
```
