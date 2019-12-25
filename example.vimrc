set sw=2
set aw
set expandtab
"set tw=71
"map! ` 

nnoremap -ev :edit ~/.vimrc
nnoremap -sv :source ~/.vimrc

nnoremap J ddp
nnoremap K mkyykPml'kdd`l
nnoremap -J J
nnoremap -K K
nnoremap <C-J> mjyyp`jj
nnoremap <C-K> mdkmk'ddd`k
nnoremap _ -
nnoremap -_ _

vnoremap aw lboe
vnoremap +" v`>a"`<i"`<v`>ll
vnoremap +( v`>a)`<i(`>llv`<
vnoremap +) v`>a)`<i(`<v`>ll
vnoremap -) v`>hhmvllx`<x`<v`v
vnoremap -( v`>hhmvllx`<x`<v`vo
vnoremap J :'>+m'<-'<Vo'>
vnoremap K :'<-m'>'<Vo'>o
vnoremap <C-Y> `<yl`>pmbl`<lv`b
vnoremap <C-E> '>ly`<Plv`>l

vnoremap <C-J> y'<P'<V'>

function! InsertSingle()
  let c = nr2char(getchar())
  return "i".c.""
endfunction
nnoremap <expr> \ InsertSingle()

augroup all
  autocmd!
  au BufNewFile,BufRead *.py set softtabstop=4
  au BufNewFile,BufRead *.py,*.rs set shiftwidth=4
  au BufNewFile,BufRead *.py set expandtab
  au BufNewFile,BufRead *.py set autoindent
  au BufNewFile,BufRead *.py set fileformat=unix
  au BufNewFile,BufRead *.py source ~/vim/vide/vide.vim
  au BufNewFile,BufRead *.py,*.c,*.h,*.cpp,*.rs match SpellBad /\s\+$/
augroup END

