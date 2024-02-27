# LinkWiz

LinkWiz is a Linux tool that lets users select their preferred browser for opening links.

## Configuration

You can configure LinkWiz by modifying the `linkwiz.toml` file, which is created in the `~/.config/linkwiz.toml` on the first run. You can add rules to specify which browser to use for specific domains.

Example `linkwiz.toml`:
```toml
[browsers] # Custom Browsers
"Firefox Private" = "/usr/bin/firefox-developer-edition --private-window"
"Brave Private" = "/usr/bin/brave --incognito"

[rules]
[rules.regex]

[rules.hostname]
"example.com" = "Brave Private"
"github.com" = "Firefox Developer Edition"
"*.google.com" = "Google Chrome"
```
