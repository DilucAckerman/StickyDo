## Optional: Background Blur

StickyDo uses Wayland layer-shell for its panel, which supports background
blur — but blur is a *compositor-level* effect, so it requires a small
addition to your Hyprland config to enable. Without this step, StickyDo
still works fully and looks translucent (via its own CSS theming) — it
just won't have the frosted-glass blur behind it.

### For Hyprland

Add the contents of [`hyprland/stickydo-layerrules.conf`](hyprland/stickydo-layerrules.conf)
to your Hyprland configuration.

- If you use a plain, single-file setup, add the lines directly to
  `~/.config/hypr/hyprland.conf`
- If you use a dotfile framework or modular config that sources multiple
  files, add the lines to whichever file is meant for personal
  customizations (check your framework's documentation) rather than
  editing framework-managed files directly

Then reload:
```bash
hyprctl reload
```

If you get a config error mentioning `invalid field`, your Hyprland version
likely uses the older layer-rule syntax — see the commented alternative
inside the config file itself.
