# PocketMine AutoUpdater

A small Python launcher that checks the latest stable release from the Axolotl-PM PocketMine-MP GitHub repository, installs its PHAR when needed, and then starts your server.

Run one command:

```bash
python3 pmmp_updater.py
```

It uses the current directory by default. You can point it at another server folder:

```bash
python3 pmmp_updater.py --dir /home/ubuntu/pocketmine
```

<details>
<summary>Features</summary>

## Features

- Checks the latest stable Axolotl-PM release through the GitHub Releases API on every launch.
- Downloads and installs a newer build when needed.
- Creates a timestamped PHAR backup before replacing an existing server PHAR.
- Leaves worlds, plugins, configuration, and other server files untouched.
- Starts the server after the update check, even when no update is needed.
- Uses your existing `start.sh` when present; otherwise it runs the PHAR with PHP.

</details>

<details>
<summary>Requirements and PHP setup</summary>

## Requirements

- Linux, Windows, macOS, or another environment with Python 3.
- Internet access for the update check and download.
- A PHP runtime compatible with the PocketMine-MP build.
- An existing server directory, or an empty directory for the first PHAR download.

### PHP version and runtime requirements

The current Axolotl-PM 5.x release line requires **PHP 8.1 or newer**. The recommended PHP build for PocketMine-MP 5.x is currently **PHP 8.4**. Use the PocketMine-specific PHP binary, which includes the extensions PocketMine needs; a generic PHP installation may be missing required extensions.

**This updater does not install or update PHP.** It only replaces `PocketMine-MP.phar`. Updating the PHAR does not automatically update your PHP runtime.

- If your server has the official `start.sh` and bundled `bin/` folder, keep them together and let `start.sh` launch the server.
- If the updater has to launch the PHAR directly, the `php` command in your PATH must point to a compatible PocketMine PHP runtime.
- Before updating an existing server, check that its PHP runtime supports the release you are installing. If it is too old or lacks required extensions, update the PHP runtime separately before starting the new PHAR.

See the [Axolotl-PM PHP requirements](https://axolotl-pm.org/docs/migrating-from-pocketmine-mp#php), [recommended PHP binaries](https://github.com/axolotl-pm/PHP-Binaries/releases), and [manual installation guide](https://axolotl-pm.org/docs/installation/installing-manually).

</details>

## Download and install

<details>
<summary>Download and install</summary>

Choose your operating system below to see the instructions.

<details>
<summary>Download the updater (any OS)</summary>

**Option 1: Clone with Git (recommended)**

Install Git and Python 3 first, then run:

```bash
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Keep the updater in this folder, or copy `pmmp_updater.py` into your PocketMine server folder.

**Option 2: Download only the Python script**

On Linux, macOS, or Termux:

```bash
mkdir -p PocketMine-AutoUpdater
cd PocketMine-AutoUpdater
curl -L -o pmmp_updater.py https://raw.githubusercontent.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater/main/pmmp_updater.py
```

On Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force PocketMine-AutoUpdater
Set-Location PocketMine-AutoUpdater
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater/main/pmmp_updater.py" -OutFile "pmmp_updater.py"
```

You can also open the [latest source file](https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater/blob/main/pmmp_updater.py) and use GitHub's **Raw** button.

</details>

<details>
<summary>Linux (Ubuntu / Debian)</summary>

Install the required tools:

```bash
sudo apt update
sudo apt install -y python3 git curl
```

Download the project:

```bash
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Run it for a server in the current directory:

```bash
python3 pmmp_updater.py
```

Or specify your server directory:

```bash
python3 pmmp_updater.py --dir /home/ubuntu/pocketmine
```

</details>

<details>
<summary>Windows (PowerShell)</summary>

1. Install [Python 3](https://www.python.org/downloads/windows/). During setup, enable **Add Python to PATH**.
2. Install [Git](https://git-scm.com/download/win) if you want to clone the repository.

Open PowerShell and run:

```powershell
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Or download only the script:

```powershell
New-Item -ItemType Directory -Force PocketMine-AutoUpdater
Set-Location PocketMine-AutoUpdater
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater/main/pmmp_updater.py" -OutFile "pmmp_updater.py"
```

Run it:

```powershell
py pmmp_updater.py
```

Or specify your server directory:

```powershell
py pmmp_updater.py --dir "C:\PocketMine"
```

**Windows notes:**
- Use a PocketMine-compatible Windows PHP runtime. Axolotl-PM 5.x requires PHP 8.1 or newer; PHP 8.4 is currently the recommended PM5 build. Download the PocketMine-specific Windows binary, not a generic PHP package. The updater does not install or update PHP.
- A Unix `start.sh` cannot be launched natively by Windows. The fallback is to run `PocketMine-MP.phar` with `php`.
- Stop the server yourself before running the updater. Automatic running-process detection currently works through Linux `/proc`, not Windows.
- If you use a bundled PHP runtime, make sure its PHP executable is available to the script, or run the updater in the same environment as the server.

</details>

<details>
<summary>Termux (Android)</summary>

Install the tools:

```bash
pkg update
pkg install -y python git
```

Download the project:

```bash
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Run the updater with your PocketMine server path:

```bash
python pmmp_updater.py --dir /path/to/pocketmine
```

**Important:** Installing the Python updater in Termux does not install PocketMine's PHP runtime. Axolotl-PM 5.x requires PHP 8.1 or newer and PocketMine-specific extensions; PHP 8.4 is currently the recommended PM5 build. Use a compatible PocketMine PHP binary for your environment.

If your server runs inside Ubuntu with `proot-distro`, install the updater inside that Ubuntu environment and run it there:

```bash
apt update
apt install -y python3 git curl
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
python3 pmmp_updater.py --dir /home/ubuntu/pocketmine
```

</details>

<details>
<summary>macOS and other Linux distributions</summary>

Install Python 3, Git, and curl using your system's package manager. Then clone the project:

```bash
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
```

Run it:

```bash
python3 pmmp_updater.py
```

Or specify your server directory:

```bash
python3 pmmp_updater.py --dir /path/to/pocketmine
```

Make sure a compatible PocketMine PHP runtime is available, either through your server's `start.sh` or as `php` in your PATH.

</details>



<details>
<summary>Installation</summary>

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

</details>

<details>
<summary>Usage examples</summary>

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

</details>

<details>
<summary>Backups and update state</summary>

## Backups and update state

Before replacing an existing `PocketMine-MP.phar`, the script copies it into `backups/`.

The file `.pmmp_updater.json` stores the last installed release tag. If this file is missing, the updater downloads the latest stable release on the next run.

Your worlds and plugins are not intentionally changed. Keep separate regular backups of important server data.

</details>

<details>
<summary>Important notes</summary>

## Important notes

- Stop the server before running the updater. On Linux, it checks `/proc` for a process using this server's PHAR and refuses to update if detected.
- The updater does not manage PHP versions or extensions. Axolotl-PM 5.x requires PHP 8.1 or newer; PHP 8.4 is currently the recommended PM5 build.
- If `start.sh` exists, it is used to start the server. Otherwise, the script looks for `php` on your PATH and then checks common bundled PHP paths.
- The updater currently follows the Axolotl-PM community-maintained PocketMine-MP fork: `https://github.com/axolotl-pm/PocketMine-MP`.
- This is a community fork, not the original PocketMine-MP maintainers' release channel. Check the fork's compatibility notes before updating an existing production server.

</details>

<details>
<summary>Troubleshooting</summary>

## Troubleshooting

**“PHP was not found”**

Install a PocketMine-compatible PHP runtime (PHP 8.1 or newer for Axolotl-PM 5.x; PHP 8.4 is currently recommended), including the required PocketMine extensions, or restore the server's `start.sh` and bundled `bin/` runtime.

**The server exits immediately**

Run the server's `start.sh` manually to see its error output. Check that its PHP runtime and required extensions are present.

**The updater refuses to update because the server is running**

Stop the PocketMine-MP process first, then run the updater again.

**The API or download request fails**

Check your internet connection and try again later. The updater needs access to `api.github.com` and GitHub's release download host. If GitHub returns an API rate-limit or network error, wait and retry.

</details>

<details>
<summary>Useful links</summary>

## Links

- [Axolotl-PM PocketMine-MP releases](https://github.com/axolotl-pm/PocketMine-MP/releases)
- [Latest release API](https://api.github.com/repos/axolotl-pm/PocketMine-MP/releases/latest)
- [Original PocketMine-MP repository](https://github.com/pmmp/PocketMine-MP)
- [Manual installation documentation](https://doc.pmmp.io/en/rtfd/installation/installing-manually.html)

</details>

