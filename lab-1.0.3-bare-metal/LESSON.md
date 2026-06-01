# ⚡ L1.0.3 Bare Metal, High Risk

**Risk Level:** High (Persistent Operational Configuration Footprints)

**Objective:** Permanently customize your native user workspace environment profile, construct a localized binary script repository, and manipulate the system execution **`PATH`** variable.  
   
**Environment:** Native Local Linux System Partition (`Debian / Fedora`)

#### The Architecture: Local Bare-Metal Testing

The syllabus explicitly states that in Module 0, students configure a **bare-metal dual-boot Linux ecosystem** where they have `sudo` access.

##### Recommended Workflow

1\. **Local Configuration (Student):** Students run through the instructions, and should be able to see if their script is working or not.

2\. **Central Collection (Teacher):** We can reuse the previous section's API for this one. Students will submit their results through a `curl` request to the path: `/lab-1-0-3` for this section. That keeps all the results centralized for teacher evaluation, and able to be visualized for immediate student feedback.

## L1.1.3 Mission Overview

Up until now, your environment adjustments have been ephemeral—closing the terminal window wiped them out. In this lab, you step onto the bare metal. You will modify your user account's permanent configuration file (`.bashrc` or `.zshrc`) to create persistent variables. You will then create a custom scripts directory, add it to the system execution `PATH`, and observe how the operating system searches for executable software binaries.

---

### ⚠️ HIGH RISK WARNING

In this lab, you will edit the `PATH` environment variable. The `PATH` variable tells your computer exactly where to look for system commands like `ls`, `cd`, `nano`, and `clear`. If you make a typo or accidentally overwrite this variable completely, your terminal will lose the ability to find **any** commands, and it will appear broken. Read instructions carefully and execute commands precisely.

---

### Step 1: Locate Your User Configuration Blueprint

When a terminal opens, it reads a startup script located right in your user's home directory. Let's find it.

1. Ensure you are inside your home user root directory.  
2. Locate your specific shell's configuration dotfile (typically `.bashrc` for Bash shells, or `.zshrc` for Zsh shells).

```shell
cd ~
ls -la
```

*Look closely at the output text. You should see a file named `.bashrc` or `.zshrc`.*

### Step 2: Create a Custom System Binary Directory

Linux reserves `~/.local/bin` as the standard location for user-installed scripts and utilities — it is part of the **XDG Base Directory Specification**, which is the agreed-upon standard for where user-specific programs live on modern Linux systems. Placing scripts here follows real-world professional conventions.

> [!NOTE]
> **Discussion:** The XDG Base Directory Specification (freedesktop.org) defines a consistent map of where Linux programs should store different types of user data: `~/.local/bin` for executables, `~/.config` for configuration files, `~/.local/share` for application data, `~/.cache` for temporary cached files. When developers and distros agree on these locations, your scripts don't collide with system packages, and system packages don't stomp on your personal configurations.

1. Create the standard user binary directory and move inside it.
2. Use a command-line text editor to create a script named `mason-cyber-syscheck`.
3. Type the following script contents exactly:

```shell
#!/bin/bash
echo "=== MASON CYBER SYSTEM CHECK ==="
echo "User:     $(whoami)@$(hostname)"
echo "Date:     $(date)"
echo ""
echo "--- Network Interfaces ---"
ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print "  " $NF ": " $2}'
echo "Default Gateway: $(ip route | grep default | awk '{print $3}')"
echo ""
echo "--- Disk Usage ---"
df -h / | tail -1 | awk '{print "  Root: " $3 " used of " $2 " (" $5 " full)"}'
echo ""
echo "--- Local User Accounts ---"
awk -F: '$3 >= 1000 && $3 < 65534 {print "  " $1 " (uid=" $3 ")"}' /etc/passwd
echo ""
echo "--- Currently Logged In ---"
who | awk '{print "  " $1 " on " $2}'
echo "================================="
```

4. Save and exit the text editor.

```shell
mkdir -p ~/.local/bin
nano ~/.local/bin/mason-cyber-syscheck
```

*Type your script lines into the nano editor interface. To save and exit nano: press `Ctrl+O`, press `Enter` to confirm the filename, then press `Ctrl+X` to exit.*

*Note: The "Local User Accounts" section uses `awk` to scan `/etc/passwd` for accounts with a UID between 1000 and 65533. On Linux, UIDs below 1000 are reserved for system processes. UIDs at or above 1000 belong to real human users — on a shared classroom machine, those are your classmates.*

> [!NOTE]
> **Discussion:** Every account on a Linux system has a **UID** (User ID) — a number the kernel uses internally to enforce all file permissions and process ownership. UIDs 0–999 are reserved for the OS itself (`root` is always UID 0). UIDs 1000 and above are created by administrators for real people. When you see unfamiliar UIDs in this range, those accounts belong to your classmates — and they can see this same list when they run `mason-cyber-syscheck`. This is the same mechanism that makes `chmod`, `chown`, and `sudo` work: the kernel checks UIDs, not usernames.

### Step 3: Understanding Privilege & Trapped Execution Paths

1. Try to run your script by typing `mason-cyber-syscheck` from your home directory. What happens? The terminal returns `command not found`. Why? Even though the file exists on disk, the operating system *only* looks for executables in directories explicitly listed inside the `$PATH` environment variable.  
2. Run the script explicitly by providing its full path:

```shell
~/.local/bin/mason-cyber-syscheck
```

3. If the terminal returns a `Permission Denied` warning, the file does not yet have its executable bit set. Modify the permissions:

```shell
chmod +x ~/.local/bin/mason-cyber-syscheck
~/.local/bin/mason-cyber-syscheck
```

*The `chmod +x` command adds executable privileges to the file, transforming it from a raw text document into a runnable system script.*

### Step 4: Hardening and Modifying the Execution PATH

Now we want to make our script run from **anywhere** on the system, just like native commands (`ls`, `clear`), without needing to type the full path.

1. First, check what directories are currently in your `PATH`:

```shell
echo $PATH
```

*On modern Debian and Fedora systems, `~/.local/bin` is often included automatically once the directory exists. If you see it in the output — great, that's the system following the XDG standard by default. If you do NOT see it listed, continue to add it manually in the next step.*

> [!TIP]
> **Discussion:** If `~/.local/bin` was already in your `PATH` without you doing anything, that's your Linux distribution being intentionally helpful. On Debian, the default `~/.profile` startup script checks whether `~/.local/bin` exists and adds it automatically at login. This is a good example of how the entire ecosystem — the OS, package managers, and individual developers — coordinate around shared conventions. When everyone agrees on a location, the system can make smart defaults.

2. Open your persistent startup configuration file in your terminal editor:

```shell
nano ~/.bashrc  # or ~/.zshrc if utilizing a Zsh environment
```

3. Scroll to the very bottom of the file. Carefully append these two lines:

```shell
export PATH="$PATH:$HOME/.local/bin"
export CLASS_PERIOD="your-class-period-number"
```

*Replace `your-class-period-number` with your actual period (e.g., `1`, `3`). This variable is used later for the submission step. ...and maybe future labs.*

4. Save and close the configuration file. Then force your active shell to reload the updated profile:

```shell
source ~/.bashrc  # or source ~/.zshrc
```

5. Verify that the change took effect. Change to an unrelated directory and run your script globally:

```shell
cd /tmp
mason-cyber-syscheck
```

*If configured correctly, the operating system searches through your `$PATH` directories in order, hits `~/.local/bin`, finds the script, and runs it — from anywhere on the system.*

## Grading and Reflection

Submit your `mason-cyber-syscheck` output to the classroom API. Verify that `$TARGET_GATEWAY` and `$CLASS_PERIOD` are active in your current shell (they should be if you completed the previous lab steps and sourced your `.bashrc`).

Run these three commands exactly:

```shell
SYSCHECK_OUTPUT=$(mason-cyber-syscheck | base64 -w0)
curl -s -X POST "$TARGET_GATEWAY/lab-1-0-3" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$(whoami)\", \"period\": \"$CLASS_PERIOD\", \"output\": \"$SYSCHECK_OUTPUT\"}"
echo ""
echo "Done! Check the class display for your Lab 1.0.3 checkmark."
```

*`base64 -w0` encodes your syscheck output into a safe text format before embedding it in the JSON payload — multi-line terminal output would otherwise break the JSON structure.*

> [!NOTE]
> **Discussion:** Base64 converts arbitrary data into a safe alphabet of 64 characters (A–Z, a–z, 0–9, `+`, `/`). It does **not** encrypt anything — anyone who receives base64 data can decode it instantly with `base64 -d`. Its purpose here is purely structural: JSON strings cannot contain raw newlines, so encoding the multi-line output first makes it a single safe string the JSON parser can handle. **Encoding is not security.** Encryption is security. Confusing the two is a common mistake.

You should see a checkmark (✓) appear next to your name on the class display. Tell your instructor to refresh the page if it hasn't updated yet! 😅

## 🚨 Emergency Troubleshooting Area

If you made a typo in Step 4 and broke your PATH, your terminal might say `ls: command not found` or `nano: command not found`. Do not panic\! Your files are not gone; your terminal has just lost its map.

You can temporarily restore your environment map for the current window by running a hardcoded recovery command:

```shell
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

Once your temporary map is restored, standard commands like `nano` will work again. Re-open your configuration profile (`nano ~/.bashrc`), locate the line you added at the bottom, carefully check for spelling errors or missing symbols (ensure you did not forget the `:` or `$` characters), fix the text, save, and reload using `source ~/.bashrc`.
