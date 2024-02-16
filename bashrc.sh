
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

export dev_dir=~/dev
sandbox_dir=$dev_dir/sandbox
sync_dir=$dev_dir/sync
gitee_sync_dir=$dev_dir/gitee_sync

cd_sync() { cd $sync_dir; }
cd_sync_gitee() { cd $gitee_sync_dir; }

. ~/dev/sync/workrc.sh
