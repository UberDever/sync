const dev = '~/dev'
const sandbox = $dev + '/sandbox'
const sync = $dev + '/sync'

def add-to-path [v: list<string>, path: string]: list<string> -> list<string> {
    ($v | split row (char esep) | append $path)
}

export-env {

    $env.config = ($env.config | upsert edit_mode vi)
    $env.config = ($env.config | upsert show_banner false)
    $env.config = ($env.config | upsert show_banner false)

    $env.PATH = (add-to-path $env.PATH ($env.HOME + '/.dotnet'))
    $env.PATH = (add-to-path $env.PATH ($env.HOME + '/.dotnet/tools'))

    for $app in (ls '~/apps' | where type == 'dir' | get name) { 
        $env.PATH = (add-to-path $env.PATH ($app + /bin))
    }

    $env.UBER = ({}
        | insert dev $dev
        | insert sandbox $sandbox
        | insert sync $sync
    )
}
