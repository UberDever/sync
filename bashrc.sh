
alias vim='nvim'
alias c='xclip'
alias v='xclip -o'

to () {
    cd "$@"
    p=$(pwd -P)
    cd "${p}"
}

export PATH="$PATH:/usr/local/go/bin"
export PATH="$PATH:$HOME/apps/go/bin"
export PATH="$PATH:$HOME/apps/nvim/bin"
export PATH="$PATH:$HOME/apps/ziglang/bin"

export panda_branch="origin"
export ecma_branch="origin"
export es2_branch="origin"

. ~/dev/sync/workrc.sh
