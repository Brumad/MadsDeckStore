# MadsDeckStore

Repositório **independente** destinado exclusivamente à publicação do catálogo assinado e dos pacotes de extensões do MadsDeck Core/Native alpha.10, via GitHub Pages.

> **Importante:** este repositório não contém o aplicativo MadsDeck nem seu código-fonte. O Core Windows e o APK Android permanecem no projeto original. Os pacotes deste repositório são da linha de desenvolvimento **DemoDev**.

## Estrutura

- `catalog.signed.json`: catálogo assinado (não modificar sem gerar nova assinatura).
- `packages/*.mdx`: 11 pacotes originais assinados, publicados sem alteração dos bytes.
- `.nojekyll`: publicação estática sem processamento do Jekyll.

## URL prevista

`https://brumad.github.io/MadsDeckStore/catalog.signed.json`

A URL funcionará apenas depois de habilitar **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root)** e publicar os arquivos.

## Segurança

Não enviar tokens, chaves privadas, arquivos do APK/EXE do Core, configuração de usuários ou dados de pareamento. O conteúdo publicado em GitHub Pages e no repositório público ficará acessível por terceiros.

A Store apresentada no Android é implementada pelo **Core original**, não por esta página. O download das extensões é realizado pelo Core, com conferência de integridade e assinaturas.

**Estado:** repositório inicializado; os arquivos da Store precisam ser enviados e conferidos antes de configurar o Core para o endereço público.
