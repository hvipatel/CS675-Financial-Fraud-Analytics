# Troubleshooting — the five stumbles you'll hit

Reference page. When something goes wrong with Docker, the cause is usually one of these. Each entry: what the error looks like → why it happens → how to fix.

## 1. "port is already allocated"

```
Error response from daemon: driver failed programming external connectivity on endpoint demo-web:
Bind for 0.0.0.0:8888 failed: port is already allocated
```

**Why:** another container, another local service (Jupyter, a Flask dev server, etc.), or a stale container from a previous run is already listening on that port.

**Fix:**

```bash
docker ps                          # see what's running
docker rm -f <container-id>        # kill the offender if it's a leftover container
# OR change the host-side port in docker-compose.yml: "8889:8888"
```

If `docker ps` shows nothing, the conflict is a non-Docker process. On macOS / Linux: `lsof -i :8888`. On Windows: `netstat -ano | findstr :8888`.

## 2. "Cannot connect to the Docker daemon"

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

**Why:** the daemon isn't running.

**Fix:**

- **macOS / Windows** — open Docker Desktop. Wait for the whale icon to stop pulsing.
- **Linux** — `sudo systemctl start docker` (and `sudo systemctl enable docker` to auto-start on boot).

If Docker Desktop refuses to start, restart it; if it still won't, restart the host.

## 3. Apple Silicon — `linux/amd64` warnings

```
The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)
```

**Why:** the image was built for Intel/AMD CPUs (`amd64`); your Mac has Apple Silicon (`arm64`). Docker Desktop emulates `amd64` via Rosetta — usually slower but functional.

**Fix:** most of the time, ignore the warning. If something behaves oddly (crashes, missing libraries):

- Look for an `arm64` variant of the same image — most popular images (`python`, `nginx`, `jupyter/pyspark-notebook`) publish both.
- Or pin the platform explicitly in your compose file: `platform: linux/arm64`.

## 4. Linux — "permission denied" on every docker command

```
Got permission denied while trying to connect to the Docker daemon socket
```

**Why:** Docker's socket is owned by `root` and the `docker` group. Your user isn't in that group yet.

**Fix:**

```bash
sudo usermod -aG docker $USER
# log out and log back in (or `newgrp docker` for the current shell)
docker ps                          # now works without sudo
```

This is a one-time fix per user on a Linux machine.

## 5. First `compose up` takes forever

```bash
$ docker compose up -d
[+] Pulling pyspark-notebook (quay.io/jupyter/pyspark-notebook:latest)...
24a89be8a559 Downloading [=>                   ]  47.2MB / 1.41GB
```

**Why:** Docker is pulling the image's layers from a remote registry. Big data-science images (PySpark, TensorFlow) are often 1–2 GB.

**Fix:** wait — this happens only on the first run. Once layers are cached locally, subsequent `compose up` calls take seconds.

If it stalls completely, your network probably can't reach the registry. Try `docker pull <image>` directly to see the raw error; on enterprise networks the registry hostname may be blocked.

## Bonus: bind mount changes not showing up

```
# edited host file, container still sees the old version
```

**Why:** usually a typo in the bind-mount path, or you're editing a different copy of the file than the one mounted.

**Fix:**

```bash
docker compose exec <service> cat /path/to/file/in/container
```

Confirm the container sees the right content. If not, check the `volumes:` block in your compose file — paths are `host:container`, and a typo in the host side fails silently. Restart the service after fixing: `docker compose restart <service>`.

---

**Most other issues** fall into "container starts but the app inside crashes." For those, the first move is always `docker compose logs <service>` — the app's own error message tells you what's wrong, not Docker.
