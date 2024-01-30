use ~/dev/sync/nushell/vars.nu *

export alias vim = ~/apps/nvim/bin/nvim
export alias c = xclip
export alias v = xclip -o

def jump-locations [] { 
    [
     {value: dev, description: $dev},
     {value: arkc, description: $arkc},
     {value: core, description: $core},
     {value: frontend, description: $ets_frontend},
     {value: build, description: ($arkc + "/build")},
     {value: sandbox, description: $sandbox},
     {value: sync, description: $sync},
     {value: plugin, description: $ets_plugin},
    ]
}

export def --env tp [loc: string@jump-locations] {
    cd (jump-locations | where value == $loc | get description | get 0)
}

