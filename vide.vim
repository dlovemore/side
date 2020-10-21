function! PythonPrompt()
  if match(getline('.'), "[ #]*\\(>>>\\|\\.\\.\\.\\) ") == 0
    let x = match(getline('.'), "\\(>>>\\|\\.\\.\\.\\) ")
    if x == -1
      return ''
    elseif x == 0
      let p = ''
    else
      let p = getline('.')[:x-1]
    endif
  else
    return ''
  endif
  let l = line('.')
  let q = p.">>> "
  while 1
    let l=l+1
    if l>line('$') || match(getline(l),p)!=0 || match(getline(l),q)==0
      break
    endif
  endwhile
  call cursor(l-1,len(q))
  return q
endfunction

function! AW()
    if &aw
      return ":w"
    end
    return ""
endfunction

function! PythonIReturn()
  let p = PythonPrompt()
  if p != ''
    if line('.') == line('$')
      return "".AW().":1,$!sideGo0".p
    endif
    return "".AW().(line('.')+1)."Gmp:1,-!side'pO0".p
  elseif match(getline('.'), "^  *$") == 0
    return ""
  else
    let block = (getline('.') =~ "^ *\\(if \\|def \\|elif \\|else\\|for \\|while \\|try\\|class \\|with \\)")
    let colon = (getline('.') =~ ":")
    let endcolon = getline('.')[getcurpos()[2]-2]==':'
    if block && colon
      if &ai
        if endcolon
            return ""
        endif
      endif
      return ""
    endif
    if block && !colon
      if &ai
        return ":"
      else
        return ":"
      endif
    endif
    return ""
  endif
endfunction
inoremap <expr>  PythonIReturn()

function! PythonR()
    let ch = getchar()
    let ch = nr2char(ch)
    let colon = getline('.')[getcurpos()[2]-2]==':'
    if ch==""
        if colon
            if &ai
                return "s"
            endif
        endif
    endif
    return "r" . ch
endfunction
nnoremap <expr> r PythonR()



function! CurChar()
endfunction

function! PythonNReturn()
  let p = PythonPrompt()
  if p != ''
    if line('.') == line('$')
      return AW().":%!sideG$"
    endif
    return AW().(line('.')+1)."Gmp:1,-!side'p$"
  else
    return ""
  endif
endfunction

function! PythonO()
  let p = PythonPrompt()
  if p != ''
    return 'O0'.p
  else
    return 'O'
  endif
endfunction

function! PythonI()
  let l=line('.')
  let p = PythonPrompt()
  if p != ''
    if len(p) >= len(getline(l))
      return 'A'
    else
      return ''.(len(p)+1).'|i'
    endif
  else
    return 'I'
  endif
endfunction

function! PythonS()
  let p = PythonPrompt()
  if p != ''
    return 'S0'.p
  else
    return 'S'
  endif
endfunction

function! PythonIndent()
  if &ai && getline('.')[len(getline('.'))-1] == ':'
    return ''
  endif
  return ''
endfunction

function! Pythono()
  let p = PythonPrompt()
  if p != ''
    return 'o0'.p
  else
    return 'o'.PythonIndent()
  endif
endfunction

function! PythonThisPrompt()
  let p = PythonPrompt()
  if p != ''
    return '0'.PythonNextPrompt()
  else
    return '0'
  endif
endfunction

function IPythonThisPrompt()
  return '0'.PythonNextPrompt()
endfunction

function! PythonPrevPrompt()
  return '?>>> .\{0,1}?e'
endfunction

function! PythonNextPrompt()
  return '/>>> .\?/e'
endfunction

nnoremap <expr>  PythonNReturn()
nnoremap <expr> O PythonO()
nnoremap <expr> o Pythono()
nnoremap <expr> I PythonI()
nnoremap <expr> S PythonS()
nnoremap <expr> [[ PythonPrevPrompt()
nnoremap <expr> ]] PythonNextPrompt()
inoremap <expr>  IPythonThisPrompt()
noremap <expr> - PythonThisPrompt()

nnoremap -g :normal! AW():%!side
vnoremap -g :!side
nnoremap -s jmsk:.!side's
