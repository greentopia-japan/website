# greentopia.jp

The Greentopia Japan website in English and Japanese (`/ja/`): plain HTML, CSS and JavaScript. Netlify publishes this folder as-is, with no build step on Netlify.

- Every push to `main` deploys to the live site. Batch your edits, since each production deploy uses Netlify credits.
- Contact form submissions go to Netlify Forms (Netlify dashboard → Forms).
- Photos in `images/` are web-sized copies. The full-size originals stay in Google Drive.

## How the pages are made

The pages are generated. Don't hand-edit the `.html` files, because the next build overwrites them.

- `_build/src/v13zip/`: the original v13 prototype pages
- `_build/tools/build.py`: all edits applied on top of v13 (content fixes, photos, Camps page, pricing)
- `_build/tools/i18n.py`: builds the Japanese pages from the English ones, plus the language switcher
- `_build/src/i18n/ja.tsv`: Japanese translations (`id ||| Japanese`). The build stops if any English text has no translation.
- `_build/tools/images.py`: resizes photos from Google Drive into `images/` (needs the Drive folders staged)

Rebuild from the repo root:

    python3 -I _build/tools/build.py _build/src/v13zip .

`_build/` is blocked from public access by `_redirects`.
