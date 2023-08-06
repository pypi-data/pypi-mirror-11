-- Copyright 2006-2015 Mitchell mitchell.att.foicica.com. See LICENSE.
-- CSS LPeg lexer.

local l = require('lexer')
local token, word_match = l.token, l.word_match
local P, R, S, V = lpeg.P, lpeg.R, lpeg.S, lpeg.V

local M = {_NAME = 'css'}

-- Whitespace.
local ws = token(l.WHITESPACE, l.space^1)

-- Comments.
local comment = token(l.COMMENT, '/*' * (l.any - '*/')^0 * P('*/')^-1)

-- Strings.
local sq_str = l.delimited_range("'")
local dq_str = l.delimited_range('"')
local string = token(l.STRING, sq_str + dq_str)

-- Numbers.
local number = token(l.NUMBER, l.digit^1)

-- Keywords.
local css1_property = word_match({
  'color', 'background-color', 'background-image', 'background-repeat',
  'background-attachment', 'background-position', 'background', 'font-family',
  'font-style', 'font-variant', 'font-weight', 'font-size', 'font',
  'word-spacing', 'letter-spacing', 'text-decoration', 'vertical-align',
  'text-transform', 'text-align', 'text-indent', 'line-height', 'margin-top',
  'margin-right', 'margin-bottom', 'margin-left', 'margin', 'padding-top',
  'padding-right', 'padding-bottom', 'padding-left', 'padding',
  'border-top-width', 'border-right-width', 'border-bottom-width',
  'border-left-width', 'border-width', 'border-top', 'border-right',
  'border-bottom', 'border-left', 'border', 'border-color', 'border-style',
  'width', 'height', 'float', 'clear', 'display', 'white-space',
  'list-style-type', 'list-style-image', 'list-style-position', 'list-style'
}, '-')
local css1_value = word_match({
  'auto', 'none', 'normal', 'italic', 'oblique', 'small-caps', 'bold', 'bolder',
  'lighter', 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large',
  'xx-large', 'larger', 'smaller', 'transparent', 'repeat', 'repeat-x',
  'repeat-y', 'no-repeat', 'scroll', 'fixed', 'top', 'bottom', 'left', 'center',
  'right', 'justify', 'both', 'underline', 'overline', 'line-through', 'blink',
  'baseline', 'sub', 'super', 'text-top', 'middle', 'text-bottom', 'capitalize',
  'uppercase', 'lowercase', 'thin', 'medium', 'thick', 'dotted', 'dashed',
  'solid', 'double', 'groove', 'ridge', 'inset', 'outset', 'block', 'inline',
  'list-item', 'pre', 'no-wrap', 'inside', 'outside', 'disc', 'circle',
  'square', 'decimal', 'lower-roman', 'upper-roman', 'lower-alpha',
  'upper-alpha', 'aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 'lime',
  'maroon', 'navy', 'olive', 'purple', 'red', 'silver', 'teal', 'white',
  'yellow'
}, '-')
local css2_property = word_match({
  'border-top-color', 'border-right-color', 'border-bottom-color',
  'border-left-color', 'border-color', 'border-top-style', 'border-right-style',
  'border-bottom-style', 'border-left-style', 'border-style', 'top', 'right',
  'bottom', 'left', 'position', 'z-index', 'direction', 'unicode-bidi',
  'min-width', 'max-width', 'min-height', 'max-height', 'overflow', 'clip',
  'visibility', 'content', 'quotes', 'counter-reset', 'counter-increment',
  'marker-offset', 'size', 'marks', 'page-break-before', 'page-break-after',
  'page-break-inside', 'page', 'orphans', 'widows', 'font-stretch',
  'font-size-adjust', 'unicode-range', 'units-per-em', 'src', 'panose-1',
  'stemv', 'stemh', 'slope', 'cap-height', 'x-height', 'ascent', 'descent',
  'widths', 'bbox', 'definition-src', 'baseline', 'centerline', 'mathline',
  'topline', 'text-shadow', 'caption-side', 'table-layout', 'border-collapse',
  'border-spacing', 'empty-cells', 'speak-header', 'cursor', 'outline',
  'outline-width', 'outline-style', 'outline-color', 'volume', 'speak',
  'pause-before', 'pause-after', 'pause', 'cue-before', 'cue-after', 'cue',
  'play-during', 'azimuth', 'elevation', 'speech-rate', 'voice-family', 'pitch',
  'pitch-range', 'stress', 'richness', 'speak-punctuation', 'speak-numeral'
}, '-')
local css2_value = word_match({
  'inherit', 'run-in', 'compact', 'marker', 'table', 'inline-table',
  'table-row-group', 'table-header-group', 'table-footer-group', 'table-row',
  'table-column-group', 'table-column', 'table-cell', 'table-caption', 'static',
  'relative', 'absolute', 'fixed', 'ltr', 'rtl', 'embed', 'bidi-override',
  'visible', 'hidden', 'scroll', 'collapse', 'open-quote', 'close-quote',
  'no-open-quote', 'no-close-quote', 'decimal-leading-zero', 'lower-greek',
  'lower-latin', 'upper-latin', 'hebrew', 'armenian', 'georgian',
  'cjk-ideographic', 'hiragana', 'katakana', 'hiragana-iroha', 'katakana-iroha',
  'landscape', 'portrait', 'crop', 'cross', 'always', 'avoid', 'wider',
  'narrower', 'ultra-condensed', 'extra-condensed', 'condensed',
  'semi-condensed', 'semi-expanded', 'expanded', 'extra-expanded',
  'ultra-expanded', 'caption', 'icon', 'menu', 'message-box', 'small-caption',
  'status-bar', 'separate', 'show', 'hide', 'once', 'crosshair', 'default',
  'pointer', 'move', 'text', 'wait', 'help', 'e-resize', 'ne-resize',
  'nw-resize', 'n-resize', 'se-resize', 'sw-resize', 's-resize', 'w-resize',
  'ActiveBorder', 'ActiveCaption', 'AppWorkspace', 'Background', 'ButtonFace',
  'ButtonHighlight', 'ButtonShadow', 'InactiveCaptionText', 'ButtonText',
  'CaptionText', 'GrayText', 'Highlight', 'HighlightText', 'InactiveBorder',
  'InactiveCaption', 'InfoBackground', 'InfoText', 'Menu', 'MenuText',
  'Scrollbar', 'ThreeDDarkShadow', 'ThreeDFace', 'ThreeDHighlight',
  'ThreeDLightShadow', 'ThreeDShadow', 'Window', 'WindowFrame', 'WindowText',
  'silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud', 'spell-out', 'mix',
  'left-side', 'far-left', 'center-left', 'center-right', 'far-right',
  'right-side', 'behind', 'leftwards', 'rightwards', 'below', 'level', 'above',
  'higher', 'lower', 'x-slow', 'slow', 'medium', 'fast', 'x-fast', 'faster',
  'slower', 'male', 'female', 'child', 'x-low', 'low', 'high', 'x-high', 'code',
  'digits', 'continous'
}, '-')

local css3_property = word_match({
  'align-content', 'align-items', 'align-self', 'alignment-adjust',
  'alignment-baseline', 'all', 'anchor-point', 'animation', 'animation-delay',
  'animation-direction', 'animation-duration', 'animation-fill-mode',
  'animation-iteration-count', 'animation-name', 'animation-play-state',
  'animation-timing-function', 'backface-visibility', 'background-clip',
  'background-origin', 'background-size', 'baseline-shift', 'binding', 'bleed',
  'bookmark-label', 'bookmark-level', 'bookmark-state', 'border-bottom-left-radius',
  'border-bottom-right-radius', 'border-image', 'border-image-outset',
  'border-image-repeat', 'border-image-slice', 'border-image-source',
  'border-image-width', 'border-radius', 'border-top-left-radius',
  'border-top-right-radius', 'box-decoration-break', 'box-shadow', 'box-sizing',
  'box-snap', 'box-suppress', 'break-after', 'break-before', 'break-inside',
  'chains', 'clip-path', 'clip-rule', 'color-interpolation-filters', 'column-count',
  'column-fill', 'column-gap', 'column-rule', 'column-rule-color', 'column-rule-style',
  'column-rule-width', 'column-span', 'column-width', 'columns', 'contain',
  'counter-set', 'crop', 'display-inside', 'display-list', 'display-outside',
  'dominant-baseline', 'filter', 'flex', 'flex-basis', 'flex-direction', 'flex-flow',
  'flex-grow', 'flex-shrink', 'flex-wrap', 'float-offset', 'flood-color',
  'flood-opacity', 'flow-from', 'flow-into', 'font-feature-settings', 'font-kerning',
  'font-language-override', 'font-synthesis', 'font-variant-alternates',
  'font-variant-caps', 'font-variant-east-asian', 'font-variant-ligatures',
  'font-variant-numeric', 'font-variant-position', 'grid', 'grid-area',
  'grid-auto-columns', 'grid-auto-flow', 'grid-auto-rows', 'grid-column',
  'grid-column-end', 'grid-column-start', 'grid-row', 'grid-row-end', 'grid-row-start',
  'grid-template', 'grid-template-areas', 'grid-template-columns', 'grid-template-rows',
  'hanging-punctuation', 'hyphens', 'icon', 'image-orientation', 'image-resolution',
  'ime-mode', 'initial-letters', 'inline-box-align', 'justify-content', 'justify-items',
  'justify-self', 'lighting-color', 'line-box-contain', 'line-break', 'line-grid',
  'line-snap', 'line-stacking', 'line-stacking-ruby', 'line-stacking-shift',
  'line-stacking-strategy', 'marker-side', 'mask', 'mask-box', 'mask-box-outset',
  'mask-box-repeat', 'mask-box-slice', 'mask-box-source', 'mask-box-width',
  'mask-clip', 'mask-image', 'mask-origin', 'mask-position', 'mask-repeat', 'mask-size',
  'mask-source-type', 'mask-type', 'max-lines', 'move-to', 'nav-down', 'nav-index',
  'nav-left', 'nav-right', 'nav-up', 'object-fit', 'object-position', 'opacity',
  'order', 'outline-offset', 'overflow-wrap', 'overflow-x', 'overflow-y', 'page-policy',
  'perspective', 'perspective-origin', 'presentation-level', 'region-fragment',
  'resize', 'rest', 'rest-after', 'rest-before', 'rotation', 'rotation-point',
  'ruby-align', 'ruby-merge', 'ruby-position', 'shape-image-threshold', 'shape-outside',
  'shape-margin', 'speak-as', 'string-set', 'tab-size', 'text-align-last',
  'text-combine-upright', 'text-decoration-color', 'text-decoration-line',
  'text-decoration-skip', 'text-decoration-style', 'text-emphasis', 'text-emphasis-color',
  'text-emphasis-color', 'text-emphasis-style', 'text-height', 'text-justify',
  'text-orientation', 'text-overflow', 'text-space-collapse', 'text-underline-position',
  'text-wrap', 'transform', 'transform-origin', 'transform-style', 'transition',
  'transition-delay', 'transition-duration', 'transition-property',
  'transition-timing-function', 'voice-balance', 'voice-duration', 'voice-pitch',
  'voice-range', 'voice-rate', 'voice-stress', 'voice-volume', 'will-change',
  'word-break', 'word-wrap', 'wrap-flow', 'wrap-through', 'writing-mode',
  })


local property = token('property', css1_property + css2_property + css3_property)
local value = token('value', css1_value + css2_value)
local keyword = property + value

-- Identifiers.
local identifier = token(l.IDENTIFIER, l.alpha * (l.alnum + S('_-'))^0)

-- Operators.
local operator = token(l.OPERATOR, S('~!#*>+=|.,:;()[]{}'))

-- At rule.
local at_rule = token('at_rule', P('@') * word_match{
  'charset', 'font-face', 'media', 'page', 'import'
})

-- Colors.
local xdigit = l.xdigit
local hex_color = '#' * xdigit * xdigit * xdigit * (xdigit * xdigit * xdigit)^-1
local color_name = word_match{
  'aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 'lime', 'maroon', 'navy',
  'olive', 'orange', 'purple', 'red', 'silver', 'teal', 'white', 'yellow'
}
local color = token('color', hex_color + color_name)

-- Pseudo.
local pseudo = token(l.CONSTANT, word_match({
  -- Pseudo elements.
  'first-line', 'first-letter', 'before', 'after',
  -- Pseudo classes.
  'first-child', 'link', 'visited', 'hover', 'active', 'focus', 'lang',
}, '-'))

-- Units.
local unit = token('unit', word_match{
  'em', 'ex', 'px', 'pt', 'pc', 'in', 'ft', 'mm', 'cm', 'kHz', 'Hz', 'deg',
  'rad', 'grad', 'ms', 's'
} + '%')

-- Immunio marker
local marker = l.token('marker', P('{immunio-var:') * l.integer * ':' * l.xdigit^1 * '}')

M._rules = {
  {'whitespace', ws},
  {'marker', marker},
  {'keyword', keyword},
  {'pseudo', pseudo},
  {'color', color},
  {'identifier', identifier},
  {'string', string},
  {'comment', comment},
  {'number', number * unit^-1},
  {'operator', operator},
  {'at_rule', at_rule},
}

M._tokenstyles = {
}

M._foldsymbols = {
}

return M
