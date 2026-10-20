# Opening and Closing the MPS Project

MoWare application projects run on a standalone MPS install (Linux or Windows). There is **no MCP tool that can open a project**: the MCP server rejects every tool call — `mps_mcp_list_open_projects` included — *before dispatch* unless an open project matches `projectPath`. Opening goes through the MPS command line; closing has its own tool, `mps_mcp_close_project`.

The usual answer to an empty project list is to ask the user to open the project in MPS. Use the command line below only when the user wants you to do it.

## The welcome-screen signature

With MPS running and no project open, every call fails with one of:

```text
Unable to determine the target project for the current MCP tool call.
Currently open projects: {"projects":[]}
```

```text
`projectPath`=`/path/to/checkout` doesn't correspond to any open project.
Currently open projects: {"projects":[]}
```

`"projects":[]` means the welcome screen, not a bad path: do not retry with a guessed `projectPath`. A non-empty list means a project *is* open and you passed a path outside it — take one of the listed paths instead.

If the `mps_mcp_*` tools are missing entirely, MPS is not running or its MCP server is disabled: ask the user to start MPS with the project and enable the server.

## Find the running MPS

Look for the `jetbrains.mps.Launcher` process and note the binary it was started from:

- **Linux:** `ps aux | grep -i '[j]etbrains.mps.Launcher'`; the exact arguments with `tr '\0' '\n' < /proc/<pid>/cmdline` (spaces in paths stay intact). The install's `bin/mps.sh` is the launcher.
- **Windows (PowerShell):** `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'jetbrains.mps.Launcher' }`; the launcher is the install's `bin\mps64.exe`.

The selector `-Didea.paths.selector=MPS<year>.<minor>` (e.g. `MPS2026.2`) identifies the install; a second process only activates the first when it uses the same install (same selector and config/system directories). With Toolbox or several installed versions, take the exact binary from the process list, never a different version from `PATH`. Do not write helper files into the project: use `$TMPDIR` / `%TEMP%`.

## Open the project via the command line

Pass the **absolute project directory** as a positional argument to the same launcher. If MPS is already running, the second process forwards the path to the running IDE and exits within a few seconds; if MPS is not running, the same command starts it with the project open.

```bash
PROJECT="/home/you/work/myProject"
MPS_SH="/opt/mps/bin/mps.sh"        # the exact path from the running process
"$MPS_SH" "$PROJECT"
```

```powershell
$project = "C:\work\myProject"
$mps = "C:\Program Files\JetBrains\MPS 2026.2\bin\mps64.exe"   # the exact path from the running process
& $mps $project
```

On Windows prefer `mps64.exe`: `mps.bat` starts `java` asynchronously, so it returns at once even when it started a new IDE. Then call `mps_mcp_list_open_projects` with `projectPath` set to the opened directory and reuse that path on every later call.

| Observation | Meaning |
|---|---|
| Second process exits 0 within ~2–15 s; MCP then lists the project | Activation worked |
| Second process stays alive, a new IDE window opens | Different install or selector — close it and use the binary of the running process |
| `ACTIVATE_NOT_INITIALIZED` | The running instance is still starting — wait and retry |
| MCP still `"projects":[]` after a clean exit | Opening may still be in progress (indexing) — wait and retry; check the IDE log ([`ide-log.md`](ide-log.md)) for `Opening project` |

## Closing a project

`mps_mcp_close_project` closes the project selected by `projectPath`, like File | Close Project. After the last project closes MPS shows the welcome screen, and reopening needs the command line above.

1. If several projects are open, call `mps_mcp_list_open_projects` and pass the intended `mpsProjectBaseDirectory` as `projectPath` — a path at or inside that project, never an ancestor.
2. Call `mps_mcp_close_project` with the default `force=false`. A normal close saves documents and may show Save or confirmation dialogs; the call waits at most 20 seconds.
3. `{ok:true, data.closed:true}` → done.
4. `code: MODAL_BLOCKED` → a modal dialog is open in MPS. Ask the user to close it, then retry. A `MODAL_BLOCKED` close is **not** a closed project.
5. Close cancelled (the project stays open) → ask the user to complete the dialog, or retry with `force=true`.

`force=true` skips the save and can-close dialogs (unsaved editor changes are discarded); use it only after a timed-out or cancelled close. `shutdownWithLastProject=true` also shuts MPS down when this was the only open project; MPS checks that itself. From the welcome screen MPS cannot be shut down via MCP.
