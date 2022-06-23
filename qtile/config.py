from libqtile import bar, layout, widget
from libqtile.config import Group, Key, Screen
from libqtile.lazy import lazy
from libqtile import hook

import subprocess
import os
mod = "mod4"
alt = "mod1"
terminal = "alacritty"


# This function was stolen from somewhere in unixporn XD
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])


keys = []

for mod_key in [mod, alt]:
    keys.extend([

        # WINDOW SWITCHING
        Key([mod_key], "h", lazy.layout.left(), desc="Move focus to left"),
        Key([mod_key], "l", lazy.layout.right(), desc="Move focus to right"),
        Key([mod_key], "j", lazy.layout.down(), desc="Move focus down"),
        Key([mod_key], "k", lazy.layout.up(), desc="Move focus up"),
        Key([mod_key], "space", lazy.layout.next(),
            desc="Move window focus to other window"),

        # WINDOW MANAGEMENT
        Key([mod_key, "shift"], "h", lazy.layout.shuffle_left(),
            desc="Move window to the left"),
        Key([mod_key, "shift"], "l", lazy.layout.shuffle_right(),
            desc="Move window to the right"),
        Key([mod_key, "shift"], "j", lazy.layout.shuffle_down(),
            desc="Move window down"),
        Key([mod_key, "shift"], "k",
            lazy.layout.shuffle_up(), desc="Move window up"),
        # Grow windows. If current window is on the edge of screen and direction
        # will be to screen edge - window would shrink.
        Key([mod_key, "control"], "h", lazy.layout.grow_left(),
            desc="Grow window to the left"),
        Key([mod_key, "control"], "l", lazy.layout.grow_right(),
            desc="Grow window to the right"),
        Key([mod_key, "control"], "j", lazy.layout.grow_down(),
            desc="Grow window down"),
        Key([mod_key, "control"], "k",
            lazy.layout.grow_up(), desc="Grow window up"),
        Key([mod_key], "n", lazy.layout.normalize(),
            desc="Reset all window sizes"),
        # Toggle between split and unsplit sides of stack.
        # Split = all windows displayed
        # Unsplit = 1 window displayed, like Max layout, but still with
        # multiple stack panes
        Key(
            [mod_key, "shift"],
            "Return",
            lazy.layout.toggle_split(),
            desc="Toggle between split and unsplit sides of stack",
        ),
        Key([mod_key], "Return", lazy.spawn(terminal), desc="Launch terminal"),
        # Toggle between different layouts as defined below
        Key([mod_key], "Tab", lazy.next_layout(),
            desc="Toggle between layouts"),
        Key([mod_key], "q", lazy.window.kill(), desc="Kill focused window"),
        # SPAWN VSCODE AND FIREFOX
        Key([mod_key], "w", lazy.spawn('firefox')),
        Key([mod_key], "c", lazy.spawn('code')),
        Key([mod_key], "x", lazy.screen.next_group()),
        Key([mod_key], "z", lazy.screen.prev_group()),

        Key([mod_key], "space", lazy.widget["keyboardlayout"].next_keyboard(),
            desc="Next keyboard layout."),
        Key([mod_key, "control"], "r",
            lazy.reload_config(), desc="Reload the config"),
        Key([mod_key, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
        Key([mod_key], "r", lazy.spawncmd(),
            desc="Spawn a command using a prompt widget"),
    ])

    groups = [Group(name, label=label)
              for name, label in zip('12345', ['', '', '', '', ''])]

    for i in groups:
        keys.extend(
            [
                Key(
                    [mod_key],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                ),
                Key(
                    [mod_key, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Switch to & move focused window to group {}".format(
                        i.name),
                ),
            ]
        )


# MEDIA KEYS AND PRINTSC
keys.extend(
    [Key([], 'XF86AudioMute', lazy.spawn('pamixer --toggle-mute')),
     Key([], 'XF86AudioLowerVolume', lazy.spawn('pamixer -d 5')),
     Key([], 'XF86AudioRaiseVolume', lazy.spawn('pamixer -i 5')),
     Key([], 'XF86AudioPlay', lazy.spawn('playerctl play-pause')),
     Key([], 'XF86AudioNext', lazy.spawn('playerctl next')),
     Key([], 'XF86AudioPrev', lazy.spawn('playerctl previous')),
     Key([], 'XF86AudioStop', lazy.spawn('playerctl stop')),
     Key([], 'Print', lazy.spawn('gnome-screenshot -i')),
     ]
)

# COLORS

dracula = {
    "BG":        '#282A36',
    "FG":        '#F8F8F2',
    "SELECTION": '#44475A',
    "COMMENT":   '#6272A4',
    "CYAN":      '#8BE9FD',
    "GREEN":     '#50FA7B',
    "ORANGE":    '#FFB86C',
    "PINK":      '#FF79C6',
    "PURPLE":    '#BD93F9',
    "RED":       '#FF5555',
    "YELLOW":    '#F1FA8C',
}

catppuccin = {
    "ROSEWATER": "#F5E0DC",
    "FLAMINGO": "#F2CDCD",
    "PINK": "#F5C2E7",
    "MAUVE": "#CBA6F7",
    "RED": "#F38BA8",
    "MAROON": "#EBA0AC",
    "PEACH": "#FAB387",
    "YELLOW": "#F9E2AF",
    "GREEN": "#A6E3A1",
    "TEAL": "#94E2D5",
    "SKY": "#89DCEB",
    "SAPPHIRE": "#74C7EC",
    "BLUE": "#89B4FA",
    "LAVENDER": "#B4BEFE",
    "TEXT": "#CDD6F4",
    "SUBTEXT1": "#BAC2DE",
    "SUBTEXT0": "#A6ADC8",
    "OVERLAY2": "#9399B2",
    "OVERLAY1": "#7F849C",
    "OVERLAY0": "#6C7086",
    "SURFACE2": "#585B70",
    "SURFACE1": "#45475A",
    "SURFACE0": "#313244",
    "BASE": "#1E1E2E",
    "MANTLE": "#181825",
    "CRUST": "#11111B",
}


def add_opacity_hex(hex_color: str, opacity: int):
    """Adds an opacity percentage to an hexadecimal color."""
    hex_opacity = hex(round(opacity * 2.55))[2:]

    if len(hex_opacity) == 1:
        hex_opacity = '0' + hex_opacity

    if opacity > 100 or opacity < 0:
        raise ValueError('Opacity must be between 0 and 100')

    return hex_color + hex_opacity


layouts = [
    layout.Columns(border_focus=add_opacity_hex(
        dracula["PURPLE"], 80), border_width=1),
    layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=18,
    padding=4,
)

extension_defaults = widget_defaults.copy()

line_separator = widget.TextBox('|', fontsize=20)

screens = [
    Screen(
        top=bar.Bar(
            [
                # GROUPS
                widget.GroupBox(fontsize=25, markup=False, highlight_method='text', disable_drag=True,
                                this_current_screen_border=catppuccin["TEAL"],
                                borderwidth=0, padding=14, background=add_opacity_hex(dracula["COMMENT"], 98)),
                line_separator,

                # PROMPT
                widget.Prompt(
                    prompt='❯ ', cursor_color=catppuccin["PINK"]),
                widget.Spacer(),

                widget.Systray(icon_size=20, fontsize=30),
                line_separator,

                # KEYBOARD
                widget.TextBox("", padding=12, fontsize=28, foreground=catppuccin["FLAMINGO"],
                               background=catppuccin["OVERLAY0"], ),
                widget.KeyboardLayout(configured_keyboards=['us', 'latam'], padding=2, display_map={
                                      'us': 'en ', 'latam': 'es '}, background=catppuccin["OVERLAY0"]),


                # Probably should add the others chars here, but my laptop is always connected, so...
                widget.Battery(unknown_char='', format='{char} {percent:2.0%}', padding=12,
                               foreground=catppuccin["BASE"],
                               background=catppuccin["FLAMINGO"]),
                widget.Clock(
                    background=catppuccin["LAVENDER"], foreground=dracula["BG"], padding=8
                ),
            ],
            32,
            background=add_opacity_hex(dracula["BG"], 80),
        ),
    ),
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "QTILE"
