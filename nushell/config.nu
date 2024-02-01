use ~/dev/sync/nushell/vars.nu *

def add-to-list [v: list<string>, path: string]: list<string> -> list<string> {
    ($v | split row (char esep) | append $path)
}

# update (find-index $env.config.keybindings { where item.name == "cut_line_from_start" }) {
def find-index [v: list, pred: closure]: list -> int {
    $v | enumerate | do $pred | get index | if ($in | is-empty) { (-1) } else { $in | get 0 }
}

export-env {
    # config
    $env.config = ($env.config | upsert show_banner false)
    $env.config.keybindings = ($env.config.keybindings |
    append {
        name: cut_line_from_start
        modifier: control
        keycode: char_u
        mode: [emacs, vi_insert]
        event: {edit: cutfromstart}
    })

    # PATH
    $env.PATH = (add-to-list $env.PATH ($env.HOME + '/.dotnet'))
    $env.PATH = (add-to-list $env.PATH ($env.HOME + '/.dotnet/tools'))
    for $app in (ls '~/apps' | where type == 'dir' | get name) { 
        $env.PATH = (add-to-list $env.PATH ($app + /bin))
    }

    # env vars
    $env.EDITOR = (scope aliases | where name == 'vim' | get expansion)
}
