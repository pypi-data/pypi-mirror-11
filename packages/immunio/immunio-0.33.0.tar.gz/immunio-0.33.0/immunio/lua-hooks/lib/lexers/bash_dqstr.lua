-- Copyright (C) 2015 Immunio, Inc.

-- Lexer for bash magic double quotes

-- NOTE: not covered by Scintillua MIT license in this directory.

-- While our lexer has the ability to embed this sort of thing as a child of another lexer
-- I didn't bother here due to the recursion; we need to lex the parent (bash) language
-- for some tokens which would be very complex at best. It's cleaner to use two lexers
-- and handle the recursion in higher level lua at a minute performance cost.

local l = require('lexer')
local token, word_match = l.token, bash_word_match
local P, R, S = lpeg.P, lpeg.R, lpeg.S

local M = {_NAME = 'bash_dqstr'}

-- Whitespace.
local ws = token(l.WHITESPACE, l.space^1)

-- Generic token.
local bash_word = (l.alpha + '_') * (l.alnum + '_' + '\\ ')^0

-- Strings.
--  Shell substitution.
local ex_str = token('ex_str', l.delimited_range('`'))

--  Other string data
local bash_string = token('str_data', (l.any - '$' - '`')^1)

-- Variables.
--  Shell Substitution.
local ex_variable = token("ex_variable",
                          '$' * l.delimited_range('()', true, true))
--  Other variables
local variable = token(l.VARIABLE,
                       '$' * (S('!#?*@$') + l.digit^1 + bash_word +
                              l.delimited_range('{}', true, true)))

local var = ex_variable + variable

M._rules = {
  {'variable', var},
  {'ex_str', ex_str},
  {'string', bash_string},
}

function M.lex_recursive( self, str, bash_lexer )
  local tokens = self:lex(str)
  for i = 1, #tokens do
    if tokens[i]['token'] == "ex_str" then
      tokens[i]['val'] = bash_lexer:lex_recursive(string.sub(tokens[i]['val'], 2, -2), self)
    elseif tokens[i]['token'] == "ex_variable" then
      tokens[i]['val'] = bash_lexer:lex_recursive(string.sub(tokens[i]['val'], 3, -2), self)
    end
  end
  return tokens
end

return M


