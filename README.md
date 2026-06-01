# Lab 1.0 — Shell Environment Configuration

**Unit:** U1 — Introduction to Security  
**Course:** AP Cybersecurity  
**Risk Level:** Escalating (Zero → Medium → High)

---

## What This Lab Is About

Students build a mental model of how operating systems manage **environment variables**, **process scope**, and **execution paths** — three concepts that underpin nearly every security tool, deployment pipeline, and configuration management system they will encounter in the real world.

The lab is split into three tiers of increasing permanence and consequence:

| Lab | Environment | What Students Do | Risk |
|-----|-------------|------------------|------|
| [L1.0.1](./lab-1.0.1-sandbox/) | Local terminal session | Create session variables, observe process isolation, use `export` | Zero — nothing persists |
| [L1.0.2](./lab-1.0.2-shared-container/) | Shared classroom API | Set `TARGET_GATEWAY`, run a submission script, break it intentionally | Medium — network interaction |
| [L1.0.3](./lab-1.0.3-bare-metal/) | Bare-metal Linux install | Edit `.bashrc`, install a custom script into `~/.local/bin`, modify `PATH` | High — permanent system changes |

The three labs are designed to be run in order within a single class period.

---

## Learning Objectives

By the end of Lab 1.0, students will be able to:

- Distinguish between session variables and exported environment variables
- Explain why child processes do not inherit unexported variables
- Use `printenv`, `export`, and `source` to inspect and modify the environment
- Identify `~/.local/bin` as the XDG-standard location for user scripts
- Modify `$PATH` safely and reload a shell profile without restarting
- Understand that environment variable integrity is a security concern, not just a convenience issue

---

## Repository Structure

```
Lab-1.0-Shell-Environment-Configuration/
│
├── lab-1.0.1-sandbox/
│   └── LESSON.md               Student instructions (no files to deploy)
│
├── lab-1.0.2-shared-container/
│   ├── LESSON.md               Student instructions
│   ├── lab-1.0-api-send        Student submission script (copy to local machine)
│   └── api/
│       ├── app.py              Flask API server (teacher deploys this)
│       ├── Dockerfile
│       ├── docker-compose.yml
│       └── requirements.txt
│
└── lab-1.0.3-bare-metal/
    ├── LESSON.md               Student instructions
    └── mason-cyber-syscheck    Reference copy of the syscheck script
```

---

## Teacher Quick Start

See [TEACHER_SETUP.md](./TEACHER_SETUP.md) for full pre-class setup, grading, and teardown instructions.

The short version for L1.0.2 and L1.0.3:

```shell
cd lab-1.0.2-shared-container/api
docker compose up -d
```

Then give students the host machine's IP address on the classroom network. They configure `TARGET_GATEWAY` and submit. Watch the live dashboard at `http://<your-ip>:8080`.
