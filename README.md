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
- A PocketMine-compatible PHP runtime for the target operating system and architecture.
- An existing server directory, or an empty directory for the first PHAR download.

### PHP version and runtime requirements

The current Axolotl-PM 5.x release line requires **PHP 8.1 or newer**. **PHP 8.4** is the recommended PM5 runtime. Use a PocketMine-specific PHP build with the required extensions; a generic PHP package from `apt` or another package manager may not include them.

**This updater does not install or update PHP.** It only replaces `PocketMine-MP.phar`.

When starting the PHAR directly, the updater checks these bundled PHP paths first:

1. `<server directory>/bin/php7/bin/php`
2. `<server directory>/bin/php/bin/php`
3. `php` available in your PATH

Put the PocketMine PHP build's `bin/` directory inside the server directory. This lets the updater use the bundled runtime instead of accidentally selecting an incompatible system PHP. If you have a working `start.sh`, the updater uses that script instead.

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

**Important:** Installing the Python updater in Termux does not install PocketMine's PHP runtime. Axolotl-PM 5.x requires PHP 8.1 or newer; PHP 8.4 is the recommended PM5 runtime. Use the PocketMine-specific PHP build for your Android architecture, not the generic PHP package installed by `apt` or `pkg`.

#### Ubuntu PRoot on Android ARM64 (aarch64)

The following example installs the Android ARM64 PHP 8.4 build tested with Ubuntu PRoot. Run these commands inside the Ubuntu PRoot shell:

```bash
mkdir -p /tmp/pmmp-php
cd /tmp/pmmp-php

curl -fL "https://github.com/axolotl-pm/PHP-Binaries/releases/download/pm5-php-8.4-latest/PHP-8.4-Android-arm64-PM5.tar.gz" -o php.tar.gz
tar -xzf php.tar.gz
```

Copy the bundled `bin/` directory into the PocketMine server directory. For a server in `/root`:

```bash
cp -a /tmp/pmmp-php/bin /root/
```

For a server in another directory, replace `/root` with that server directory. Confirm the PHP binary works and includes PocketMine extensions:

```bash
/root/bin/php7/bin/php -v
/root/bin/php7/bin/php -m
```

You should see PHP 8.4.x and extensions including `chunkutils2`, `curl`, `crypto`, `encoding`, `gmp`, `igbinary`, `leveldb`, `mbstring`, `morton`, `pmmpthread`, `yaml`, and `zip`.

The updater checks the server's bundled `bin/php7/bin/php` before the system PHP in PATH, so it will use this runtime when launching the PHAR directly. Keep the `bin/` directory inside the server folder.

If your server runs inside Ubuntu with `proot-distro`, install and run the updater inside that same Ubuntu environment:

```bash
apt update
apt install -y python3 git curl
git clone https://github.com/jn5ncjzj7j-byte/PocketMine-AutoUpdater.git
cd PocketMine-AutoUpdater
python3 pmmp_updater.py --dir /root
```

Use a PHP archive that matches your actual Android architecture. The URL above is specifically for Android ARM64; do not use it on x86_64 or other architectures.

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
- If `start.sh` exists, it is used to start the server. Otherwise, the script checks `bin/php7/bin/php` and `bin/php/bin/php` inside the server directory first, then looks for `php` on PATH.
- The updater currently follows the Axolotl-PM community-maintained PocketMine-MP fork: `https://github.com/axolotl-pm/PocketMine-MP`.
- This is a community fork, not the original PocketMine-MP maintainers' release channel. Check the fork's compatibility notes before updating an existing production server.

</details>

<details>
<summary>Troubleshooting</summary>

## Troubleshooting

**“PHP was not found”**

Install a PocketMine-compatible PHP runtime (PHP 8.1 or newer for Axolotl-PM 5.x; PHP 8.4 is recommended), including the required PocketMine extensions. Put its `bin/` folder inside the server directory, or restore the server's working `start.sh` and bundled runtime.

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

