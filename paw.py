import os
user = os.getenv("USER")

kitty_theme_path = f"/home/{user}/.config/kitty/theme.conf"
kitty_colors = {}

with open(kitty_theme_path, "r") as kitty_file:
    for line in kitty_file:
        line = line.strip()
        if line and not line.startswith("#"):
            parts = line.split()
            if len(parts) == 2:
                if "cursor" in parts[0] or "background" in parts[0] or "foreground" in parts[0]:
                    kitty_colors[parts[0]] = parts[1].replace("#", "")
                if "color" in parts[0] and not "cursor" in parts[0]:
                    num = int( parts[0].replace("color", "") )
                    if num < 8:
                        kitty_colors[f'regular{num}'] = parts[1].replace("#", "")
                    else:
                        kitty_colors[f'bright{num - 8}'] = parts[1].replace("#", "")

print(kitty_colors)

foot_ini_path = f"/home/{user}/.config/foot/foot.ini"
updated_lines = []

with open(foot_ini_path, "r") as foot_file:
    for line in foot_file:
        updated_line = line.strip()
        if ("regular" in updated_line or "bright" in updated_line) and not "#" in updated_line:
            key, value = updated_line.split("=", 1)
            key = key.strip()
            value = value.strip()
            updated_line = f"{key}={kitty_colors[key]}"
        if "color=" in updated_line and not "#" in updated_line:
            updated_line = f"color={kitty_colors['cursor_text_color']} {kitty_colors['cursor']}"
        if ("background" in updated_line or "foreground" in updated_line) and not "#" in updated_line:
            key, value = updated_line.split("=", 1)
            key = key.strip()
            updated_line =  f"{key}={kitty_colors[key]}"
        updated_lines.append(updated_line)

with open(foot_ini_path, "w") as updated_foot_file:
    for line in updated_lines:
        updated_foot_file.write(line + "\n")

print(f"foot.ini updated!")