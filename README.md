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
  pip3 install dnspython

# Usage

Test a single domain for DNS zone transfer:
```
python3 zonetransfer.py example.com
```
Batch Domains
Test multiple domains from a file:

```
python3 zonetransfer.py -l domains.txt
```

## Example Output
For a domain allowing zone transfers:
```
[*] Found NS: ns1.example.com
Zone transfer allowed for example.com

           Subdomain                   IP
           www.example.com    192.168.1.1
           mail.example.com   192.168.1.2
```
