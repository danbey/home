# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias grep='grep --color=auto'
alias sgrep='grep -rIn --color=auto --include=\*.{c,cpp,h} --exclude-dir="*\.{svn,git}" --exclude="*\tags"'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi


shopt -s histappend
PROMPT_COMMAND='history -a'

export HISTTIMEFORMAT='%Y-%m-%d %H:%M:%S '

shopt -s cdspell

__git_ps1 () 
{ 
    local b="$(git symbolic-ref HEAD 2>/dev/null)";
    if [ -n "$b" ]; then
        printf " (%s)" "${b##refs/heads/}";
    fi
}
PS1='\[\e]0;\w\a\]\[\e[1;32m\]\u@\H \[\e[1;33m\]\w \[\e[1;36m\]$(__git_ps1 "(%s) ")\[\e[1;0m\]\$ '

source ~/bin/git-completion.sh
source ~/bin/git-flow-completion.sh


export IBSIM_SERVER_NAME=localhost
export IBSIM_SERVER_PORT=55555
export OSM_CACHE_DIR=/tmp/sasha/opensm 
export IBUTILS_PATH=/.autodirect/mtrswgwork/sashakot/src/simulator/dist/
export LD_LIBRARY_PATH=/.autodirect/mtrswgwork/sashakot/src/simulator/dist/lib

