use ~/dev/sync/nushell/vars.nu *

export alias vim = ~/apps/nvim/bin/nvim
export alias c = xclip
export alias v = xclip -o

def jump-locations [] { 
    [
     {value: $dev, description: "dev"},
     {value: $arkc, description: "arkcompiler"},
     {value: $core, description: "runtime core"},
     {value: $ets_frontend, description: "ets frontend"},
     {value: $sandbox, description: "sandbox"},
     {value: $sync, description: "sync"},
     {value: $ets_plugin, description: "ets plugin"},
    ]
}

export def --env jump [loc: string@jump-locations] {
    cd $loc
}

