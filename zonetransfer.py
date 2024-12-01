#!/usr/bin/env python

import argparse
import dns.query
import dns.resolver
import dns.zone
import csv

def get_ns(zone):
    """Returns the nameservers associated with the domain provided as an 
    argument.
    
    Arguments:
        zone (string): Domain to be analysed.
    """
    try:
        name_servers = dns.resolver.resolve(zone, 'NS')
    except Exception as e:
        return None
    else:
        return name_servers

def get_zone(ip, domain):
    """ Try a zone transfer using the ip of the name server and the domain to 
        be analysed.
        Return the zone or None if the server doesn't allow zone transfer.
    
    Arguments:
        ip (dns.rdtypes.IN.A.A): IP address of the authoritative server for 
            the zone.
        domain (string): Domain to be analysed.    
    """
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(str(ip), domain))
    except Exception:
        return None
    else:
        return zone

def extract_records(zone):
    """ Returns a list of the A and CNAME records of the dns zone to be sent to 
    the corresponding output.
    
    Arguments:
        zone (dns.zone.Zone): Object Zone with the records returned by the 
            analyzed zone.
    """
    records = []
    for name, node in zone.nodes.items():
        for rdataset in node.rdatasets:
            if rdataset.rdtype in [dns.rdatatype.A, dns.rdatatype.CNAME]:
                for rdata in rdataset:
                    records.append((str(name), rdata.to_text()))
    return records

def zone_to_stdout(data):
    """ Outputs the records of the zone to stdout.
    
    Arguments:
        data (list): Records of the dns zone.
    """
    print()
    print("{: >20} {: >20}".format('Subdomain', 'IP'))
    for row in data:
        print("{: >20} {: >20}".format(*row))

def process_domain(domain):
    """ Processes the domain to perform a zone transfer and print results if successful.
    
    Arguments:
        domain (string): Domain to be processed.
    """
    name_servers = get_ns(domain)
    if name_servers is not None:
        ns_printed = False  # Flag to track if NS has been printed for the domain
        for server in name_servers:
            addr = dns.resolver.resolve(server.target, 'A')
            ip = addr.rrset[0]
            zone = get_zone(ip, domain)
            if zone is not None:
                if not ns_printed:
                    # Only print NS when zone transfer is allowed
                    print(f"[*] Found NS: {server.target}")
                    ns_printed = True
                data = extract_records(zone)
                print(f"Zone transfer allowed for {domain}")
                zone_to_stdout(data)
                break  # Stop after the first successful zone transfer

def main():
    parser = argparse.ArgumentParser(prog='zonetransfer',
                                    description="Test DNS Zone Transfer")
    parser.add_argument('domain', 
                            type=str, 
                            nargs='?', 
                            help='Domain to test the zone transfer')
    parser.add_argument('-l', '--list', 
                            type=str, 
                            help='File containing a list of domains to test')
    args = parser.parse_args()

    if args.list:
        # Read domains from file and process each one
        with open(args.list, 'r') as file:
            for line in file:
                domain = line.strip()
                process_domain(domain)  # No need to print "Testing domain"
    elif args.domain:
        # Process single domain
        process_domain(args.domain)
    else:
        print("Please provide a domain or a file with a list of domains.")

if __name__ == "__main__":
    main()
