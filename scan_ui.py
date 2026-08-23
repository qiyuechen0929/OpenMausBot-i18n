#!/usr/bin/env python3
"""Deep scan JS bundle for untranslated UI strings."""
import re
import json

bundle_path = r'C:\Users\26529\AppData\Local\Programs\openmausbot\resources\ui\assets\index-B14-933s.js'
with open(bundle_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all string literals
strings = re.findall(r'"((?:[^"\\]|\\.)*)"', content)

with open('locales/zh-CN.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)
existing_keys = set(existing.keys())

# Patterns to skip
SKIP_PATTERNS = [
    r'^[a-z]+(-[a-z]+)+(\s+[a-z]+(-[a-z]+)+)*$',  # CSS classes
    r'^\d+(\.\d+)?px$',  # pixel values
    r'^#[0-9a-fA-F]+$',  # hex colors
    r'^rgba?\(',  # rgb colors
    r'^translate',  # CSS transforms
    r'^scale\(',  # CSS transforms
    r'^rotate\(',  # CSS transforms
    r'^matrix\(',  # CSS transforms
    r'^var\(--',  # CSS variables
]

SKIP_EXACT = {
    'flex', 'grid', 'block', 'inline', 'hidden', 'absolute', 'relative',
    'fixed', 'sticky', 'static', 'none', 'auto', 'center', 'left', 'right',
    'top', 'bottom', 'start', 'end', 'normal', 'bold', 'italic', 'underline',
    'uppercase', 'lowercase', 'capitalize', 'truncate', 'overflow', 'hidden',
    'visible', 'scroll', 'solid', 'dashed', 'dotted', 'double', 'groove',
    'ridge', 'inset', 'outset', 'transparent', 'currentColor', 'inherit',
    'initial', 'unset', 'revert', 'pointer', 'default', 'grab', 'grabbing',
    'not-allowed', 'wait', 'help', 'progress', 'text', 'crosshair', 'move',
    'resize', 'zoom-in', 'zoom-out', 'col-resize', 'row-resize', 'no-drop',
    'url', 'data', 'blob', 'file', 'http', 'https', 'ftp', 'mailto',
    'tel', 'sms', 'ssh', 'ws', 'wss', 'javascript', 'void', 'null',
    'undefined', 'true', 'false', 'NaN', 'Infinity', 'globalThis',
    'object', 'function', 'string', 'number', 'boolean', 'symbol',
    'bigint', 'undefined', 'function', 'object', 'number', 'string',
    'boolean', 'symbol', 'bigint', 'undefined', 'function', 'object',
}

SKIP_PREFIXES = (
    'webkit', 'moz', 'ms', 'o', 'webkit-', 'moz-', 'ms-', 'o-',
    'data-', 'aria-', 'role=', 'tabindex', 'aria', 'role',
    'svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon',
    'ellipse', 'g', 'defs', 'clipPath', 'mask', 'pattern', 'use',
    'linearGradient', 'radialGradient', 'stop', 'text', 'tspan',
    'textPath', 'switch', 'foreignObject', 'desc', 'title',
    'feBlend', 'feColorMatrix', 'feComponentTransfer', 'feComposite',
    'feConvolveMatrix', 'feDiffuseLighting', 'feDisplacementMap',
    'feFlood', 'feGaussianBlur', 'feImage', 'feMerge', 'feMergeNode',
    'feMorphology', 'feOffset', 'fePointLight', 'feSpecularLighting',
    'feSpotLight', 'feTile', 'feTurbulence', 'animate', 'animateMotion',
    'animateTransform', 'set',
)

likely_ui = []
for s in strings:
    s_stripped = s.strip()
    if len(s_stripped) < 3:
        continue
    if s_stripped in existing_keys:
        continue
    if s_stripped in SKIP_EXACT:
        continue
    
    skip = False
    for pat in SKIP_PATTERNS:
        if re.match(pat, s_stripped):
            skip = True
            break
    if skip:
        continue
    
    # Skip SVG attributes
    if any(s_stripped.startswith(p) for p in SKIP_PREFIXES):
        continue
    
    # Skip things that look like code
    if any(x in s_stripped for x in ['JSON.', '.catch(', 'setAttribute', 'innerHTML', 'appendChild', 'querySelector', 'getElementById', 'addEventListener', 'removeEventListener', 'classList.', 'style.', 'className', 'textContent', 'innerText', 'innerHTML', 'outerHTML', 'nodeType', 'nodeName', 'nodeValue', 'parentNode', 'childNodes', 'firstChild', 'lastChild', 'nextSibling', 'previousSibling', 'ownerDocument', 'documentElement', 'body', 'head', 'title', 'meta', 'link', 'script', 'style', 'base', 'br', 'hr', 'img', 'input', 'source', 'track', 'wbr', 'iframe', 'embed', 'object', 'param', 'video', 'audio', 'canvas', 'map', 'area', 'col', 'colgroup', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th', 'caption', 'figure', 'figcaption', 'details', 'summary', 'dialog', 'template', 'slot', 'portal', 'fragment']):
        continue
    
    # Skip CSS class lists (space-separated lowercase words with hyphens)
    if ' ' in s_stripped:
        words = s_stripped.split()
        css_count = sum(1 for w in words if '-' in w or w.islower() or re.match(r'^[\[\]\d\.]+$', w))
        if css_count > len(words) * 0.5:
            continue
    
    # Must contain at least one word starting with uppercase (UI text pattern)
    if re.search(r'[A-Z][a-z]', s_stripped):
        likely_ui.append(s_stripped)

likely_ui.sort(key=len)
print(f'Found {len(likely_ui)} potential UI strings not yet translated:')
for s in likely_ui:
    print(f'  [{s}]')
