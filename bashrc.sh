
alias vim='nvim'
alias c='xclip'
alias v='xclip -o'
alias st='st &>/dev/null &'

to () {
    cd "$@"
    p=$(pwd -P)
    cd "${p}"
}

# Go in local path
export PATH="$PATH:/usr/local/go/bin"
# Dotnet
export DOTNET_ROOT="$HOME/.dotnet"
export PATH="$PATH:$HOME/.dotnet"
export PATH="$PATH:$HOME/.dotnet/tools"

# Add all apps to PATH
for d in $HOME/apps/*/; do
    export PATH="$PATH:$d"/bin
done

export panda_branch="origin"
export ecma_branch="origin"
export es2_branch="origin"

. ~/dev/sync/workrc.sh
