-- Copyright 2006-2015 Mitchell mitchell.att.foicica.com.
-- Copyright 2015 Immunio, Inc.

-- Shell LPeg lexer.

-- This is based on the lexer from the Scintillua package, with a ot of extension
-- The goal isn't a complete parser for bash, but a lexer that can extract a useful
-- amount of structure to detect tampering. The emphasis is more on common injection
-- techniques and lexical structure than actually extracting properly formed bash
-- statements. Down the road we may need to go as far as to parse statements, and that
-- should be possible at the cost of a lot more complexity.

local l = require('lexer')
local token = l.token
local P, R, S = lpeg.P, lpeg.R, lpeg.S

local M = {_NAME = 'bash'}

-- Whitespace.
local ws = token(l.WHITESPACE, l.space^1)

local bash_word = (l.alpha + '_') * (l.alnum + '_' + '\\ ')^0


-- Comments.
local comment = token(l.COMMENT, '#' * l.nonnewline^0)

-- Strings.
local sq_str = token('sq_str', l.delimited_range("'", false, true))
local dq_str = token('dq_str', l.delimited_range('"'))
local ex_str = token('ex_str', l.delimited_range('`'))
local heredoc = token('heredoc', '<<' * P(function(input, index)
  local s, e, _, delimiter =
    input:find('%-?(["\']?)([%a_][%w_]*)%1[\n\r\f;]+', index)
  if s == index and delimiter then
    local _, e = input:find('[\n\r\f]+'..delimiter, e)
    return e and e + 1 or #input + 1
  end
end))
local bash_string = sq_str + dq_str + ex_str + heredoc

-- Numbers.
local number = token(l.NUMBER, l.float + l.integer)

-- Keywords.
local keyword = token(l.KEYWORD, l.word_match({
  'if', 'then', 'elif', 'else', 'fi', 'case', 'in', 'esac', 'while', 'for',
  'do', 'done', 'continue', 'local', 'return', 'select',
-- Operators. These could be split into individual tokens...
  '-a', '-b', '-c', '-d', '-e', '-f', '-g', '-h', '-k', '-p', '-r', '-s', '-t',
  '-u', '-w', '-x', '-O', '-G', '-L', '-S', '-N', '-nt', '-ot', '-ef', '-o',
  '-z', '-n', '-eq', '-ne', '-lt', '-le', '-gt', '-ge'
}, '-'))

-- Common commands ... this is not exhaustive nor does it need to be.
local command = token("command", l.word_match({
  'awk', 'cat', 'cmp', 'cp', 'curl', 'cut', 'date', 'find', 'grep', 'gunzip', 'gvim',
  'gzip', 'kill', 'lua', 'make', 'mkdir', 'mv', 'php', 'pkill', 'python', 'rm',
  'rmdir', 'rsync', 'ruby', 'scp', 'sed', 'sleep', 'ssh', 'sudo', 'tar', 'unlink',
  'wget', 'zip'
}, '-'))

-- Builtins
local builtin = token("builtin", l.word_match({
  'alias', 'bind', 'builtin', 'caller', 'command', 'declare', 'echo', 'enable',
  'help', 'let', 'local', 'logout', 'mapfile', 'printf', 'read', 'readarray',
  'source', 'type', 'typeset', 'ulimit', 'unalias',
}, '-'))

-- Filenames. This is a bit sloppy, but tries to discern filenames from other identifiers
-- Very much a case of R&D 'suck it and see'
local filename = token("filename", P('/')^0 * (bash_word + '.') * (
                                    '/' + bash_word + '.' )^0 * ('.' * bash_word )^0 )

-- Identifiers.
local identifier = token(l.IDENTIFIER, bash_word)

-- Variables.
local ex_variable = token("ex_variable",
                          '$' * l.delimited_range('()', true, true))

local variable = token(l.VARIABLE,
                       '$' * (S('!#?*@$') + l.digit^1 + bash_word +
                              l.delimited_range('{}', true, true)))

local var = ex_variable + variable

-- Operators. These could be split into individual tokens...
local operator = token(l.OPERATOR, S('=!<>+-/*^&|~.,:;?()[]{}'))

M._rules = {
  {'whitespace', ws},
  {'keyword', keyword},
  {'builtin', builtin},
  {'command', command},
  {'identifier', identifier},
  {'filename', filename},
  {'string', bash_string},
  {'comment', comment},
  {'number', number},
  {'variable', var},
  {'operator', operator},
}

-- This is the main function for lexing bash data. It recurses and uses
-- the dqstr sub-lexer instance provided (we don't instantiate it directly
-- to allow the caller to cache the instance and avoid recompiling the grammar)
function M.lex_recursive( self, str, bash_dqstr_lexer )
  local tokens = self:lex(str)
  for i = 1, #tokens do
    if tokens[i]['token'] == "ex_str" then
      tokens[i]['val'] = self:lex_recursive(string.sub(tokens[i]['val'], 2, -2), bash_dqstr_lexer)
    elseif tokens[i]['token'] == "ex_variable" then
      tokens[i]['val'] = self:lex_recursive(string.sub(tokens[i]['val'], 3, -2), bash_dqstr_lexer)
    elseif tokens[i]['token'] == "dq_str" then
      tokens[i]['val'] =
        bash_dqstr_lexer:lex_recursive(string.sub(tokens[i]['val'], 2, -2), self)
    elseif tokens[i]['token'] == "heredoc" then
      tokens[i]['val'] =
        bash_dqstr_lexer:lex_recursive(tokens[i]['val'], self)
    end
  end
  return tokens
end

return M


