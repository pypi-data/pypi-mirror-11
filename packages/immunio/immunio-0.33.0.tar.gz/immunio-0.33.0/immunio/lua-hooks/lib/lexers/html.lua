-- Copyright (C) 2015 Immunio, Inc.

-- HTML: Simple h5 like HTML lexer for Immun.io.

-- NOTE: not covered by Scintillua MIT license in this directory.

local l = require('lexer')
local token, parent_token, word_match = l.token, l.parent_token, l.word_match
local P, R, S, V = lpeg.P, lpeg.R, lpeg.S, lpeg.V

local M = {_NAME = 'html'}

local case_insensitive_tags = true

-- Whitespace.
local ws = l.space^1
-- This is broad to both accept our placeholders and be very liberal about what may be
-- interpreted as an attribute to ensure we escape attributes fairly aggressively.
local element_chars = (l.any - '<' - '>' - '=' - '"' - "'" - ws)^1
-- Comments.
local comment = token(l.COMMENT, '<!--' * (l.any - '-->')^0 * P('-->')^-1)
-- XXX add h5 bogus comment 1 and bogus comment 2?

-- Strings.
local sq_str = l.delimited_range("'")
local dq_str = l.delimited_range('"')
local string = sq_str + dq_str

-- Attributes. Individual recognition is handled in our XSS processing code.
local attr_name = token('attr_name', element_chars - '=')
local attr_value = token('attr_value', string + element_chars)
local attribute = parent_token('attribute', attr_name * '=' * attr_value)

-- Tags.
local tag_name = token('tag_name', element_chars - '/')
local tag_data = token('tag_data', (l.any - '>')^1 ) -- crap in a tag

-- XXX how should we handle void tags... right now they are an unmatched tag_open
local tag_open = parent_token('tag_open', P('<') * tag_name * ((ws * attribute) + tag_data)^0 * (P('>') + '/>') )
local tag_close = parent_token('tag_close', P('</') * tag_name * tag_data^0 * '>')

-- Special case for script and style tags.
local style_tag_name = token("tag_name", word_match({'style'}, nil, case_insensitive_tags))
local style_tag_open = parent_token("tag_open", P('<') * style_tag_name * ((ws * attribute) + tag_data)^0 * P('>'))
local style_tag_close = parent_token("tag_close", P('</') * style_tag_name * tag_data^0 * '>')
local style_data = token("style_data", (l.any - style_tag_close)^0)
local style_tag = parent_token('style_tag', style_tag_open * style_data * style_tag_close)

local script_tag_name = token("tag_name", word_match({'script'}, nil, case_insensitive_tags))
local script_tag_open = parent_token("tag_open", P('<') * script_tag_name * ((ws * attribute) + tag_data)^0 * P('>'))
local script_tag_close = parent_token("tag_close", P('</') * script_tag_name * tag_data^0 * '>')
local script_data = token("script_data", (l.any - script_tag_close)^0)
local script_tag = parent_token('script_tag', script_tag_open * script_data * script_tag_close)

-- Top level rules

-- Note: the ordering is important here as <script> and <style> have to supercede tag_open...
local tag = style_tag + script_tag + tag_open + tag_close

-- Entities.
local entity = token('entity', '&' * (l.any - l.space - ';' - '<' - '>' - "'" - '"' - "/" )^1 * ';')

-- Doctype.
local doctype = token('doctype', '<!' *
                      word_match({'doctype'}, nil, case_insensitive_tags) *
                      (l.any - '>')^1 * '>')

-- Data between tags
local data = token('data', (l.any - '<')^1)

M._rules = {
  {'comment', comment},
  {'doctype', doctype},
  {'tag', tag},
  {'entity', entity},
  {'data', data},
}

M._tokenstyles = {
}

M._foldsymbols = {
}

return M
