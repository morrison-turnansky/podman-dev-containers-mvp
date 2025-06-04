# Podman Dev Containers MVP

This is a minimal viable product demonstrating how to use **dev containers** with **Podman** instead of Docker.

---

## Prerequisites

1. **Git Configuration**  
   Ensure you have a global Git configuration. If not, run the following commands:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your-email@example.com"
   ```


2. **Install Podman**
   If you are using Fedorda at Red Hat, it should be preinstalled. 

3. **Install vscode**

4. **Install  vscode extensions**
    Install the following extensions: dev containers.

## Using the project: 

1. **Clone the project** 
   ```bash
      git clone git@github.com:morrison-turnansky/podman-dev-containers-mvp.git
   ``` 
2. **Enter the project in vscode** 
      ```bash
      code ./podman-dev-containers-mvp
   ``` 

In the bottome left hand corner of the vs code window there is a blue button, press on it and select reopen in container from the drop down menu. 

You now have containerized environment. Git credentials will be copied from your host, so develop as your normally would. 