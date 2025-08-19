# NerdyLinode

A comprehensive Python script for managing Linode infrastructure through the Linode API v4. Easily manage instances, billing, domains, and NodeBalancers from the command line.

## Features

- 📱 **Instance Management**: Create, list, boot, shutdown, reboot, and delete Linode instances
- 💰 **Billing & Invoices**: View account balance, billing information, and detailed invoice data
- 🌐 **Domain Management**: List and manage your Linode domains
- ⚖️ **NodeBalancer Support**: View and manage your NodeBalancers
- 📊 **Account Summary**: Get comprehensive overview of your Linode account
- 🔧 **Account Updates**: Update billing and account information

## Prerequisites

- Python 3.6+
- Linode API token with appropriate permissions
- `linode_api4` Python package

## Installation

1. Clone or download this repository
2. Install the required dependency:
```bash
pip install linode_api4
```

3. Configure your API credentials (see Configuration section below)

## Configuration

Create a `nerdylinode.json` file in the same directory as the script:

```json
{
  "api_token": "YOUR_LINODE_API_TOKEN_HERE",
  "default_root_password": "SecurePassword123!",
  "default_region": "us-east",
  "default_instance_type": "g6-nanode-1",
  "default_image": "linode/ubuntu22.04",
  "notification_email": "your-email@example.com",
  "settings": {
    "auto_confirm_destructive": false,
    "show_costs": true,
    "preferred_regions": ["us-east", "us-west", "eu-west"],
    "backup_enabled": true
  }
}
```

### Getting Your Linode API Token

1. Log into your Linode account
2. Go to your profile settings
3. Navigate to the "API Tokens" tab
4. Create a new Personal Access Token with the required scopes
5. Copy the token to your configuration file

**Required Scopes:**
- Linodes: Read/Write
- Domains: Read/Write (if using domain features)
- NodeBalancers: Read/Write (if using NodeBalancer features)
- Account: Read/Write

## Usage

### Basic Commands

**List all instances:**
```bash
python3 nerdylinode.py list
```

**Create a new instance:**
```bash
python3 nerdylinode.py create --label my-server --region us-east --type g6-standard-1
```

**Manage instance (boot/shutdown/reboot):**
```bash
python3 nerdylinode.py manage --id 12345678 --action reboot
```

**Delete an instance:**
```bash
python3 nerdylinode.py delete --id 12345678
```

### Billing & Account Management

**View billing information:**
```bash
python3 nerdylinode.py billing
```

**View invoice details:**
```bash
python3 nerdylinode.py invoices
```

**Account summary:**
```bash
python3 nerdylinode.py summary
```

**Update billing information:**
```bash
python3 nerdylinode.py update-billing --company "My Company" --email "new@email.com"
```

### Other Resources

**List domains:**
```bash
python3 nerdylinode.py domains
```

**List NodeBalancers:**
```bash
python3 nerdylinode.py nodebalancers
```

### Custom Configuration File

Use a different configuration file:
```bash
python3 nerdylinode.py --config /path/to/config.json list
```

## Command Reference

| Command | Description | Options |
|---------|-------------|---------|
| `list` | List all Linode instances | None |
| `create` | Create a new instance | `--label`, `--region`, `--type`, `--image` |
| `manage` | Boot/shutdown/reboot instance | `--id`, `--action` |
| `delete` | Delete an instance | `--id` |
| `billing` | Show billing information | None |
| `invoices` | Show invoice details | None |
| `summary` | Show account summary | None |
| `update-billing` | Update billing info | `--company`, `--email`, `--first-name`, `--last-name` |
| `domains` | List domains | None |
| `nodebalancers` | List NodeBalancers | None |

## Example Output

```
=== Linode Instances ===
🟢 web-server-01 (ID: 12345678)
   Type: Linode 2GB | Region: Newark, NJ
   Status: running | IPv4: 192.168.1.100
   Created: 2024-01-15T10:30:00

🔴 backup-server (ID: 87654321)
   Type: Linode 1GB | Region: Atlanta, GA
   Status: offline | IPv4: 192.168.1.101
   Created: 2024-01-10T15:45:00
```

## Security Notes

- Keep your API token secure and never commit it to version control
- Use environment variables or secure configuration management in production
- The script includes basic error handling for invalid tokens
- Consider using limited-scope API tokens for specific use cases

## Error Handling

The script provides clear error messages for common issues:
- Invalid or missing API tokens
- Network connectivity problems
- Invalid instance IDs or parameters
- Missing configuration files

## Contributing

Feel free to submit issues and enhancement requests! This script can be extended to support additional Linode API features.

## License

This project is open source. Use it however you'd like!