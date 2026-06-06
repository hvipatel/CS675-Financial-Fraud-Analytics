# compose-demo — minimal Compose + custom-network test

A 2-service stack used to verify Docker, Compose v2, and user-defined bridge networking all work on your machine. Runs identically on macOS, Linux, and Windows.

## Services

| Service | Image | Role |
|---|---|---|
| `web`    | `nginx:alpine` | Serves the default welcome page on container port 80, published to host `:8080`. |
| `client` | `alpine:3.20`  | Idle container with `curl` installed; used to test in-network DNS to `web`. |

Both are attached to a user-defined bridge network named **`demo-net`**.

## Usage

```bash
docker compose up -d                                          # start
docker compose ps                                             # both should be Up
curl -s http://localhost:8080 | head -n 5                     # host -> web (port mapping)
docker compose exec client curl -s http://web | head -n 5     # client -> web (service-name DNS)
docker compose exec client ping -c 2 web                      # raw ICMP, same network
docker network inspect demo-net                               # see both containers attached
docker compose down                                           # stop + remove containers and network
```

`web` has a healthcheck, and `client` waits on `service_healthy` — so as soon as `docker compose up -d` returns, both `curl` tests are guaranteed to succeed without sleeps.

## Why these choices

- **`nginx:alpine` + `alpine:3.20`** — multi-arch (amd64/arm64) so no `platform:` overrides needed.
- **No bind mounts** — avoids macOS/Windows path quirks.
- **Explicit `networks:`** — gives the bridge a stable, inspectable name (`demo-net`).
- **Default `bridge` driver** — works on every host; no Swarm or overlay required.
- **Published port `8080:80`** — host-to-container test that doesn't conflict with anything common.

If port 8080 is already taken on your host, override it without editing the file:

```bash
# macOS / Linux / WSL / Git-Bash
HOST_PORT=18080 docker compose up -d

# Windows PowerShell
$env:HOST_PORT=18080; docker compose up -d
```

Then `curl http://localhost:18080`. The container-side port stays `80`.

## Reset

```bash
docker compose down -v --rmi local
```

Removes containers, the `demo-net` network, any local volumes, and the pulled images.
