#!/usr/bin/env python3
# Author: xit exploiter | TBCN
# Multi Decoder Pro Max - Fixed Version

import base64, urllib.parse, codecs, sys, os, re, html, zlib, gzip, binascii

# COLORS
G="\033[92m"; R="\033[91m"; C="\033[96m"; Y="\033[93m"; W="\033[0m"

# BANNER
def banner():
    os.system("cls" if os.name=="nt" else "clear")
    print(G+r"""
████████╗██████╗  ██████╗███╗   ██╗
╚══██╔══╝██╔══██╗██╔════╝████╗  ██║
   ██║   ██████╔╝██║     ██╔██╗ ██║
   ██║   ██╔══██╗██║     ██║╚██╗██║
   ██║   ██████╔╝╚██████╗██║ ╚████║
   ╚═╝   ╚═════╝  ╚═════╝╚═╝  ╚═══╝

      MULTI DECODER PRO MAX
      Dev : xit exploiter | TBCN
""" + W)

# SAFE EXEC
def safe(func, data):
    try:
        r = func(data)
        if isinstance(r, bytes):
            return r.decode(errors='ignore')
        if isinstance(r, str):
            return r.strip() or None
        return str(r)
    except Exception:
        return None

def b64url(d):
    d += "=" * (-len(d) % 4)
    return base64.urlsafe_b64decode(d).decode(errors='ignore')

# CORE DECODERS
decoders = {
    # BASE
    "Base64": lambda d: base64.b64decode(d).decode(errors='ignore'),
    "Base64 URL": b64url,
    "Double Base64": lambda d: base64.b64decode(base64.b64decode(d)).decode(errors='ignore'),
    "Base32": lambda d: base64.b32decode(d).decode(errors='ignore'),
    "Base16": lambda d: base64.b16decode(d.upper()).decode(errors='ignore'),
    "Base85": lambda d: base64.b85decode(d).decode(errors='ignore'),
    "Ascii85": lambda d: base64.a85decode(d).decode(errors='ignore'),

    # URL / HTML
    "URL Decode": lambda d: urllib.parse.unquote(d),
    "Double URL Decode": lambda d: urllib.parse.unquote(urllib.parse.unquote(d)),
    "HTML Entity": lambda d: html.unescape(d),
    "Unicode Escape": lambda d: d.encode(errors='ignore').decode("unicode_escape", errors='ignore'),

    # TEXT
    "Reverse": lambda d: d[::-1],
    "Reverse Words": lambda d: ' '.join(d.split()[::-1]),
    "Swap Case": lambda d: d.swapcase(),
    "Lowercase": lambda d: d.lower(),
    "Uppercase": lambda d: d.upper(),
    "Strip Non-ASCII": lambda d: re.sub(r'[^\x00-\x7F]+','',d),

    # ROT / CLASSIC
    "ROT13": lambda d: codecs.decode(d,"rot_13"),
    "ROT5": lambda d: codecs.decode(d,"rot_5"),
    "ROT47": lambda d: ''.join(chr(33+(ord(c)-33+47)%94) if 33<=ord(c)<=126 else c for c in d),
    "Atbash": lambda d: ''.join(chr(219-ord(c)) if c.isalpha() else c for c in d),

    # NUMBER BASE
    "Hex": lambda d: bytes.fromhex(d).decode(errors='ignore'),
    "Hex Reversed Bytes": lambda d: bytes.fromhex(d)[::-1].decode(errors='ignore'),
    "Binary": lambda d: ''.join(chr(int(b,2)) for b in d.split()),
    "Binary (No Space)": lambda d: ''.join(chr(int(d[i:i+8],2)) for i in range(0,len(d),8)),
    "Binary Reversed": lambda d: ''.join(chr(int(b[::-1],2)) for b in d.split()),
    "Octal": lambda d: ''.join(chr(int(x,8)) for x in d.split()),
    "Decimal ASCII": lambda d: ''.join(chr(int(x)) for x in d.split()),

    # COMPRESSION
    "Zlib": lambda d: zlib.decompress(base64.b64decode(d)).decode(errors='ignore'),
    "Gzip": lambda d: gzip.decompress(base64.b64decode(d)).decode(errors='ignore'),

    # XOR / SIMPLE
    "XOR-1": lambda d: ''.join(chr(ord(c)^1) for c in d),
    "XOR-42": lambda d: ''.join(chr(ord(c)^42) for c in d),

    # JWT
    "JWT Header": lambda d: b64url(d.split('.')[0]),
    "JWT Payload": lambda d: b64url(d.split('.')[1]),

    # MORSE
    "Morse": lambda d: ''.join({
        ".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E","..-.":"F","--.":"G",
        "....":"H","..":"I",".---":"J","-.-":"K",".-..":"L","--":"M","-.":"N",
        "---":"O",".--":"P","--.-":"Q",".-.":"R","...":"S","-":"T","..-":"U",
        "...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z","/":" "
    }.get(x,"") for x in d.split()),

    # CAESAR
    "Caesar -1": lambda d: ''.join(chr(ord(c)-1) if c.isprintable() else c for c in d),
    "Caesar -3": lambda d: ''.join(chr(ord(c)-3) if c.isprintable() else c for c in d),
    "Caesar +1": lambda d: ''.join(chr(ord(c)+1) if c.isprintable() else c for c in d),
    "Caesar +3": lambda d: ''.join(chr(ord(c)+3) if c.isprintable() else c for c in d),

    # ESCAPES
    "JS \\uXXXX": lambda d: re.sub(r'\\u([0-9a-fA-F]{4})',lambda m: chr(int(m.group(1),16)),d),
    "HTML Hex Entity": lambda d: re.sub(r'&#x([0-9a-fA-F]+);',lambda m: chr(int(m.group(1),16)),d),
}

# MENU 
def menu():
    print(C+"\nAvailable Decoders:\n"+W)
    for i,n in enumerate(decoders,start=1):
        print(f"[{i:02}] {n}")
    print("[99] Auto Decode")
    print("[00] Exit\n")

# AUTO DECODE
def auto_decode(data, depth=5):
    seen=set()
    cur=data
    print(Y+"\n[+] Auto decoding...\n"+W)
    for _ in range(depth):
        decoded=False
        for name,f in decoders.items():
            r=safe(f,cur)
            if r and r not in seen and r != cur:
                seen.add(r)
                print(G+f"[✔] {name}"+W)
                print(r)
                print("-"*60)
                cur=r
                decoded=True
                break
        if not decoded:
            break  # stop if nothing new decoded

# MAIN
banner()
while True:
    menu()
    ch=input(Y+"Select option: "+W)
    if ch in ("0","00"):
        sys.exit()
    data=input(C+"Enter encoded text: "+W)
    if ch=="99":
        auto_decode(data)
    else:
        try:
            key=list(decoders)[int(ch)-1]
            r=safe(decoders[key],data)
            if r:
                print(G+f"\n[✔] {key} Result:\n"+W+r)
            else:
                print(R+"Decode failed"+W)
        except Exception:
            print(R+"Invalid option"+W)
    input(Y+"\nPress Enter to continue..."+W)
    banner()
