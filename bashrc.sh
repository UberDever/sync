
alias vim='nvim'
# alias c='xclip'
# alias v='xclip -o'
alias st='st &>/dev/null &'

to () {
    cd "$@"
    p=$(pwd -P)
    cd "${p}"
}

# Go in local path
# export PATH="$PATH:/usr/local/go/bin"
# Dotnet
# export DOTNET_ROOT="$HOME/.dotnet"
# export PATH="$PATH:$HOME/.dotnet"
# export PATH="$PATH:$HOME/.dotnet/tools"

# Add all apps to PATH
# for d in $HOME/apps/*/; do
#     export PATH="$PATH:$d"/bin
# done

export dev_dir=~/dev
sandbox_dir=$dev_dir/sandbox
sync_dir=$dev_dir/sync

cd_sync() { cd $sync_dir; }

export PS1='\[\e[32m\]\w\[\e[33m\]$(__git_ps1)\[\e[00m\]$ '

. "$sync_dir/z.sh"
