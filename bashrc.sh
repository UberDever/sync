
alias vim='nvim'
alias c='xclip'
alias v='xclip -o'

to () {
    cd "$@"
    p=$(pwd -P)
    cd "${p}"
}

export PATH="$PATH:$HOME/apps/go/bin"
export PATH="$PATH:$HOME/apps/nvim/bin"
export PATH="$PATH:$HOME/apps/ziglang/bin"

. ~/dev/sync/workrc.sh
