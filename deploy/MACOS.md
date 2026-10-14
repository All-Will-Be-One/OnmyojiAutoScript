# macOS headless installation

Use Homebrew `adb` and `uv`, then run `bash deploy/macos.sh install` (Python 3.10).
The server and Python API do not require the Windows Qt GUI or OASX.
Apple Silicon uses an lxml wheel; Windows-only dependencies are marked accordingly.

Copy `config/template.json` to a named local config, e.g. `config/k70e.json`.
Set `config_name`, `script.device.serial`, `screenshot_method: "ADB"`,
`control_method: "adb"`, and the actual installed game package.
Disable every task's `scheduler.enable` until its settings have been reviewed.
Local configs, screenshots, and logs must not be committed.

Commands from the repository root:

```sh
bash deploy/macos.sh check k70e   # JSON diagnostic report; no taps/game tasks
bash deploy/macos.sh serve       # foreground API on 127.0.0.1:22267
curl -fsS http://127.0.0.1:22267/home/test
curl -fsS http://127.0.0.1:22267/config_list
curl -fsS http://127.0.0.1:22267/openapi.json
.venv/bin/python -m unittest discover -s tests -p test_non_windows_device.py
```

Agent access uses the existing API and Python modules. Do not call a config's
`/start` endpoint merely to check installation: it starts its task scheduler.
The JSON check reports device transport/OCR separately from game readiness.

OAS expects a 1280x720 landscape game surface. A phone at its native tall-screen
resolution is connected but is not game-ready. Before opening the game, the
operator can explicitly apply `adb -s SERIAL shell wm size 720x1280` and later
restore with `adb -s SERIAL shell wm size reset`. The check never changes display
settings. Game login, layout compatibility, and actual task execution require
separate validation with the game installed and open.

On phones, the expanded courtyard menu may place the shikigami icon farther
left and hide the buff icon. Login and navigation also recognize the combination
of the shikigami and shop icons; both must be visible for this fallback.
DailyTrifles does not require the Windows-only `winerror` module.
Phone safe-area offsets are supported for the back button, gift-room daily tab,
and TalismanPass page marker. The shop recommendation page also recognizes its
Chinese title when the currency icon differs from the original template.

Live validation on the CN mobile client still required agent assistance to close
the courtyard sign-in/result overlays. Treat login plus harvest as supervised;
task completion alone does not prove every overlay has closed or every reward
was claimed. Leave recurring schedules disabled until the desired task chain
has been validated without assistance.

Set deploy.yaml to local-only host, disable auto-updates (to preserve fork fixes),
and use the virtual environment's Python path and Homebrew ADB path. Neither
background scheduling nor login-time startup is required for agent use.
