# MadsDeckStore — 10 extensões

Distribuição estática da Store para MadsDeck Core/Native alpha.10, separada do repositório principal.

- **Medal (official.medal)**: temporariamente suspensa em razão do alerta Microsoft Defender `Trojan:Win32/Wacatac.C!ml`.
- **10 pacotes**: originais e idênticos aos arquivos `.mdx` anteriores; hashes em `SHA256_PUBLICACAO.json`.
- **Catálogo**: assinado com **nova chave Ed25519**. O Core precisa reconhecer a chave pública nova para aceitar este catálogo. A chave privada não deve ser publicada.
- **Segurança**: integridade e assinaturas do MadsDeck não substituem uma análise antimalware independente. Não desative o antivírus.

### GitHub Pages

Após subir os arquivos, configure `Settings -> Pages -> Deploy from a branch -> main -> /(root)`.

URL esperada: `https://brumad.github.io/MadsDeckStore/catalog.signed.json`.

**Recomendação de publicação:** envie primeiro os dez arquivos `packages/*.mdx`, confirme os hashes remotos e por último publique `catalog.signed.json` para evitar exibir downloads indisponíveis.
