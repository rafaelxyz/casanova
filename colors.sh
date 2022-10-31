
red() {
  printf %b '\e[41m' '\e[8]' '\e[H\e[J'
}

green() {
  printf %b '\e[42m' '\e[8]' '\e[H\e[J'
}

black() {
  printf %b '\e[40m' '\e[8]' '\e[H\e[J'
}

clear
"$@"
