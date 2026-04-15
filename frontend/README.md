# rafaelortiz.dev

Personal portfolio and case studies site for Rafael Ortiz — Data Engineer.

## Stack

- **Astro 6** — static site generation with i18n routing (ES/EN)
- **React 19** — interactive SVG visualizations (StreamingPipeline, MatViewChain, etc.)
- **Tailwind CSS 4** — utility-first styling with CSS custom properties
- **MDX** — case study content with embedded components

## Development

```sh
npm install
npm run dev       # localhost:4321
npm run build     # production build → dist/
```

## Content

- `src/content/case-studies/` — MDX case studies with frontmatter (bilingual)
- `src/views/` — page layouts (HomePage, AboutPage, CaseStudiesPage, etc.)
- `src/components/visuals/` — React SVG diagrams for case studies
- `src/lib/api.ts` — fetches profile/experience/projects from api.rafaelortiz.dev
- `src/lib/i18n.ts` — i18n helpers with ES/EN locale support
