#!/usr/bin/env python3
"""
NerdyLinode - Comprehensive Linode Management Script
Manage Linode instances, networking, billing, and more through the API
"""

import json
import sys
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional

try:
    from linode_api4 import LinodeClient, LinodeLoginError
    from linode_api4.objects import Instance, Domain, NodeBalancer
except ImportError:
    print("Error: linode_api4 not installed. Run: pip install linode_api4")
    sys.exit(1)


class NerdyLinode:
    def __init__(self, config_file: str = "nerdylinode.json"):
        """Initialize the Linode management client"""
        self.config = self._load_config(config_file)
        try:
            self.client = LinodeClient(self.config.get('api_token'))
            # Test the connection
            self.account = self.client.account()
        except LinodeLoginError:
            print("Error: Invalid API token. Please check your configuration.")
            sys.exit(1)
        except Exception as e:
            print(f"Error connecting to Linode API: {e}")
            sys.exit(1)

    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        if not os.path.exists(config_file):
            print(f"Error: Configuration file {config_file} not found.")
            print("Please create the file with your Linode API token.")
            sys.exit(1)
        
        with open(config_file, 'r') as f:
            return json.load(f)

    def list_instances(self) -> None:
        """List all Linode instances"""
        print("\n=== Linode Instances ===")
        instances = self.client.linode.instances()
        
        if not instances:
            print("No instances found.")
            return
        
        for instance in instances:
            status_color = "🟢" if instance.status == "running" else "🔴" if instance.status == "offline" else "🟡"
            print(f"{status_color} {instance.label} (ID: {instance.id})")
            print(f"   Type: {instance.type.label} | Region: {instance.region.label}")
            print(f"   Status: {instance.status} | IPv4: {', '.join(instance.ipv4)}")
            print(f"   Created: {instance.created}")
            print()

    def create_instance(self, label: str, region: str, instance_type: str, image: str) -> None:
        """Create a new Linode instance"""
        try:
            print(f"Creating instance '{label}'...")
            instance = self.client.linode.instance_create(
                ltype=instance_type,
                region=region,
                image=image,
                label=label,
                root_pass=self.config.get('default_root_password', 'TempPassword123!')
            )
            print(f"✅ Instance created successfully!")
            print(f"   ID: {instance.id}")
            print(f"   Label: {instance.label}")
            print(f"   IPv4: {', '.join(instance.ipv4)}")
        except Exception as e:
            print(f"❌ Error creating instance: {e}")

    def manage_instance(self, instance_id: int, action: str) -> None:
        """Manage instance (boot, shutdown, reboot)"""
        try:
            instance = self.client.load(Instance, instance_id)
            
            if action == "boot":
                instance.boot()
                print(f"✅ Instance {instance.label} is booting...")
            elif action == "shutdown":
                instance.shutdown()
                print(f"✅ Instance {instance.label} is shutting down...")
            elif action == "reboot":
                instance.reboot()
                print(f"✅ Instance {instance.label} is rebooting...")
            else:
                print(f"❌ Unknown action: {action}")
        except Exception as e:
            print(f"❌ Error managing instance: {e}")

    def delete_instance(self, instance_id: int) -> None:
        """Delete a Linode instance"""
        try:
            instance = self.client.load(Instance, instance_id)
            label = instance.label
            instance.delete()
            print(f"✅ Instance '{label}' (ID: {instance_id}) deleted successfully!")
        except Exception as e:
            print(f"❌ Error deleting instance: {e}")

    def show_billing_info(self) -> None:
        """Display account billing information"""
        print("\n=== Billing Information ===")
        try:
            account = self.account
            print(f"Account Balance: ${account.balance:.2f}")
            print(f"Account Email: {account.email}")
            print(f"Company: {account.company or 'N/A'}")
            print(f"Active Since: {account.active_since}")
            
            # Get current month's invoice
            invoices = self.client.account.invoices()
            if invoices:
                latest_invoice = invoices[0]
                print(f"\nLatest Invoice:")
                print(f"   Date: {latest_invoice.date}")
                print(f"   Total: ${latest_invoice.total:.2f}")
                print(f"   Label: {latest_invoice.label}")
        except Exception as e:
            print(f"❌ Error retrieving billing info: {e}")

    def show_invoice_details(self, invoice_id: Optional[int] = None) -> None:
        """Show detailed invoice information"""
        print("\n=== Invoice Details ===")
        try:
            invoices = self.client.account.invoices()
            
            if not invoices:
                print("No invoices found.")
                return
            
            target_invoice = invoices[0] if invoice_id is None else next((inv for inv in invoices if inv.id == invoice_id), None)
            
            if not target_invoice:
                print(f"Invoice {invoice_id} not found.")
                return
            
            print(f"Invoice ID: {target_invoice.id}")
            print(f"Date: {target_invoice.date}")
            print(f"Total: ${target_invoice.total:.2f}")
            print(f"Label: {target_invoice.label}")
            
            # Get invoice items
            items = target_invoice.items
            if items:
                print("\nInvoice Items:")
                for item in items:
                    print(f"   - {item.label}: ${item.amount:.2f}")
        except Exception as e:
            print(f"❌ Error retrieving invoice details: {e}")

    def list_domains(self) -> None:
        """List all domains"""
        print("\n=== Domains ===")
        try:
            domains = self.client.load(Domain).instances()
            
            if not domains:
                print("No domains found.")
                return
            
            for domain in domains:
                print(f"🌐 {domain.domain}")
                print(f"   ID: {domain.id}")
                print(f"   Type: {domain.type}")
                print(f"   Status: {domain.status}")
                print()
        except Exception as e:
            print(f"❌ Error listing domains: {e}")

    def list_nodebalancers(self) -> None:
        """List all NodeBalancers"""
        print("\n=== NodeBalancers ===")
        try:
            nodebalancers = self.client.load(NodeBalancer).instances()
            
            if not nodebalancers:
                print("No NodeBalancers found.")
                return
            
            for nb in nodebalancers:
                print(f"⚖️  {nb.label}")
                print(f"   ID: {nb.id}")
                print(f"   Region: {nb.region.label}")
                print(f"   IPv4: {nb.ipv4}")
                print(f"   IPv6: {nb.ipv6}")
                print()
        except Exception as e:
            print(f"❌ Error listing NodeBalancers: {e}")

    def show_account_summary(self) -> None:
        """Show comprehensive account summary"""
        print("\n=== Account Summary ===")
        try:
            account = self.account
            instances = self.client.linode.instances()
            
            print(f"Account: {account.email}")
            print(f"Balance: ${account.balance:.2f}")
            print(f"Active Instances: {len(instances)}")
            
            # Calculate monthly estimate
            monthly_cost = sum(float(instance.type.price.monthly) for instance in instances)
            print(f"Estimated Monthly Cost: ${monthly_cost:.2f}")
            
            # Show instances by status
            running = [i for i in instances if i.status == "running"]
            stopped = [i for i in instances if i.status == "offline"]
            
            print(f"Running: {len(running)} | Stopped: {len(stopped)}")
            
        except Exception as e:
            print(f"❌ Error retrieving account summary: {e}")

    def update_billing_info(self, **kwargs) -> None:
        """Update billing information"""
        print("\n=== Updating Billing Information ===")
        try:
            account = self.account
            
            # Update fields that were provided
            update_fields = {}
            if 'company' in kwargs:
                update_fields['company'] = kwargs['company']
            if 'email' in kwargs:
                update_fields['email'] = kwargs['email']
            if 'first_name' in kwargs:
                update_fields['first_name'] = kwargs['first_name']
            if 'last_name' in kwargs:
                update_fields['last_name'] = kwargs['last_name']
            
            if update_fields:
                account.save(**update_fields)
                print("✅ Billing information updated successfully!")
            else:
                print("No fields provided to update.")
                
        except Exception as e:
            print(f"❌ Error updating billing info: {e}")


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(description="NerdyLinode - Linode Management Script")
    parser.add_argument("--config", default="nerdylinode.json", help="Configuration file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List instances
    subparsers.add_parser("list", help="List all Linode instances")
    
    # Create instance
    create_parser = subparsers.add_parser("create", help="Create a new Linode instance")
    create_parser.add_argument("--label", required=True, help="Instance label")
    create_parser.add_argument("--region", default="us-east", help="Region (default: us-east)")
    create_parser.add_argument("--type", default="g6-nanode-1", help="Instance type (default: g6-nanode-1)")
    create_parser.add_argument("--image", default="linode/ubuntu22.04", help="Image (default: linode/ubuntu22.04)")
    
    # Manage instance
    manage_parser = subparsers.add_parser("manage", help="Manage instance (boot/shutdown/reboot)")
    manage_parser.add_argument("--id", type=int, required=True, help="Instance ID")
    manage_parser.add_argument("--action", choices=["boot", "shutdown", "reboot"], required=True, help="Action to perform")
    
    # Delete instance
    delete_parser = subparsers.add_parser("delete", help="Delete a Linode instance")
    delete_parser.add_argument("--id", type=int, required=True, help="Instance ID to delete")
    
    # Billing commands
    subparsers.add_parser("billing", help="Show billing information")
    subparsers.add_parser("invoices", help="Show invoice details")
    subparsers.add_parser("summary", help="Show account summary")
    
    # Update billing
    update_parser = subparsers.add_parser("update-billing", help="Update billing information")
    update_parser.add_argument("--company", help="Company name")
    update_parser.add_argument("--email", help="Email address")
    update_parser.add_argument("--first-name", help="First name")
    update_parser.add_argument("--last-name", help="Last name")
    
    # Other resources
    subparsers.add_parser("domains", help="List domains")
    subparsers.add_parser("nodebalancers", help="List NodeBalancers")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize NerdyLinode
    nerdy = NerdyLinode(args.config)
    
    # Execute commands
    if args.command == "list":
        nerdy.list_instances()
    elif args.command == "create":
        nerdy.create_instance(args.label, args.region, args.type, args.image)
    elif args.command == "manage":
        nerdy.manage_instance(args.id, args.action)
    elif args.command == "delete":
        nerdy.delete_instance(args.id)
    elif args.command == "billing":
        nerdy.show_billing_info()
    elif args.command == "invoices":
        nerdy.show_invoice_details()
    elif args.command == "summary":
        nerdy.show_account_summary()
    elif args.command == "update-billing":
        kwargs = {k.replace('-', '_'): v for k, v in vars(args).items() 
                 if v is not None and k not in ['command', 'config']}
        nerdy.update_billing_info(**kwargs)
    elif args.command == "domains":
        nerdy.list_domains()
    elif args.command == "nodebalancers":
        nerdy.list_nodebalancers()


if __name__ == "__main__":
    main()
