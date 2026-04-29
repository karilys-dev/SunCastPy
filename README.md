#  DevOps Refresh: Docker, DevContainers & Python Packaging

##  About

This repository is part of my journey back into DevOps fundamentals.

The goal is to refresh and strengthen core skills by focusing on:
- Using Docker with VSCode DevContainers
- Building clean and reproducible development environments
- Exploring Python packaging by creating a simple weather package

This project is intentionally simple in scope but focused on doing things **the right way**, not just making them work.

---

##  Objectives

- Rebuild a local development workflow using **VSCode DevContainers**
- Run containers as a **non-root user**
- Understand and fix common DevContainer issues (e.g. UID mismatch, permissions)
- Explore when and why to use a **virtual environment inside a container**
- Create a simple, structured **Python package**
- Reinforce best practices that translate into real-world DevOps and backend systems

---

##  DevContainer Setup

This project uses VSCode DevContainers to create a consistent development environment.

### Key Learnings

- Running containers as a non-root user improves security and mirrors production practices
- DevContainers may fail silently due to **UID and permission mismatches**
- A simple but critical fix: 

```json
// .devcontainer/devcontainer.json
"updateRemoteUserUID": true
```

## Forecast
- A forecast report can be created using github actions and it will show up as a github page

## GitHub Actions
- Run on Pull Request
- Create Forecast report
