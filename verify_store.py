#!/usr/bin/env python3
"""Read-only CI gate for public MadsDeckStore. Does not execute any .mdx code."""
import base64
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT = Path(__file__).resolve().parent
MAX_PACKAGE_BYTES = 64 * 1024 * 1024
EXPECTED = {
    'official.amd','official.discord','official.gta','official.meter',
    'official.obs','official.playnite','official.spotify','official.steam',
    'official.voicemeeter','official.voicemod',
}

def b64_decode(text):
    return base64.b64decode(text.strip()+'='*((-len(text.strip()))%4))

def main():
    envelope=json.loads((ROOT/'catalog.signed.json').read_text(encoding='utf8'))
    cat=envelope['catalog']
    assert cat['schema']==1
    items=cat['items']
    assert len(items)==10
    assert {x['id'] for x in items}==EXPECTED
    assert all('medal' not in x['id'].lower() and 'medal' not in x['packageUrl'].lower() for x in items)
    assert len(list((ROOT/'packages').glob('*.mdx')))==10, 'No other MDX files permitted'
    pub=Ed25519PublicKey.from_public_bytes(b64_decode((ROOT/'catalog_public.b64').read_text()))
    canonical=json.dumps(cat,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').encode('utf8')
    # Go encoding/json escapes U+2028/U+2029 as well; none are present in this catalog.
    assert b'\xe2\x80\xa8' not in canonical and b'\xe2\x80\xa9' not in canonical
    pub.verify(b64_decode(envelope['signature']),canonical)
    extension_keys=[Ed25519PublicKey.from_public_bytes(b64_decode(s)) for s in (ROOT/'extension_public_keys.csv').read_text().strip().split(',') if s.strip()]
    assert len(extension_keys)>=10
    for x in items:
        rel=x['packageUrl']
        assert rel.startswith('packages/') and rel.count('/')==1 and '..' not in rel and rel.endswith('.mdx')
        data=(ROOT/rel).read_bytes()
        assert len(data)<MAX_PACKAGE_BYTES and len(data)==x['size']
        assert hashlib.sha256(data).hexdigest()==x['sha256']
        with ZipFile(ROOT/rel) as z:
            filenames=z.namelist()
            assert len(filenames)==len(set(filenames)), 'Duplicate file in MDX'
            assert all(not p.startswith('/') and '..' not in Path(p).parts and '\\' not in p for p in filenames)
            assert 'signature.ed25519' in filenames
            files={n:z.read(n) for n in filenames if n!='signature.ed25519'}
            signature=b64_decode(z.read('signature.ed25519').decode())
            h=hashlib.sha256()
            for n in sorted(files):
                buf=files[n]
                h.update(n.encode());h.update(b'\0');h.update(len(buf).to_bytes(8,'big'));h.update(buf)
            digest=h.digest()
            ok=False
            for k in extension_keys:
                try:
                    k.verify(signature,digest);ok=True;break
                except Exception:
                    pass
            assert ok, f'Invalid package signature: {rel}'
        print('Verified',rel)
    print('PASS: 10 packages and Store catalog cryptographically verified; Medal absent')
    print('NOTE: This does not constitute antivirus/malware clearance.')

if __name__=='__main__':main()
