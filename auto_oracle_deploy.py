#!/usr/bin/env python3
"""
🚀 ORACLE CLOUD AUTOMATED DEPLOYMENT
Khud se setup krega - koi setup nahi!
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

try:
    import oci
    from oci.config import from_file, validate_config
    from oci.identity import IdentityClient
    from oci.database import DatabaseClient
    from oci.compute import ComputeClient
except ImportError:
    print("⏳ Installing OCI SDK...")
    subprocess.run([sys.executable, "-m", "pip", "install", "oci", "-q"])
    import oci

class OracleDeployer:
    def __init__(self):
        self.config = None
        self.identity_client = None
        self.database_client = None
        self.compute_client = None
        self.tenancy_id = None
        self.compartment_id = None
        
    def setup_credentials(self):
        """Setup OCI CLI credentials"""
        print("\n" + "="*60)
        print("🔐 ORACLE CLOUD AUTHENTICATION SETUP")
        print("="*60)
        
        # Check if .oci/config exists
        oci_config_path = Path.home() / ".oci" / "config"
        
        if oci_config_path.exists():
            print("✅ OCI config found!")
            try:
                self.config = from_file(config_file_location=str(oci_config_path))
                validate_config(self.config)
                print("✅ Config validated!")
                return True
            except Exception as e:
                print(f"❌ Config invalid: {e}")
                return False
        
        print("\n📝 No config found. Need authentication details.\n")
        
        # Get credentials from user
        print("Choose authentication method:")
        print("1. API Key (Recommended)")
        print("2. User/Password")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            return self.setup_api_key()
        else:
            return self.setup_user_password()
    
    def setup_api_key(self):
        """Setup using API Key"""
        print("\n" + "="*60)
        print("🔑 API KEY SETUP")
        print("="*60)
        
        tenancy_ocid = input("Enter Tenancy OCID: ").strip()
        user_ocid = input("Enter User OCID: ").strip()
        fingerprint = input("Enter Fingerprint: ").strip()
        private_key_path = input("Enter Private Key Path (default: ~/.ssh/id_rsa): ").strip()
        
        if not private_key_path:
            private_key_path = "~/.ssh/id_rsa"
        
        region = input("Enter Region (default: ap-mumbai-1): ").strip()
        if not region:
            region = "ap-mumbai-1"
        
        # Create config
        oci_dir = Path.home() / ".oci"
        oci_dir.mkdir(exist_ok=True)
        
        config_content = f"""[DEFAULT]
user={user_ocid}
fingerprint={fingerprint}
tenancy={tenancy_ocid}
region={region}
key_file={os.path.expanduser(private_key_path)}
"""
        
        config_path = oci_dir / "config"
        with open(config_path, "w") as f:
            f.write(config_content)
        
        os.chmod(config_path, 0o600)
        
        print("\n✅ OCI Config created!")
        
        try:
            self.config = from_file(config_file_location=str(config_path))
            validate_config(self.config)
            self.tenancy_id = tenancy_ocid
            print("✅ Configuration validated!")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def setup_user_password(self):
        """Setup using username/password"""
        print("\n⚠️  User/Password setup requires interactive login in console.")
        print("Please use API Key method instead.")
        return False
    
    def initialize_clients(self):
        """Initialize OCI clients"""
        print("\n🔗 Initializing OCI clients...")
        
        try:
            self.identity_client = IdentityClient(self.config)
            self.database_client = DatabaseClient(self.config)
            self.compute_client = ComputeClient(self.config)
            
            # Get tenancy info
            tenancy = self.identity_client.get_tenancy(self.tenancy_id)
            print(f"✅ Connected to tenancy: {tenancy.data.name}")
            
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_database(self, db_password):
        """Create Oracle Autonomous Database"""
        print("\n" + "="*60)
        print("🗄️  CREATING ORACLE AUTONOMOUS DATABASE")
        print("="*60)
        
        db_name = f"DUHUBDB{int(time.time())}"
        
        print(f"\nDatabase Name: {db_name}")
        print("Size: 20GB (Always Free)")
        print("Type: Autonomous Transaction Processing")
        
        try:
            # Create database
            response = self.database_client.create_autonomous_database(
                create_autonomous_database_details=oci.database.models.CreateAutonomousDatabaseDetails(
                    compartment_id=self.compartment_id,
                    db_name=db_name,
                    display_name="DUHub Database",
                    admin_password=db_password,
                    data_storage_size_in_gbs=20,
                    cpu_core_count=1,
                    is_free_tier=True,
                    db_workload="OLTP"
                )
            )
            
            db_ocid = response.data.id
            print(f"\n✅ Database created: {db_ocid}")
            
            # Wait for database
            print("⏳ Waiting for database to be available (5-10 minutes)...")
            waiter = oci.wait_until(
                self.database_client,
                self.database_client.get_autonomous_database(db_ocid),
                'lifecycle_state',
                'AVAILABLE',
                max_wait_seconds=3600
            )
            
            print("✅ Database is AVAILABLE!")
            
            # Get connection details
            db_details = self.database_client.get_autonomous_database(db_ocid).data
            
            connection_info = {
                "db_name": db_name,
                "db_ocid": db_ocid,
                "display_name": db_details.display_name,
                "connection_strings": {
                    "high": db_details.connection_strings.high if hasattr(db_details.connection_strings, 'high') else "",
                    "medium": db_details.connection_strings.medium if hasattr(db_details.connection_strings, 'medium') else "",
                    "low": db_details.connection_strings.low if hasattr(db_details.connection_strings, 'low') else "",
                }
            }
            
            return db_ocid, connection_info
            
        except Exception as e:
            print(f"❌ Database creation failed: {e}")
            return None, None
    
    def create_instance(self):
        """Create Compute Instance"""
        print("\n" + "="*60)
        print("🖥️  CREATING COMPUTE INSTANCE")
        print("="*60)
        
        instance_name = f"DUHub-Server-{int(time.time())}"
        
        print(f"\nInstance Name: {instance_name}")
        print("Shape: VM.Standard.E2.1.Micro (Always Free)")
        print("OS: Ubuntu 22.04")
        
        try:
            # Get Ubuntu 22.04 image
            print("📷 Finding Ubuntu 22.04 image...")
            images = self.compute_client.list_images(
                compartment_id=self.compartment_id,
                operating_system="Canonical Ubuntu"
            )
            
            ubuntu_image = None
            for img in images.data:
                if "22.04" in img.display_name:
                    ubuntu_image = img
                    break
            
            if not ubuntu_image:
                print("❌ Ubuntu 22.04 image not found")
                return None
            
            print(f"✅ Found image: {ubuntu_image.display_name}")
            
            # Generate/get SSH key
            ssh_key_path = Path.home() / ".ssh" / "id_rsa.pub"
            
            if not ssh_key_path.exists():
                print("📝 Generating SSH key...")
                subprocess.run([
                    "ssh-keygen", "-t", "rsa", "-N", "", 
                    "-f", str(Path.home() / ".ssh" / "id_rsa")
                ], check=True)
            
            with open(ssh_key_path) as f:
                ssh_public_key = f.read()
            
            # Create instance
            print("⏳ Creating instance...")
            
            response = self.compute_client.launch_instance(
                launch_instance_details=oci.compute.models.LaunchInstanceDetails(
                    compartment_id=self.compartment_id,
                    display_name=instance_name,
                    image_id=ubuntu_image.id,
                    shape="VM.Standard.E2.1.Micro",
                    metadata={"ssh_authorized_keys": ssh_public_key},
                    create_vnic_details=oci.compute.models.CreateVnicDetails(
                        assign_public_ip=True
                    )
                )
            )
            
            instance_id = response.data.id
            print(f"✅ Instance created: {instance_id}")
            
            # Wait for instance
            print("⏳ Waiting for instance to be RUNNING (2-5 minutes)...")
            waiter = oci.wait_until(
                self.compute_client,
                self.compute_client.get_instance(instance_id),
                'lifecycle_state',
                'RUNNING',
                max_wait_seconds=600
            )
            
            print("✅ Instance is RUNNING!")
            
            # Get public IP
            vnics = self.compute_client.list_vnic_attachments(
                compartment_id=self.compartment_id,
                instance_id=instance_id
            ).data
            
            if vnics:
                vnic_id = vnics[0].vnic_id
                # Get IP from VNIC
                public_ip = "pending..."
            
            return instance_id, public_ip
            
        except Exception as e:
            print(f"❌ Instance creation failed: {e}")
            return None, None
    
    def deploy(self):
        """Main deployment workflow"""
        print("\n" + "█"*60)
        print("█ 🚀 DU HUB UNOFFICIAL - ORACLE CLOUD DEPLOYMENT")
        print("█"*60)
        
        # Step 1: Setup credentials
        if not self.setup_credentials():
            print("❌ Authentication failed!")
            return False
        
        # Step 2: Initialize clients
        if not self.initialize_clients():
            print("❌ Client initialization failed!")
            return False
        
        # Step 3: Get compartment
        try:
            compartments = self.identity_client.list_compartments(
                compartment_id=self.tenancy_id
            ).data
            self.compartment_id = compartments[0].id if compartments else self.tenancy_id
        except:
            self.compartment_id = self.tenancy_id
        
        # Step 4: Create database
        db_password = input("\nEnter Database Admin Password (min 12 chars): ").strip()
        if len(db_password) < 12:
            print("❌ Password too short!")
            return False
        
        db_id, db_info = self.create_database(db_password)
        if not db_id:
            return False
        
        # Step 5: Create instance
        instance_id, public_ip = self.create_instance()
        if not instance_id:
            return False
        
        # Summary
        print("\n" + "="*60)
        print("✅ DEPLOYMENT COMPLETE!")
        print("="*60)
        print(f"""
Database:
  ID: {db_id}
  Admin Password: {db_password}
  Connection: See console for details

Instance:
  ID: {instance_id}
  Public IP: {public_ip}
  SSH: ssh -i ~/.ssh/id_rsa ubuntu@{public_ip}

Next Steps:
  1. SSH to instance and run deployment script
  2. Configure Django with database
  3. Start application
  4. Enable SSL
""")
        
        return True

def main():
    deployer = OracleDeployer()
    success = deployer.deploy()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
