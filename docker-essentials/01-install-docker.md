# Lesson 01 — Install Docker

> **Goal:** install Docker + the Compose v2 plugin on your OS, then verify with one command.

---

## What you're installing

Two pieces ship together in modern Docker:

| Piece | What it is |
|---|---|
| **Docker Engine** (`docker`) | The daemon + CLI that builds and runs containers. |
| **Compose plugin** (`docker compose`) | Subcommand that runs multi-container apps from a YAML file. Bundled with Docker Desktop and with the official Linux packages since 2022. |

> The standalone `docker-compose` (hyphenated, Python-based v1) is **deprecated**. Use `docker compose` (space, Go-based v2) everywhere.

---

## macOS

**Recommended: Docker Desktop** — easiest, includes Compose, works on Apple Silicon and Intel.

```bash
brew install --cask docker        # or download from docker.com/products/docker-desktop
open -a Docker                    # first launch; accept the license
```

Alternatives if you don't want Docker Desktop:

| Tool | Install |
|---|---|
| **OrbStack** (fastest on Apple Silicon) | `brew install --cask orbstack` |
| **Colima** (CLI-only, free, OSS) | `brew install colima docker docker-compose && colima start` |

All three give you the same `docker` and `docker compose` commands.

---

## Linux (Ubuntu / Debian)

Use Docker's official apt repo — the distro-packaged `docker.io` is older and bundles v1 Compose only.

```bash
# 1. Repo + GPG key
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
    | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 2. Install engine + compose plugin
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin

# 3. Run docker without sudo (log out / back in after this)
sudo usermod -aG docker $USER
newgrp docker
```

For Fedora / RHEL, swap step 1–2 for:

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER && newgrp docker
```

---

## Windows

**Docker Desktop with the WSL2 backend** is the only path you should use. WSL2 ships with Windows 10/11.

1. Install WSL2 (PowerShell as admin, then reboot):
   ```powershell
   wsl --install
   ```
2. Download and run **Docker Desktop for Windows**: <https://docs.docker.com/desktop/install/windows-install/>
3. During setup leave **"Use WSL 2 instead of Hyper-V"** checked.
4. After install, open *Settings → Resources → WSL Integration* and enable your default distro.

You can now run `docker` from PowerShell, cmd, or any WSL shell — they all talk to the same daemon.

> **Avoid:** the legacy *Docker Toolbox* and the standalone `docker-compose.exe` binary. Neither is needed; both are deprecated.

---

## Verify (all platforms)

```bash
$ docker --version
Docker version 27.3.1, build ce12230

$ docker compose version
Docker Compose version v2.29.7

$ docker run --rm hello-world
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

If all three commands succeed, you're done. If `hello-world` fails:

| Symptom | Fix |
|---|---|
| `Cannot connect to the Docker daemon` (Mac/Win) | Docker Desktop / OrbStack / Colima isn't running — start it. |
| `Cannot connect to the Docker daemon` (Linux) | `sudo systemctl start docker` and confirm your user is in the `docker` group (`groups` should list it). |
| `permission denied … /var/run/docker.sock` (Linux) | You added yourself to `docker` group but didn't open a new shell — run `newgrp docker` or log out/in. |
| `docker compose` says *unknown command* | You installed the v1 standalone, not the plugin. Reinstall using the official repo above (Linux) or upgrade Docker Desktop (Mac/Win). |

---

## Practice

1. Run all three verify commands above and confirm they succeed.
2. Run `docker info | grep -E "Server Version|Operating System|Architecture"` — sanity-check the engine sees your OS/arch correctly.
3. List images: `docker image ls` — `hello-world` should be there from the verify step.

> **Done?** Continue to [Lesson 02 — Test with Compose + a custom network](./02-test-with-compose.md).
