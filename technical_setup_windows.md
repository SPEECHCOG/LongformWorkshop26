# Technical Setup for Windows users
Many tools for long-form processing do not work for Windows systems. Therefore, we install the Windows Subsystem for Linux (WSL). Note that some of the following steps might require administrator rights. We are following the [official Windows tutorial for WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install). 

1. Open PowerShell (if possible, in admin mode by right-clicking the icon and chosing 'Run as administrator'), type the following command and press enter: 

```bash
wsl --install
```

2. You will be prompted to set a UNIX password and username. Save these for later use! Then close the shell with the following command:

```bash
exit
```

3. You should now see a WSL shell icon on your desktop, or be able to find it from your search window. Open the WSL shell, or the PowerShell if you cannot find the icon. Verify the installation with the following command:

```bash
wsl                     # in case you are in PowerShell, this command switches to WSL system
wsl --version
```

4. The above command should output information about your Linux (Ubuntu) subsystem. If everything looks fine, you can from now on use the linux commands. You can open a linux terminal by double-clicking WSL or PowerShell icon, and running:

```bash
wsl                     # in case you are in PowerShell
```
