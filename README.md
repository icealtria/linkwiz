# Linkwiz

A tool that lets users select their preferred browser for opening links.

![Screenshot](https://raw.githubusercontent.com/icealtria/linkwiz/assets/win.avif)

## Installation
### Arch
```
paru -S linkwiz
```

Set linkwiz as default browser

## Configuration

You can configure LinkWiz by modifying the `linkwiz.toml` file, which is created in the `~/.config/linkwiz/linkwiz.toml` on the first run. You can add rules to specify which browser to use for specific domains.

Example `linkwiz.toml`:
```toml
[browsers] # Custom Browsers
"Firefox Private" = ["/usr/bin/firefox-developer-edition", "--private-window"]
"Brave Private" = ["/usr/bin/brave", "--incognito"]
# Windows
"Firefox Private" = ['C:\Program Files\Firefox Developer Edition\private_browsing.exe']
"Brave Private" = ['C:\Users\<user>\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe', '--incognito']

[rules.fnmatch]
"*.cn" = "Brave Private"
"*.google.com" = "Google Chrome" # This will not match "google.com"

[rules.hostname]
"example.com" = "Brave Private"
"github.com" = "Firefox Developer Edition"
"google.com" = "Google Chrome"
```
## TODO
- [x] Windows Support
- [x] RIIR
