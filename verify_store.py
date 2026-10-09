#!/usr/bin/env python3
"""Verify signed catalog and original MDX packages; never execute them."""
import base64
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT=Path(__file__).resolve().parent
EXPECTED={'official.spotify','official.gta','official.discord','official.obs',
          'official.steam','official.voicemod','official.amd','official.meter',
          'official.voicemeeter','official.playnite'}

def dec(v):
    v=v.strip()
    return base64.b64decode(v+'='*((-len(v))%4))

def main():
    e=json.loads((ROOT/'catalog.signed.json').read_text('utf8'))
    cat=e['catalog']; items=cat['items']
    assert cat['schema']==1 and len(items)==10
    assert {x['id'] for x in items}==EXPECTED
    assert len(list((ROOT/'packages').glob('*.mdx')))==10
    pub=Ed25519PublicKey.from_public_bytes(dec((ROOT/'catalog_public.b64').read_text()))
    canonical=json.dumps(cat,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').encode('utf8')
    assert b'\xe2\x80\xa8' not in canonical and b'\xe2\x80\xa9' not in canonical
    pub.verify(dec(e['signature']),canonical)
    roots=[Ed25519PublicKey.from_public_bytes(dec(s)) for s in (ROOT/'extension_public_keys.csv').read_text().strip().split(',') if s.strip()]
    assert len(roots)>=10
    for item in items:
        rel=item['packageUrl']
        assert rel.startswith('packages/') and rel.count('/')==1 and '..' not in rel and rel.endswith('.mdx')
        assert 'medal' not in (item['id']+rel).lower()
        blob=(ROOT/rel).read_bytes()
        assert len(blob)<=64*1024*1024 and len(blob)==item['size'] and hashlib.sha256(blob).hexdigest()==item['sha256']
        with ZipFile(ROOT/rel) as z:
            names=z.namelist()
            assert 'signature.ed25519' in names and len(names)==len(set(names))
            assert all(not n.startswith('/') and '..' not in Path(n).parts and '\\' not in n for n in names)
            data={n:z.read(n) for n in names if n!='signature.ed25519'}
            sig=dec(z.read('signature.ed25519').decode())
            h=hashlib.sha256()
            for n in sorted(data):
                b=data[n]
                h.update(n.encode());h.update(b'\0');h.update(len(b).to_bytes(8,'big'));h.update(b)
            digest=h.digest()
            valid=False
            for key in roots:
                try: key.verify(sig,digest);valid=True;break
                except Exception: pass
            assert valid,rel+' has invalid MDX signature'
        print('OK',rel)
    print('OK: 10 signed MDX packages; Medal absent. Antivirus clearance NOT implied.')

if __name__=='__main__': main()
