#!/bin/python3
import requests
import argparse
import logging

# Configure the logging module
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

def get_args():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Manage Cloudflare DNS records.")
    parser.add_argument("--force-update", action="store_true", 
                        help="Force an update of the DNS record.")
    parser.add_argument("--force-delete-create", action="store_true",
                        help="Force a deletion and then creation of the DNS record.")
    return parser.parse_args()

def fetch_existing_record(zone_id, record_name, headers):
    """
    Fetch the existing DNS record from Cloudflare.

    Args:
        zone_id (str): Cloudflare Zone ID.
        record_name (str): Name of the DNS record.
        headers (dict): Required headers for Cloudflare API authentication.

    Returns:
        dict: The existing DNS record details or None if not found.
    """
    endpoint = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={record_name}"
    response = requests.get(endpoint, headers=headers)
    records = response.json().get('result')
    
    if records:
        return records[0]
    return None

def create_dns_record(zone_id, record_type, record_name, record_content, headers):
    """
    Create a new DNS record on Cloudflare.
    """
    data = {
        "type": record_type,
        "name": record_name,
        "content": record_content,
        "ttl": 3600,  # TTL set to 5 hours.
        "proxied": False
    }
    
    response = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", 
                             headers=headers, json=data)
    return response.json()

def get_ipv4_address():
    """
    Fetch the public IPv4 address of the machine running the script using the ipify service.

    Returns:
        str: The public IPv4 address.
    
    Raises:
        ValueError: If there's an issue fetching the IP address or parsing the response.
    """
    try:
        response = requests.get("http://api.ipify.org/?format=json", headers={"Accept": "application/json"})
        
        # Ensure the response status code is 200 (OK)
        response.raise_for_status()

        # Parse the JSON response and return the IP address
        return response.json()['ip']

    except (requests.RequestException, KeyError) as e:
        raise ValueError(f"Error fetching the public IPv4 address: {e}")

def update_dns_record(zone_id, record_id, record_type, record_name, record_content, headers):
    """
    Update an existing DNS record on Cloudflare.
    """
    data = {
        "type": record_type,
        "name": record_name,
        "content": record_content,
        "ttl": 120,
        "proxied": False
    }

    response = requests.put(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
                            headers=headers, json=data)
    return response.json()

def delete_dns_record(zone_id, record_id, headers):
    """
    Delete an existing DNS record on Cloudflare.
    """
    response = requests.delete(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
                               headers=headers)
    return response.json()

def main():
    # Authentication and configuration details

    API_KEY = 'Your Cloudflare Global API key'
    EMAIL = 'Your Cloudflare Login Email'
    ZONE_ID = 'Your Zone ID'
    headers = {
        "X-Auth-Email": EMAIL,
        "X-Auth-Key": API_KEY,
        "Content-Type": "application/json"
    }

    args = get_args()
    record_type = "A"  # Insert the type of DNS record (e.g., "A" for IPv4 address, "AAAA" for IPv6, "CNAME" for canonical name, etc.)
    record_name = "Your domain name"
    record_content = get_ipv4_address()
    existing_record = fetch_existing_record(ZONE_ID, record_name, headers)

    if args.force_update:
        if existing_record:
            logging.info(f"Updating DNS record with new IP {record_content}.")
            update_dns_record(ZONE_ID, existing_record['id'], record_type, record_name, record_content, headers)
        else:
            logging.info(f"Creating new DNS record with IP {record_content}.")
            create_dns_record(ZONE_ID, record_type, record_name, record_content, headers)

    elif args.force_delete_create:
        if existing_record:
            logging.info(f"Deleting existing DNS record and creating a new one with IP {record_content}.")
            delete_dns_record(ZONE_ID, existing_record['id'], headers)
        create_dns_record(ZONE_ID, record_type, record_name, record_content, headers)

    else:
        if existing_record:
            if existing_record['content'] != record_content:
                logging.info(f"IP has changed. Updating DNS record from {existing_record['content']} to {record_content}.")
                update_dns_record(ZONE_ID, existing_record['id'], record_type, record_name, record_content, headers)
            else:
                logging.info("IP address has not changed. No update necessary.")
        else:
            logging.info(f"No existing DNS record found. Creating new record with IP {record_content}.")
            create_dns_record(ZONE_ID, record_type, record_name, record_content, headers)

if __name__ == "__main__":
    main()
