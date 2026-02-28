import re
import sys

CSS_PATH = 'styles.css'

hex_re = re.compile(r"#([0-9a-fA-F]{3,8})")
var_re = re.compile(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;]+);")
prop_re = re.compile(r"([^{]+)\{([^}]+)\}", re.S)

def parse_hex(s):
    s = s.lstrip('#')
    if len(s) == 3:
        r = int(s[0]*2,16)
        g = int(s[1]*2,16)
        b = int(s[2]*2,16)
        return (r,g,b,1)
    if len(s) == 6:
        r = int(s[0:2],16)
        g = int(s[2:4],16)
        b = int(s[4:6],16)
        return (r,g,b,1)
    if len(s) == 8:
        r = int(s[0:2],16)
        g = int(s[2:4],16)
        b = int(s[4:6],16)
        a = int(s[6:8],16)/255
        return (r,g,b,a)
    raise ValueError(s)


def parse_rgb(s):
    s = s.strip()
    if s.startswith('rgba'):
        nums = re.findall(r"([0-9.]+)", s)
        r,g,b,a = map(float, nums[:4])
        return (int(r), int(g), int(b), a)
    if s.startswith('rgb'):
        nums = re.findall(r"([0-9.]+)", s)
        r,g,b = map(float, nums[:3])
        return (int(r), int(g), int(b), 1)
    return None


def composite(fg, bg):
    # fg and bg are (r,g,b,a)
    fr,fgc,fb,fa = fg
    br,bc,bb,ba = bg
    a = fa + ba*(1-fa)
    if a == 0:
        return (0,0,0,0)
    r = (fr*fa + br*ba*(1-fa))/a
    g = (fgc*fa + bc*ba*(1-fa))/a
    b = (fb*fa + bb*ba*(1-fa))/a
    return (r,g,b,a)


def srgb_to_lin(c):
    c = c/255.0
    if c <= 0.03928:
        return c/12.92
    return ((c+0.055)/1.055)**2.4


def luminance(rgb):
    r,g,b,_ = rgb
    R = srgb_to_lin(r)
    G = srgb_to_lin(g)
    B = srgb_to_lin(b)
    return 0.2126*R + 0.7152*G + 0.0722*B


def contrast(a,b):
    la = luminance(a)
    lb = luminance(b)
    L1 = max(la,lb)
    L2 = min(la,lb)
    return (L1+0.05)/(L2+0.05)


def parse_value(val, vars):
    val = val.strip()
    # css var
    if val.startswith('var('):
        m = re.match(r"var\(--([a-zA-Z0-9_-]+)\)", val)
        if m:
            k = m.group(1)
            return parse_value(vars.get(k, ''), vars)
    # hex
    m = hex_re.search(val)
    if m:
        return parse_hex(m.group(0))
    # rgb
    m2 = parse_rgb(val)
    if m2:
        return m2
    # rgba in the form rgba(0,0,0,0.5)
    # fallback: named color or unknown
    return None


def read_css_vars():
    with open(CSS_PATH,'r',encoding='utf-8') as f:
        text = f.read()
    vars = {}
    # parse :root block explicitly
    root_match = re.search(r":root\s*\{([^}]+)\}", text, re.S)
    if root_match:
        body = root_match.group(1)
        for m in var_re.finditer(body):
            vars[m.group(1).strip()] = m.group(2).strip()
    # also search for .body-wrapper color
    body_color = None
    for m in prop_re.finditer(text):
        sel = m.group(1)
        block = m.group(2)
        if '.body-wrapper' in sel:
            mm = re.search(r'color\s*:\s*([^;]+);', block)
            if mm:
                body_color = mm.group(1).strip()
    return vars, body_color


def find_rule(selector):
    with open(CSS_PATH,'r',encoding='utf-8') as f:
        text = f.read()
    m = re.search(r""+re.escape(selector)+r"\s*\{([^}]+)\}", text, re.S)
    return m.group(1).strip() if m else ''


def parse_gradient_avg(s):
    # extract rgba/hex stops and average them
    stops = []
    for m in re.finditer(r"rgba?\([^\)]+\)", s):
        v = parse_rgb(m.group(0))
        if v:
            stops.append(v)
    for m in re.finditer(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", s):
        v = parse_hex(m.group(0))
        stops.append(v)
    if not stops:
        return None
    # average RGB and alpha
    r = sum(x[0] for x in stops)/len(stops)
    g = sum(x[1] for x in stops)/len(stops)
    b = sum(x[2] for x in stops)/len(stops)
    a = sum(x[3] for x in stops)/len(stops)
    return (r,g,b,a)


def to_rgb(val, vars, fallback_bg=None):
    v = parse_value(val, vars)
    if v:
        return v
    # fallback: if val is rgba(...) or similar already, try parsing
    return None


def run_check():
    vars, body_color = read_css_vars()
    bg = to_rgb(vars.get('bg-1'), vars) or (4,20,36,1)
    muted = to_rgb(vars.get('muted'), vars) or (200,220,240,1)
    accent = to_rgb(vars.get('accent'), vars) or (6,182,212,1)
    card_bg_raw = vars.get('card-bg') or 'rgba(255,255,255,0.02)'
    card_bg = parse_rgb(card_bg_raw) or (255,255,255,0.02)
    body = None
    if body_color:
        body = parse_value(body_color, vars)
    if not body:
        # fallback to muted
        body = muted

    # composite card bg over bg base
    comp_card = composite(card_bg, bg)

    pairs = [
        ('Background (--bg-1)', bg, 'Body text (.body-wrapper)', body),
        ('Background (--bg-1)', bg, '--muted', muted),
        ('Background (--bg-1)', bg, '--accent', accent),
        ('Card background (composited)', comp_card, 'Card title (.card h3)', (255,255,255,1)),
    ]

    # Additional UI element checks
    # pills (.pill), tab.active background, nav hover backgrounds
    pill_rule = find_rule('.pill')
    pill_bg = parse_gradient_avg(pill_rule) or card_bg
    # try to read color from rule, fallback to --accent
    pill_color_match = re.search(r'color\s*:\s*([^;]+);', pill_rule)
    if pill_color_match:
        pill_text = parse_value(pill_color_match.group(1).strip(), vars) or to_rgb('var(--accent)', vars) or accent
    else:
        pill_text = to_rgb('var(--accent)', vars) or accent
    pill_comp = composite(pill_bg, bg) if pill_bg else comp_card

    tab_active_rule = find_rule('.tab.active')
    tab_bg = parse_gradient_avg(tab_active_rule)
    tab_color_match = re.search(r'color\s*:\s*([^;]+);', tab_active_rule)
    if tab_color_match:
        tab_text = parse_value(tab_color_match.group(1).strip(), vars) or to_rgb('var(--accent)', vars) or accent
    else:
        tab_text = to_rgb('var(--accent)', vars) or accent
    tab_comp = composite(tab_bg, bg) if tab_bg else bg

    nav_hover_rule = find_rule('.nav-link:hover')
    m = re.search(r'background\s*:\s*([^;]+);', nav_hover_rule)
    nav_hover_bg_raw = m.group(1).strip() if m else 'rgba(255,255,255,0.04)'
    nav_hover_bg = parse_rgb(nav_hover_bg_raw) or parse_value(nav_hover_bg_raw, vars)
    nav_hover_comp = composite(nav_hover_bg, bg) if nav_hover_bg else bg
    nav_hover_text = to_rgb('var(--accent)', vars) or accent

    pairs += [
        ('Pill background (avg stops)', pill_comp, 'Pill text (--accent)', pill_text),
        ('Tab.active background (avg stops)', tab_comp, 'Tab.active text (--accent)', tab_text),
        ('Nav hover background', nav_hover_comp, 'Nav hover text (--accent)', nav_hover_text),
    ]

    print('Contrast check results (WCAG):')
    for a_name,a,b_name,b in pairs:
        try:
            ratio = contrast(a,b)
            ok = 'PASS' if ratio >= 4.5 else ('AA-large' if ratio>=3 else 'FAIL')
            print(f"{a_name} vs {b_name}: {ratio:.2f} — {ok}")
        except Exception as e:
            print('Error computing',a_name,b_name,e)

if __name__=='__main__':
    run_check()
