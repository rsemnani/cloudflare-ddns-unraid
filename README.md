# Cloudflare DDNS Update for Unraid

A script to help Unraid users automatically update their dynamic IP on Cloudflare.

## Prerequisites:

1. Install Python on Unraid through the nerdpack plugin: 
   - python3-3.9.6-x86_64-1.txz 
   - python-pip-21.2.3-x86_64-1.txz 
   
2. After installation, run:
   ```bash
   pip3 install requests

Usage:

    Replace placeholders (Your Cloudflare Global API key, Your Cloudflare Login Email, Your Zone ID, and Your domain name) in ddns_update.py with your respective information.

    Run the script:

    bash

python3 ddns_update.py

Optional arguments:

    --force-update: Force an update of the DNS record.
    --force-delete-create: Force a deletion and then creation of the DNS record.

Set a cron job to run the script every 6 hours:

bash

0 */6 * * * /path/to/python3 /path/to/ddns_update.py