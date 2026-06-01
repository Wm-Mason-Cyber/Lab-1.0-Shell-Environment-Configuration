# 🛑 L1.0.1 Sandbox

**Risk Level:** Zero

**Objective:** Master basic terminal navigation, apply command flags, and explore the concepts of **session scope** and variable inheritance.

**Environment:** Active Shell Session (Single Terminal Window)

#### The Whiteboard

Everything in this section of the lab is ephemeral. So, we can simplify the process down to just run on the student’s local machine. 

The only plausible conflict here is the difficulty added to the grading process for this subsection’s work. However, all of Lab 1.0 will be graded as a group, so we don’t have to worry about it too much for this L1.0.1 \- nice\!😎

## L1.0.1 Mission Overview

You are an administrator auditing a file hierarchy. You need to navigate a dense folder structure entirely through text, use utility flags to reveal hidden system metadata, and experiment with temporary environment variables to see how process scopes isolate data.

### Step 1: Terminal Navigation & File Inspection

1. Open your terminal application.  
2. Determine exactly where you are currently located in the file system tree.  
3. List all files and folders in your current directory. Notice that by default, the system hides configuration files.  
4. Apply advanced utility flags to the listing command to reveal **hidden files** (files starting with a `.`) and view detailed file information (permissions, owners, file size, and modification timestamps).

To print your working directory:

```shell
pwd
```

To list all items, including hidden files, in a long/detailed list format:

```shell
ls -la
```

*Note: The `-l` flag tells the system to use the "long" listing format, and the `-a` flag tells it to show "all" files, including hidden ones.*

### Step 2: Creating Local Session Variables

Operating systems use variables to keep track of information. Let's create a temporary variable tied strictly to your current terminal window.

1. Create a variable named `SESSION_SECURITY_TOKEN` and assign it a secret text value.  
2. Print the value of your variable to the screen to verify it was stored correctly.

To assign the variable (do not put spaces around the `=` sign\!):

```shell
SESSION_SECURITY_TOKEN="Alpha-99X-Vault"
```

To print the variable back to the terminal screen, you must use the `$` symbol to tell the shell to evaluate the variable name:

```shell
echo $SESSION_SECURITY_TOKEN
```

> [!NOTE]
> **Discussion:** This variable only exists inside your current terminal process. If you close this window, it disappears completely — no file was written, no system was changed. This is called **session-scoped state**. Security tools often use this pattern intentionally: secrets loaded into memory for a session vanish automatically when the session ends, leaving no persistent trace on disk.

### Step 3: Analyzing Process Isolation and Scope

Now we will test the boundaries of this variable. Is it available everywhere on the computer, or is it isolated?

1. Open a completely new, second terminal window side-by-side with your first window.  
2. In this *new* window, try to print the value of `$SESSION_SECURITY_TOKEN`. What happens?  
- In the second window, running `echo $SESSION_SECURITY_TOKEN` returns a blank line because variables are bound to their specific session scope by default.  
3. Go back to your *first* window. Spawn a "child process" by typing `bash` or `zsh` (depending on your system shell) to start a shell inside a shell. Try to print the variable now.  
- In your first window, when you spawn a child shell:

```shell
bash # spawns a child process
echo $SESSION_SECURITY_TOKEN
```

- *It returns blank again\! Child processes do not automatically inherit standard shell variables from parent processes.* 

> [!NOTE]
> **Discussion:** This blank result is process isolation in action. Every process on Linux has its own private environment — a separate copy of variables it received at startup. This same isolation model is the foundation of containerization: Docker containers are essentially just processes with especially strict boundaries around what they can see and inherit from the host system.

4. Exit the child shell to return to your primary window session.

### Conclusion:

To make a variable inheritable by child processes within that session, you must transform it into an **Environment Variable** using the `export` utility:

```shell
exit # Exit the child shell first
export SESSION_SECURITY_TOKEN="Alpha-99X-Vault"
bash # Spawn a child shell again
echo $SESSION_SECURITY_TOKEN # Now it inherits perfectly!
exit # Exit the child shell again
```

> [!TIP]
> **Discussion:** `export` publishes a variable into the **environment block** — a table of key-value pairs that gets copied into every child process spawned from this shell. Think of it as the difference between a sticky note on your desk (session variable, visible only to you) versus posting on a shared bulletin board (exported variable, readable by every subprocess you launch). This inheritance chain is how programs pick up configuration: your text editor, your compiler, your scripts — they all read from the environment they were launched into.

## Grading and Self Reflection

This sequence is entirely ephemeral. You could take a screenshot to record the terminal outputs, but there is no automated grading for this section. 