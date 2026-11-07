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

- Linux or another Unix-like environment with Python 3.
- Internet access for the update check and download.
- A PHP runtime compatible with the PocketMine-MP build.
- An existing server directory, or an empty directory for the first PHAR download.

The script updates the PocketMine-MP PHAR only. It does **not** install or update PHP. PocketMine-MP requires a compatible PHP build and extensions. Keeping the official `start.sh` and bundled `bin/` runtime is recommended.

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
