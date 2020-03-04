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
    let colon = getline('.')[getcurpos()[2]-2]==':'
    if block && colon
      if &ai
        return ""
      else
        return ""
      endif
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
  let l=line('.')
  let p = PythonPrompt()
  if p != ''
    return 'S'.p
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

function! PythonPrevPrompt()
  return '?>>> nell'
endfunction

function! PythonNextPrompt()
  return '/>>> ell'
endfunction

nnoremap <expr>  PythonNReturn()
nnoremap <expr> O PythonO()
nnoremap <expr> o Pythono()
nnoremap <expr> I PythonI()
nnoremap <expr> S PythonS()
nnoremap <expr> [[ PythonPrevPrompt()
nnoremap <expr> ]] PythonNextPrompt()

nnoremap -g :normal! AW():%!side
vnoremap -g :!side
nnoremap -s jmsk:.!side's
