call plug#begin('~/.local/share/nvim/plugged')
" looking
  Plug 'vim-airline/vim-airline'
  Plug 'vim-airline/vim-airline-themes'
  Plug 'airblade/vim-gitgutter'
  Plug 'Yggdroot/indentLine'
  Plug 'scrooloose/syntastic'
  Plug 'myusuf3/numbers.vim'
" navigation
  Plug 'scrooloose/nerdtree'
  Plug 'ctrlpvim/ctrlp.vim'
  Plug 'wesleyche/SrcExpl'
  Plug 'majutsushi/tagbar'
  Plug 'vim-scripts/taglist.vim'
  Plug 'rizzatti/dash.vim'
" completion/coding
  Plug 'Valloric/YouCompleteMe'
  Plug 'jiangmiao/auto-pairs' "自动括号匹配
  Plug 'scrooloose/nerdcommenter'
  Plug 'tpope/vim-surround'
  Plug 'junegunn/vim-easy-align'
" php 
"  Plug 'arnaud-lb/vim-php-namespace'
"  Plug '2072/PHP-Indenting-for-VIm'
"  Plug 'shawncplus/phpcomplete.vim'
"  Plug 'm2mdas/phpcomplete-extended-laravel'
"  Plug 'StanAngeloff/php.vim'
call plug#end()

" Fundamental settings
  let mapleader = ','
  let g:mapleader = ','
  set fileencoding=utf-8
  set fileencodings=ucs-bom,utf-8,gbk,gb18030,big5,cp936,latin-1
  set fileformat=unix
  set fileformats=unix,dos,mac
  set number
  filetype on
  filetype plugin on
  filetype plugin indent on
  syntax on
" Some useful settings
  set smartindent
  set expandtab         "tab to spaces
  set tabstop=4         "the width of a tab
  set shiftwidth=4      "the width for indent
  set foldenable
  hi Folded ctermbg=242

  set foldmethod=indent "folding by indent
  set ignorecase        "ignore the case when search texts
  set smartcase         "if searching text contains uppercase case will not be ignored
  if has("autocmd")
    au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$")
      \| exe "normal! g'\"" | endif
  endif
  " vimrc文件修改之后自动加载, linux
  autocmd! bufwritepost .vimrc source %
  
  " 自动补全配置
  " 让Vim的补全菜单行为与一般IDE一致(参考VimTip1228)
  set completeopt=longest,menu
  
  " 增强模式中的命令行自动完成操作
  set wildmenu
  " Ignore compiled files
  set wildignore=*.o,*~,*.pyc,*.class
  " 具体编辑文件类型的一般设置，比如不要 tab 等
  autocmd FileType python set tabstop=4 shiftwidth=4 expandtab ai
  autocmd FileType ruby,javascript,html,css,xml set tabstop=2 shiftwidth=2 softtabstop=2 expandtab ai
  autocmd BufRead,BufNewFile *.md,*.mkd,*.markdown set filetype=markdown.mkd
  autocmd BufRead,BufNewFile *.part set filetype=html
  " disable showmatch when use > in php
  au BufWinEnter *.php set mps-=<:>
  
  " 保存python文件时删除多余空格
  fun! <SID>StripTrailingWhitespaces()
      let l = line(".")
      let c = col(".")
      %s/\s\+$//e
      call cursor(l, c)
  endfun
  autocmd FileType c,cpp,java,go,php,javascript,puppet,python,rust,twig,xml,yml,perl autocmd BufWritePre <buffer> :call <SID>StripTrailingWhitespaces()
  
  
  " 定义函数AutoSetFileHead，自动插入文件头
  autocmd BufNewFile *.sh,*.py exec ":call AutoSetFileHead()"
  function! AutoSetFileHead()
      "如果文件类型为.sh文件
      if &filetype == 'sh'
          call setline(1, "\#!/bin/bash")
      endif
  
      "如果文件类型为python
      if &filetype == 'python'
          call setline(1, "\#!/usr/bin/env python")
          call append(1, "\# @Author: zhoubo(congminghaoxue@gmail.com)")
          call append(1, "\# encoding: utf-8")
      endif
  
      normal G
      normal o
      normal o
  endfunc
  
  
  " 设置可以高亮的关键字
  if has("autocmd")
    " Highlight TODO, FIXME, NOTE, etc.
    if v:version > 701
      autocmd Syntax * call matchadd('Todo',  '\W\zs\(TODO\|FIXME\|CHANGED\|DONE\|XXX\|BUG\|HACK\)')
      autocmd Syntax * call matchadd('Debug', '\W\zs\(NOTE\|INFO\|IDEA\|NOTICE\)')
    endif
  endif
" Lookings
  set title
  set t_ti= t_te=
  set cursorline       "hilight the line that the cursor exists in
  set cursorcolumn     "hilight the column that the cursor exists in
"   hi CursorLine   cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
"   hi CursorColumn cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
  set nowrap           "no line wrapping
  let $NVIM_TUI_ENABLE_TRUE_COLOR=1
  set scrolloff=7      " 在上下移动光标时，光标的上方或下方至少会保留显示的行数


" Shortcuts
  " <space> => fold/unfold current text tips: zR => unfold all; zM => fold all
  nnoremap <space> @=((foldclosed(line('.')) < 0) ? 'zc' : 'zo')<CR>
  " ,, => escape to normal mode
  imap ,, <Esc>
  " <esc> => go back to normal mode (in terminal mode)
  " tnoremap <Esc> <C-\><C-n> 
  " use t{h,j,k,l} to switch between different windows
  map <C-j> <C-W>j
  map <C-k> <C-W>k
  map <C-h> <C-W>h
  map <C-l> <C-W>l
  " <F4> => popup the file tree navigation)
  nmap <leader>n :NERDTreeToggle<CR>
  " t[number] => switch to the file showed in the top tabs
  " t[ t] => prev tab/next tab
    nmap t1 <Plug>AirlineSelectTab1
    nmap t2 <Plug>AirlineSelectTab2
    nmap t3 <Plug>AirlineSelectTab3
    nmap t4 <Plug>AirlineSelectTab4
    nmap t5 <Plug>AirlineSelectTab5
    nmap t6 <Plug>AirlineSelectTab6
    nmap t7 <Plug>AirlineSelectTab7
    nmap t8 <Plug>AirlineSelectTab8
    nmap t9 <Plug>AirlineSelectTab9
    nmap t[ <Plug>AirlineSelectPrevTab
    nmap t] <Plug>AirlineSelectNextTab
  " <F8> => toggle the srcExpl (for source code exploring)
    nmap <F8> :SrcExplToggle<CR>
  " tb => open the tagbar
    nmap tb :TlistClose<CR>:TagbarToggle<CR>
  " ti => taglist
    nmap ti :TagbarClose<CR>:Tlist<CR>
  " \jd => GoTo the definition
    nnoremap <leader>jd :YcmCompleter GoTo<CR>
  " Neoterm


" Plugin settings
  " EasyAlign
    xmap ga <Plug>(EasyAlign)
    nmap ga <Plug>(EasyAlign)
  " IdentLine
    let g:indentLine_color_term = 239
  " markdown_preview (a plugin in nyaovim)
    let g:markdown_preview_eager=1
  " airline
    let g:airline#extensions#tabline#enabled = 1
    if !exists('g:airline_symbols')
      let g:airline_symbols = {}
    endif
    let g:airline_left_sep = ''
    let g:airline_left_alt_sep = ''
    let g:airline_right_sep = ''
    let g:airline_right_alt_sep = ''
    let g:airline_symbols.branch = ''
    let g:airline_symbols.readonly = ''
    let g:airline_symbols.linenr = ''
    let g:airline_symbols.crypt = '🔒'
    let g:airline_symbols.paste = 'ρ'
    let g:airline_symbols.notexists = '∄'
    let g:airline_symbols.whitespace = 'Ξ'
    let g:airline#extensions#tabline#buffer_idx_mode = 1
  " Neoterm
    let g:neoterm_size=5
    let g:neoterm_position = 'horizontal'
    let g:neoterm_automap_keys = ',tt'
    " toogle the terminal
    nnoremap <silent> <s-cr> :Ttoggle<cr>
    " kills the current job (send a <c-c>)
    nnoremap <silent> tc :call neoterm#kill()<cr>
    command! -nargs=+ Tg :T git <args>   let g:neoterm_
  " Syntastics
    let g:syntastic_cpp_compiler = "g++"
    let g:syntastic_cpp_compiler_options = ' -std=c++11'
  " Tagbar
    let g:tagbar_width=30
  " Taglist
    let Tlist_Show_One_File=1
    let Tlist_Exit_OnlyWindow=1
    let Tlist_File_Fold_Auto_Close=1
    let Tlist_WinWidth=30
    let Tlist_Use_Right_Window=1
    let g:Tlist_Ctags_Cmd='/usr/local/bin/ctags'
  " YouCompleteMe
    let g:ycm_confirm_extra_conf=0
    let g:ycm_python_binary_path = '/usr/local/bin/python'
    let g:ycm_server_python_interpreter = '/usr/local/bin/python'
    let g:ycm_autoclose_preview_window_after_completion=1
    let g:ycm_filetype_blacklist = {
      \ 'tagbar' : 1,
      \ 'qf' : 1,
      \ 'notes' : 1,
      \ 'unite' : 1,
      \ 'vimwiki' : 1,
      \ 'pandoc' : 1,
      \ 'infolog' : 1,
      \ 'mail' : 1
    \}

" for php 
" Put at the very end of your .vimrc file.
"
"function! PhpSyntaxOverride()
"  hi! def link phpDocTags  phpDefine
"  hi! def link phpDocParam phpType
"endfunction
"
"augroup phpSyntaxOverride
"  autocmd!
"  autocmd FileType php call PhpSyntaxOverride()
"augroup END
