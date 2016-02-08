# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
setopt autocd nomatch notify
unsetopt beep extendedglob
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/dark/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

PS1=$'%{\e[1;34m%}%n %{\e[0m%}at %{\e[0;33m%}%M %{\e[0m%}in %{\e[1;32m%}%~ 
%{\e[1;30m%}>>> %{\e[0m%}'

