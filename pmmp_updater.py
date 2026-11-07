#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.github.com/repos/axolotl-pm/PocketMine-MP/releases/latest"
PHAR_NAME = "PocketMine-MP.phar"
STATE_NAME = ".pmmp_updater.json"
BACKUP_DIR = "backups"
USER_AGENT = "PocketMine-AutoUpdater/1.1"


class UpdaterError(Exception):
    pass


def request_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read()
    try:
        data = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UpdaterError("The GitHub release API returned invalid JSON.") from exc
    if not isinstance(data, dict):
        raise UpdaterError("The GitHub release API returned an unexpected response.")
    return data


def get_latest_build():
    data = request_json(API_URL)
    if data.get("draft") or data.get("prerelease"):
        raise UpdaterError("GitHub returned a draft or prerelease instead of a stable release.")

    version = str(data.get("tag_name") or "").strip()
    if not version:
        raise UpdaterError("The GitHub release did not include a version tag.")

    assets = data.get("assets")
    if not isinstance(assets, list):
        raise UpdaterError("The GitHub release did not include a valid assets list.")

    download_url = None
    for asset in assets:
        if isinstance(asset, dict) and asset.get("name") == PHAR_NAME:
            download_url = asset.get("browser_download_url")
            break

    parsed = urllib.parse.urlparse(download_url or "")
    if parsed.scheme != "https" or parsed.hostname != "github.com":
        raise UpdaterError(f"The release {version} does not contain a valid {PHAR_NAME} download.")

    return {
        "build": version,
        "version": version,
        "channel": "stable",
        "download_url": download_url,
        "published_at": str(data.get("published_at", "unknown")),
    }


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_state(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def is_server_running(server_dir):
    target = str((server_dir / PHAR_NAME).resolve()).encode()
    proc = Path("/proc")
    if not proc.is_dir():
        return False
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        try:
            command = (entry / "cmdline").read_bytes()
        except (OSError, PermissionError):
            continue
        if target in command and int(entry.name) != os.getpid():
            return True
    return False


def download_phar(url, destination):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response:
        final_url = urllib.parse.urlparse(response.geturl())
        if final_url.scheme != "https":
            raise UpdaterError("The download redirected to a non-HTTPS URL.")
        with destination.open("wb") as output:
            shutil.copyfileobj(response, output)
    if not destination.is_file() or destination.stat().st_size < 100_000:
        destination.unlink(missing_ok=True)
        raise UpdaterError("The downloaded PHAR is missing or unexpectedly small.")
    with destination.open("rb") as file:
        beginning = file.read(4096).lower()
    if b"<html" in beginning or b"<!doctype" in beginning:
        destination.unlink(missing_ok=True)
        raise UpdaterError("The download returned a webpage instead of a PHAR file.")


def update_server(server_dir, latest):
    phar = server_dir / PHAR_NAME
    state_path = server_dir / STATE_NAME
    state = read_state(state_path)
    current_build = state.get("build")
    if phar.exists() and str(current_build) == str(latest["build"]):
        print(f"PocketMine-MP {latest['version']} is already up to date.")
        return

    if is_server_running(server_dir):
        raise UpdaterError("PocketMine-MP appears to be running. Stop the server before updating.")

    print(f"Latest available: PocketMine-MP {latest['version']}")
    if phar.exists():
        backup_dir = server_dir / BACKUP_DIR
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = backup_dir / f"PocketMine-MP-{stamp}.phar"
        shutil.copy2(phar, backup)
        print(f"Backup created: {backup}")

    fd, temp_name = tempfile.mkstemp(prefix=".pmmp-download-", suffix=".phar", dir=server_dir)
    os.close(fd)
    temp_path = Path(temp_name)
    try:
        print("Downloading PocketMine-MP...")
        download_phar(latest["download_url"], temp_path)
        os.replace(temp_path, phar)
    finally:
        temp_path.unlink(missing_ok=True)

    state = {
        "build": latest["build"],
        "version": latest["version"],
        "channel": latest["channel"],
        "published_at": latest["published_at"],
        "sha256": sha256_file(phar),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print("PocketMine-MP update installed successfully.")


def start_server(server_dir):
    start_script = server_dir / "start.sh"
    if start_script.is_file():
        print("Starting server with start.sh...")
        if os.access(start_script, os.X_OK):
            command = [str(start_script)]
        else:
            command = ["sh", str(start_script)]
    else:
        phar = server_dir / PHAR_NAME
        if not phar.is_file():
            raise UpdaterError(f"{PHAR_NAME} was not found after the update.")
        php = None
        for candidate in (server_dir / "bin" / "php7" / "bin" / "php", server_dir / "bin" / "php" / "bin" / "php"):
            if candidate.is_file() and os.access(candidate, os.X_OK):
                php = str(candidate)
                break
        if not php:
            php = shutil.which("php")
        if not php:
            raise UpdaterError("PHP was not found. Install a compatible PHP runtime or provide start.sh.")
        command = [php, str(phar)]

    print("Server is starting. Press Ctrl+C to stop it.")
    try:
        result = subprocess.run(command, cwd=server_dir)
    except FileNotFoundError as exc:
        raise UpdaterError(f"Could not start the server: {exc}") from exc
    if result.returncode != 0:
        raise UpdaterError(f"PocketMine-MP exited with status {result.returncode}.")


def main():
    parser = argparse.ArgumentParser(
        description="Check for PocketMine-MP updates, install them, and start your server."
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="PocketMine-MP server directory (default: current directory).",
    )
    args = parser.parse_args()
    server_dir = Path(args.dir).expanduser().resolve()
    if not server_dir.is_dir():
        raise UpdaterError(f"Server directory does not exist: {server_dir}")

    print(f"Server directory: {server_dir}")
    latest = get_latest_build()
    update_server(server_dir, latest)
    start_server(server_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(130)
    except (UpdaterError, urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
