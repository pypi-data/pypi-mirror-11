-- Copyright (C) 2015 Immunio, Inc.

-- Lexer for HTML markers used in Immunio.io XSS

-- NOTE: not covered by Scintillua MIT license in this directory.

local l = require('lexer')
local token, parent_token, word_match = l.token, l.parent_token, l.word_match
local P, R, S, V = lpeg.P, lpeg.R, lpeg.S, lpeg.V

local M = {_NAME = 'markers'}

local start_marker = l.token('start_marker', P('{immunio-var:') * l.integer * ':' * l.xdigit^1 * '}')
local end_marker = l.token('end_marker', P('{/immunio-var:') * l.integer * ':' * l.xdigit^1 * '}')
local marker = start_marker + end_marker

-- Data between markers
local data = token('data', (l.any - ( marker ) )^1 )
local substitution = l.parent_token( 'substitution', start_marker * data^0 * end_marker )

M._rules = {
  {'substitution', substitution},
  {'marker', marker},
  {'data', data},
}

M._tokenstyles = {
}

M._foldsymbols = {
}

return M
