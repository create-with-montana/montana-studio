# Montana Studio

The website for Montana Studio, a brand management studio.

It is a plain static site with no build step: `index.html`, `styles.css` and the `images/` folder.

## Preview locally

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deploy

The site is deployed with Vercel. Import this repository in Vercel and keep the defaults: framework preset "Other", no build command, output directory set to the repository root. Every push to `main` deploys to production. Every pull request gets its own preview link.

## Editing

- Colours and fonts are set as variables at the top of `styles.css`.
- Each homepage section is a commented block in both `index.html` and `styles.css`, so it can be refined one section at a time.
- Photos live in `images/`. Keep the long edge at 2200px or less.
