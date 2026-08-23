#!/usr/bin/env python3
"""Find UI strings in JS bundle that are NOT yet translated."""
import re
import json

bundle = open(r'C:\Users\26529\AppData\Local\Programs\openmausbot\resources\ui\assets\index-B14-933s.js', 'r', encoding='utf-8').read()
existing = set(json.load(open('locales/zh-CN.json', 'r', encoding='utf-8')).keys())

# Find all quoted strings starting with uppercase letter
all_strings = set()
for m in re.finditer(r'"([A-Z][^"]{1,100})"', bundle):
    s = m.group(1).strip()
    if len(s) >= 2 and s not in existing:
        all_strings.add(s)

for m in re.finditer(r"'([A-Z][^']{1,100})'", bundle):
    s = m.group(1).strip()
    if len(s) >= 2 and s not in existing:
        all_strings.add(s)

# Filter out code/SVG/technical
filtered = []
for s in all_strings:
    # Skip CSS/technical
    if any(x in s for x in ['\\n', '\\t', '\\r', '${', 'xmlns', 'viewBox', 'stroke', 'fill', 'opacity', 'translate', 'scale', 'rotate', 'matrix', 'rgb(', 'rgba(', 'hsl(']):
        continue
    # Skip SVG elements
    if s in ['Path', 'Circle', 'Rect', 'Line', 'G', 'Defs', 'ClipPath', 'Mask', 'Pattern', 'Use', 'Svg', 'Stop', 'Text', 'Tspan', 'Animate']:
        continue
    # Skip React internals
    if s in ['Fragment', 'Suspense', 'SuspenseList', 'Portal', 'StrictMode', 'Profiler', 'Lazy', 'ForwardRef', 'Memo', 'Activity', 'Module', 'Map', 'Set', 'Date', 'RegExp', 'Number', 'String', 'Boolean', 'Object', 'Array', 'ArrayBuffer', 'BigInt']:
        continue
    # Skip keyboard keys
    if s in ['Escape', 'Enter', 'Tab', 'Space', 'ArrowDown', 'ArrowUp', 'ArrowLeft', 'ArrowRight', 'PageUp', 'PageDown', 'Home', 'End', 'Delete', 'Insert', 'Backspace', 'CapsLock', 'NumLock', 'ScrollLock', 'PrintScreen', 'Pause', 'AltLeft', 'AltRight', 'ControlLeft', 'ControlRight', 'ShiftLeft', 'ShiftRight', 'MetaLeft', 'MetaRight', 'OSLeft', 'OSRight', 'ContextMenu']:
        continue
    # Skip browser/device strings
    if s in ['Android', 'iPhone', 'iPad', 'iPod', 'Mac', 'Windows', 'Linux', 'Chrome', 'Firefox', 'Safari', 'Edge', 'Opera', 'MSIE', 'Trident', 'Wayland', 'Xorg', 'Kobo', 'Kindle Fire', 'Wearable']:
        continue
    # Skip format/date strings
    if re.match(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$', s):
        continue
    # Skip short generic words
    if len(s) <= 3 and not any(c == ' ' for c in s):
        continue
    filtered.append(s)

filtered.sort(key=lambda x: (not ' ' in x, len(x)))
print(f'Found {len(filtered)} potential untranslated UI strings:')
for s in filtered:
    print(f'  [{s}]')
