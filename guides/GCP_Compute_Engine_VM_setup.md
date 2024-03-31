# Setting up GCP Compute Engine VM Instance

1. Generate a new SSH key by running `ssh-keygen -t rsa -f 'C:\Users\<username>\.ssh\<key-name>' -C <username-on-vm> -b 2048`
2. Run cat command on the .pub output then copy its contents in Compute Engine > Settings > Metadata > SSH KEYS then ADD SSH KEY > Save.

## Creating a VM Instance in Compute Engine
3. Navigate to Compute Engine > VM instances then select CREATE INSTANCE.
4. Select a name, region, and zone that works best for you. Note the region, as we will deploy all resources into that region.
5. For this project, the Machine type used is e2-standard-4 with 4vCPU (2 core), 16 GB memory specifications. 
6. The Boot disk used for this project is 30 GB in an Ubuntu operating system with Ubuntu 20.04 LTS version.
![](guides/images/VM_2.png)
7. Select "CREATE" then navigate to the VM Instance and select "Start / Resume" from the three-dot menu to the right. Make a note of the external IP address provided to setup the ssh config file.

## Accessing the VM Instance
8. Add the Remote Explorer Extension from the Extensions page of VSCode.
9. Create or update (if already existing) the config file in your .ssh/ directory to include the new VM Instance.
```bash
Host <any-host-name>
    HostName <VM-Instance-External-IP>
    User <username>
    IdentityFile <path-to-ssh-key-name>
```
10. Connect to the VM instance through VSCode by selecting the host name in the ssh config file
11. Or by running the  command `ssh <host-name>` from your terminal.

## Setting up Project Dependencies
12. Clone the project repo  `<git clone https://github.com/demapumpum/flight-analytics.git>`
13. Navigate and run the script in `scripts/vm_dependencies.sh`
14. Test by running docker-compose —version. If it does not run successfully, try running `source .bashrc`

## Setting up GCP Credentials in the VM Instance
15. Create a directory folder `.google/credentials/` in your VM machine’s home directory with the json file generated in setting up your GCP project.