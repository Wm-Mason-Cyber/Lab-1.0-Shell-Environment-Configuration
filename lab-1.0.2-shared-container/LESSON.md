# 🌐 L1.0.2 Shared Classroom Container

**Risk Level:** Medium (Configuration Interference Risk)

**Objective:** Understand how applications use system-level environment variables to route data and discover how configuration collisions happen when variables are misconfigured.

**Environment:** Shared Network Simulation Space / Multi-User Environment Variables

#### Step 2 Architecture: Shared API Container

Instead of running 30 separate containers per class, you deploy **one container that can be easily reset between periods**.   
Students use simple scripts (that capture their username, first and last name, timestamp, and class period) to upload data to the class-container.   
The teacher will be able to see the student uploads to the container to evaluate who participated here.   
The API service actually also hosts a simple page that shows ‘live’ (perhaps on a short auto-refresh) who has sent in their data. 

## L1.1.2 Mission Overview

You are deploying a local utility that needs to communicate with an API service. Instead of hardcoding the network server's IP address directly into your software code (which is a massive security risk), you will configure the system environment to feed the server configuration dynamically to your tools.

> [!NOTE]
> **Discussion:** Hardcoding an IP address or URL directly in a script creates several problems: the script breaks the moment the server moves, every student needs a different copy of the file, and — most critically — if the script is ever shared publicly or committed to a repository, the internal network topology is exposed. Environment variables solve all three: the configuration lives outside the code, is set per-machine at runtime, and never touches the source file.

`<Instructor_Provided_IP_Address>` ← **10.24.81.95** (as of June 1, 2026\)

### Step 1: Mapping Out the Execution Target

1. Your instructor has launched a local web application service within the lab network environment.  
2. In your terminal, verify that your machine can structurally see and communicate with the host application framework over the local network path using a basic testing probe.

To check if a host is reachable over the network interface:

```shell
ping -c 4 <Instructor_Provided_IP_Address>
```

### Step 2: Utilizing App Environment Triggers

1. The following script uses `curl` to read an environment variable called `TARGET_GATEWAY` to know where to transmit data logs. Copy the contents of the code clock below into a file called `lab-1.0-api-send` on your local computer. 

```shell
#!/bin/bash
if [ -z "$TARGET_GATEWAY" ]; then
    echo "Error: TARGET_GATEWAY environment variable is not set."
    echo "Fix:  export TARGET_GATEWAY=\"http://<Instructor_IP>:8080\""
    exit 1
fi

USERNAME=$(whoami)
TIMESTAMP=$(date -Iseconds)
read -p "Enter your first name: " FIRST_NAME
read -p "Enter your last name: " LAST_NAME
read -p "Enter your class period number: " CLASS_PERIOD

echo "Sending to $TARGET_GATEWAY ..."
RESPONSE=$(curl -s -X POST "$TARGET_GATEWAY/lab-1-0-2" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$USERNAME\", \"first_name\": \"$FIRST_NAME\", \"last_name\": \"$LAST_NAME\", \"timestamp\": \"$TIMESTAMP\", \"period\": \"$CLASS_PERIOD\"}")

echo "$RESPONSE"
```

   \*\* If the environment variable named `TARGET_GATEWAY` is not configured, this script will complain to you, and stop. 

2. Make the above script executable with the following command: `chmod +x lab-1.0-api-send`  
3. Create and export an environment variable named `TARGET_GATEWAY` configured with the application server IP parameter.

```shell
export TARGET_GATEWAY="http://<Instructor_Provided_IP_Address>:8080"
```

4. Print all currently active environment variables in your system to prove your new key is registered globally in the environment block.  
   To print out every active environment variable currently loaded into your active process space:

```shell
printenv
```

   *Look through the output list to find your `TARGET_GATEWAY` entry. Or run:* `printenv | grep “TARGET_GATEWAY”`

> [!NOTE]
> **Discussion:** `printenv` reveals *every* environment variable currently loaded — your home directory path, your username, your language settings, your shell, and any secrets your shell has exported. On a multi-user system, any process running as your user can read all of these values. This is why production systems use dedicated secret management tools (like HashiCorp Vault or environment injection from a secrets manager) instead of plain exported variables for sensitive credentials like API keys or passwords.

### Step 3: Experiencing Configuration Interception

1. What happens if another administrator modifies your configuration flags, or if you accidentally point your variable to the wrong place?  
2. Change your `TARGET_GATEWAY` environment variable to a fake or broken address (e.g., `http://127.0.0.1:9999`).  
3. Attempt to run your local diagnostic checks or execute a network interaction tool that relies on that variable. Observe the connection failure. This demonstrates why configuration security and environment variable integrity are critical parameters of system protection.

> [!NOTE]
> **Discussion:** What you just simulated is a **configuration interception scenario**. In real infrastructure this same failure appears when: a misconfigured deployment points a service at the wrong backend, a developer runs a script with a stale variable still set from a previous session, or a malicious actor modifies an environment variable before your script runs. The script itself was never broken — only its configuration was. This separation between code and configuration is why environment variable integrity is treated as a security concern, not just a convenience issue.

## Grading and Reflection

By getting your username, timestamp, and class-period into the API, you have completed the graded requirement of this section.   
You should be able to see that your data is present on the page the teacher is showing in class (tell them to turn it on, if they haven’t yet 😅)