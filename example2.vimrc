set sw=2
set aw
set expandtab
set laststatus=2
set statusline=%f\ %m\ %{mode(1)}\ %{wordcount()['cursor_bytes']+1-line('.')}%=\ %l:%c\ %p%%/%L
"set statusline=%f\ %m\ %{mode(1)}\ %{wordcount()['cursor_bytes']+1-line('.')}\ %{''+(100*(line('.')-1)+col('.'))}%=\ %l:%c\ %p%%/%L
"set tw=71
"map! ` 

nnoremap -ev :edit ~/.vimrc
nnoremap -sv :w:source ~/.vimrc
nnoremap -ss :w:source ~/python/side/vide.vim

nnoremap J ddp
nnoremap K mkyykPml'kdd`l
nnoremap -J J
nnoremap -K K
nnoremap <C-J> yypV
nnoremap <C-K> yyPV
nnoremap _ -
nnoremap -_ _
nnoremap -( mb%x`bx
nnoremap -) mb%x`bhx

vnoremap v 
vnoremap V 
vnoremap <C-v> 
vnoremap aw lboe
vnoremap ++ v`<hv`>l
vnoremap -- v`<lv`>h
vnoremap +" v`>a"`<i"`<v`>ll
vnoremap +' v`>a'`<i'`<v`>ll
vnoremap +( v`>a)`<i(`>llv`<
vnoremap +) v`>a)`<i(`<v`>ll
vnoremap -) v`>hhmvllx`<x`<v`v
vnoremap -( v`>hhmvllx`<x`<v`vo
vnoremap +{ v`>a}`<i{`>llv`<
vnoremap +} v`>a}`<i{`<v`>ll
vnoremap -} v`>hhmvllx`<x`<v`v
vnoremap -{ v`>hhmvllx`<x`<v`vo
vnoremap J :'>+m'<-'<Vo'>
vnoremap K :'<-m'>'<Vo'>o
vnoremap <C-Y> `<yl`>pmbl`<lv`b
vnoremap <C-E> '>ly`<Plv`>l

vnoremap <C-J> y'<P'<V'>

function! Mode()
  echo 'cc'
endfunction
vnoremap <expr> -z Mode()

function! InsertSingle()
  let c = nr2char(getchar())
  return "i".c.""
endfunction
nnoremap <expr> \ InsertSingle()

function! GoFileAndLine()
  let n=matchlist(getline('.'),'[: ]\([1-9][0-9]*\)')
  let n=len(n)?'gf'.n[1].'G':''
  return n
endfunction
nnoremap <expr> gx GoFileAndLine()

function! VUpLine()
  let m=mode()
  if m=='v'
    let @p=matchstr(getline('.'),'\m^\([#> \t]*\)')
    return 'yO0p_="F_V'
  elseif m=='V'
    let m=matchlist(getline('.'),'\m^\([#> \t]*\(let\)\?\) *\(\i\+\) *= *\(.*\)')
    let @a=string(m)
    if len(m)
      return ":'<-m'>'>j:s/\\V".escape(m[4],'\')."/".m[3]."/eg'<Vo'>"
    endif
  endif
  return ":'<-m'>'<Vo'>"
endfunction
vnoremap <expr> K VUpLine()
vnoremap <expr> <C-K> VUpLine()

function! VDownLine()
  let m=matchlist(getline('.'),'\m^\([#> \t]*\(let\)\?\) *\(\i\+\) *= *\(.*\)')
  if len(m)
    return ":'>+m'<-:s/\\V\\<".m[3]."\\>/".m[4]."/eg'<Vo'>"
  else
    return ":'>+m'<-'<Vo'>"
  endif
endfunction
vnoremap <expr> J VDownLine()
vnoremap <expr> <C-J> VDownLine()
vnoremap <expr> s mode()."s"

augroup all
  autocmd!
  au BufNewFile,BufRead *.py set softtabstop=4
  au BufNewFile,BufRead *.py,*.rs set shiftwidth=4
  au BufNewFile,BufRead *.py set expandtab
  au BufNewFile,BufRead *.py set autoindent
  au BufNewFile,BufRead *.py set fileformat=unix
  au BufNewFile,BufRead *.py source ~/python/side/vide.vim
  au BufNewFile,BufRead *.py,*.c,*.h,*.cpp,*.rs match SpellBad /\s\+$/
augroup END

digraph .a 775
source ~/vim/hebrew/hebrew.vim
