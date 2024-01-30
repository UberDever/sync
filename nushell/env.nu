use ~/dev/sync/nushell/vars.nu *

def add-to-list [v: list<string>, path: string]: list<string> -> list<string> {
    ($v | split row (char esep) | append $path)
}

export-env {
    # config
    $env.config = ($env.config | upsert edit_mode vi)
    $env.config = ($env.config | upsert show_banner false)

    # PATH
    $env.PATH = (add-to-list $env.PATH ($env.HOME + '/.dotnet'))
    $env.PATH = (add-to-list $env.PATH ($env.HOME + '/.dotnet/tools'))
    for $app in (ls '~/apps' | where type == 'dir' | get name) { 
        $env.PATH = (add-to-list $env.PATH ($app + /bin))
    }

    # env vars
    $env.EDITOR = (scope aliases | where name == 'vim' | get expansion)
    $env.UBER = ({}
        | insert dev $dev
        | insert sandbox $sandbox
        | insert sync $sync
    )
}
