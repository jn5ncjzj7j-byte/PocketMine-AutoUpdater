# PocketMine AutoUpdater

A small Python launcher that checks the official PocketMine-MP update API, installs the latest available PocketMine-MP 5 build when needed, and then starts your server.

Run one command:

```bash
python3 pmmp_updater.py
```

It uses the current directory by default. You can point it at another server folder:

```bash
python3 pmmp_updater.py --dir /home/ubuntu/pocketmine
```

## Features

- Checks the official PocketMine-MP 5 update API on every launch.
- Downloads and installs a newer build when needed.
- Creates a timestamped PHAR backup before replacing an existing server PHAR.
- Leaves worlds, plugins, configuration, and other server files untouched.
- Starts the server after the update check, even when no update is needed.
- Uses your existing `start.sh` when present; otherwise it runs the PHAR with PHP.

## Requirements

- Linux, Windows, macOS, or another environment with Python 3.
- Internet access for the update check and download.
- A PHP runtime compatible with the PocketMine-MP build.
- An existing server directory, or an empty directory for the first PHAR download.

The script updates the PocketMine-MP PHAR only. It does **not** install or update PHP. PocketMine-MP requires a compatible PHP build and extensions. Keeping the official `start.sh` and bundled `bin/` runtime is recommended.

## Download and install

### Option 1: Clone with Git (recommended)

Install Git and Python 3 first, then download the project:

```bash
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Keep the updater in this folder, or copy `pmmp_updater.py` into your PocketMine server folder.

### Option 2: Download only the Python script

If you do not want to clone the repository:

```bash
mkdir -p PocketMine-AutoUpdater
cd PocketMine-AutoUpdater
curl -L -o pmmp_updater.py https://raw.githubusercontent.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater/main/pmmp_updater.py
```

You can also open the [latest source file](https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater/blob/main/pmmp_updater.py) and use GitHub's **Raw** button.

### Linux (Ubuntu / Debian)

Install the required download tools:

```bash
sudo apt update
sudo apt install -y python3 git curl
```

Then clone and enter the project:

```bash
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Run it against a server in the current directory:

```bash
python3 pmmp_updater.py
```

Or point it at your server directory:

```bash
python3 pmmp_updater.py --dir /home/ubuntu/pocketmine
```

### Windows (PowerShell)

1. Install **Python 3** from [python.org](https://www.python.org/downloads/windows/). During setup, enable **Add Python to PATH**.
2. Install Git from [git-scm.com](https://git-scm.com/download/win) if you want to clone the repository.
3. Open PowerShell and download the project:

```powershell
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

If you do not want to install Git, download just the updater:

```powershell
New-Item -ItemType Directory -Force PocketMine-AutoUpdater
Set-Location PocketMine-AutoUpdater
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater/main/pmmp_updater.py" -OutFile "pmmp_updater.py"
```

Run it for a server in the current directory:

```powershell
py pmmp_updater.py
```

Or specify the server folder:

```powershell
py pmmp_updater.py --dir "C:\PocketMine"
```

**Windows notes:**
- Make sure a Windows-compatible PHP runtime that meets PocketMine-MP's requirements is available in your PATH. The updater does not install PHP.
- If your server folder has a Unix `start.sh`, it cannot be launched natively by Windows. The fallback is to run `PocketMine-MP.phar` with `php`.
- Stop the PocketMine server yourself before running the updater. Automatic running-process detection currently works through Linux `/proc`, not Windows.
- If you use the official Windows PocketMine package or a bundled PHP runtime, check that its startup method and PHP executable are available to this script; otherwise run the updater in the same environment that provides the server's PHP runtime.

### Termux (Android)

Install the tools in Termux:

```bash
pkg update
pkg install -y python git
```

Download the project:

```bash
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Run the updater with the path to your PocketMine server:

```bash
python pmmp_updater.py --dir /path/to/pocketmine
```

**Termux note:** This installs the Python updater in Termux, but it does not make PocketMine's PHP runtime compatible with native Android/Termux. If your PocketMine server runs inside Ubuntu using `proot-distro`, install Git and Python inside that Ubuntu environment and clone the project there. Run the updater from the same environment as the server, using the Ubuntu server directory path.

Example inside Ubuntu:

```bash
apt update
apt install -y python3 git curl
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
python3 pmmp_updater.py --dir /home/ubuntu/pocketmine
```

### Other Linux distributions

Install Python 3, Git, and curl using your distribution's package manager, then use the Git clone commands above. The updater itself uses only Python's standard library; Git and curl are needed only for downloading the project with these examples.

## Installation

1. Put `pmmp_updater.py` in your server directory, or keep it elsewhere and use `--dir`.
2. Make sure the server directory has a working `start.sh` or a compatible `php` command is available.
3. Run:

   ```bash
   python3 pmmp_updater.py
   ```

Optional executable mode:

```bash
chmod +x pmmp_updater.py
./pmmp_updater.py
```

## Examples

Start the server in the current directory:

```bash
python3 pmmp_updater.py
```

Update and start a server stored elsewhere:

```bash
python3 pmmp_updater.py --dir /home/ubuntu/pocketmine
```

Run it from any directory using an absolute script path:

```bash
python3 /path/to/pmmp_updater.py --dir /home/ubuntu/pocketmine
```

## Backups and update state

Before replacing an existing `PocketMine-MP.phar`, the script copies it into `backups/`.

The file `.pmmp_updater.json` stores the last installed build number. If this file is missing, the updater downloads the currently advertised build on the next run.

Your worlds and plugins are not intentionally changed. Keep separate regular backups of important server data.

## Important notes

- Stop the server before running the updater. On Linux, it checks `/proc` for a process using this server's PHAR and refuses to update if detected.
- The updater does not manage PHP versions or extensions.
- If `start.sh` exists, it is used to start the server. Otherwise, the script looks for `php` on your PATH and then checks common bundled PHP paths.
- The updater targets PocketMine-MP 5 using `https://update.pmmp.io/api?version=5`.
- PocketMine-MP's maintainers announced that the project would no longer receive new Minecraft-version updates. This tool can install only builds still made available by the configured update API; it cannot create new upstream releases.

## Troubleshooting

**“PHP was not found”**

Install a PHP runtime compatible with your PocketMine-MP build, or restore the official server `start.sh` and its bundled `bin/` runtime.

**The server exits immediately**

Run the server's `start.sh` manually to see its error output. Check that its PHP runtime and required extensions are present.

**The updater refuses to update because the server is running**

Stop the PocketMine-MP process first, then run the updater again.

**The API or download request fails**

Check your internet connection and try again later. The updater needs access to `update.pmmp.io` and the HTTPS download host returned by its API.

## Links

- [PocketMine-MP](https://github.com/pmmp/PocketMine-MP)
- [Official update API](https://update.pmmp.io/api?version=5)
- [Manual installation documentation](https://doc.pmmp.io/en/rtfd/installation/installing-manually.html)
