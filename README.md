# Zone-Transfer
This tool is a Python script designed to test DNS Zone Transfers. It checks if an authoritative name server allows zone transfers and extracts `A` and `CNAME` records if successful.

## Features

- Query nameservers for a domain.
- Attempt DNS zone transfers to retrieve zone data.
- Extract and display `A` and `CNAME` records from the DNS zone.
- Supports processing a single domain or batch testing multiple domains from a file.
- User-friendly output to standard output (stdout).

## Prerequisites

- **Python 3.6+**
- **dnspython library**:
  Install it using pip:
  ```bash
  pip install dnspython
