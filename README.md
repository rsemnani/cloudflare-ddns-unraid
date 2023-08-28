# Cloudflare DDNS Update for Unraid

A script to help Unraid users automatically update their dynamic IP on Cloudflare.

## Prerequisites:

1. Install Python on Unraid through the nerdpack plugin: 
   - python3-3.9.6-x86_64-1.txz 
   - python-pip-21.2.3-x86_64-1.txz 
   
2. After installation, run:
```bash
   pip3 install requests
```
## Background

Dynamic DNS (DDNS) is a method of updating, in real time, a Domain Name System (DNS) to point to a changing IP address on the Internet. This is especially useful for users who are hosting servers at home, where the IP address can change frequently due to ISP policies.

While several tools and services exist to facilitate this task, many users have found challenges with some of the popular tools, such as ddclient. These challenges may range from compatibility issues, complex configurations, or periodic failures in updating the DNS records.

This Python script, designed as an alternative to ddclient, specifically caters to Cloudflare users who want to update their A records (IPv4) with ease. By leveraging Cloudflare's robust API and the simplicity of Python's requests library, this script aims to provide:

- Simplicity: A straightforward way to update or even recreate DNS records without delving into intricate configurations.
- Flexibility: Options to force update the IP or force delete and recreate the DNS record based on user preference.
- Reliability: By directly interfacing with Cloudflare's API and fetching the public IP via the ipify service, the chances of failures are minimized.
- Compatibility: While designed with Unraid servers in mind, any system with Python can run this script, making it a versatile tool.

For users struggling with ddclient or those seeking a more direct way to update their Cloudflare DNS records, this script offers a reliable and user-friendly alternative.

## Usage:

Replace placeholders (Your Cloudflare Global API key, Your Cloudflare Login Email, Your Zone ID, and Your domain name) in ddns_update.py with your respective information.

Run the script:

```bash
python3 ddns_update.py

Optional arguments:

    --force-update: Force an update of the DNS record.
    --force-delete-create: Force a deletion and then creation of the DNS record.
```

Set a cron job to run the script every `X` hours:

```bash
0 */X * * * /path/to/python3 /path/to/ddns_update.py
```