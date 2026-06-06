# Docker Essentials

Install Docker on any OS, then prove it works end-to-end with a multi-service `docker compose` stack on a user-defined bridge network.

## Who this is for

Engineers who want the smallest set of moving parts that lets them:

- Install Docker correctly on **macOS, Linux, or Windows**
- Run a multi-container app via `docker compose`
- Wire services together on a **custom bridge network** (DNS by service name)
- Verify it all works with one command, then tear it down cleanly

No prior Docker knowledge assumed. We use **Compose v2** (`docker compose`, no hyphen) throughout — `docker-compose` (v1) is end-of-life.

## Learning path

| # | Lesson | What you'll do |
|---|---|---|
| 01 | [Install Docker](./01-install-docker.md) | Install + post-install verify on macOS / Linux / Windows |
| 02 | [Test with Compose + a custom network](./02-test-with-compose.md) | Bring up `nginx + alpine-client` on `demo-net`, prove service-name DNS resolves |
| —  | [`compose-demo/`](./compose-demo/) | Self-contained demo stack (the file you actually run) |
| 99 | [Troubleshooting](./99-troubleshooting.md) | The five stumbles you'll hit and how to fix them |

## TL;DR — 60-second smoke test

After installing Docker (lesson 01):

```bash
cd docker-essentials/compose-demo

docker compose up -d                          # start web + client on demo-net
docker compose exec client curl -s http://web | head -n 5   # service-name DNS works
docker network inspect demo-net               # see both containers attached
docker compose down                           # clean up (network removed too)
```

If `curl http://web` returns the nginx welcome page, your install + Compose + custom networking are all healthy.

## Cross-platform guarantee

The `compose-demo/docker-compose.yml` only uses portable features — no bind mounts, no host networking, no platform-specific images. The same file runs identically on:

- macOS (Docker Desktop, Colima, OrbStack)
- Linux (Docker Engine + Compose plugin)
- Windows (Docker Desktop with WSL2 backend, PowerShell or cmd)
