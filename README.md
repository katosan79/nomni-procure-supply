# Procure & Supply website (staging)

Staging build of the new Procure and Supply site. It replaces zeemart.co and uses the Nomni Design System v1.6.0 colours and fonts.

- The **live staging site** is served by GitHub Pages from the `docs/` folder on `main`.
- **Copy and sitemap:** see the "Procure & Supply website rebuild — sitemap and copy" doc in the Zeemart 2.0 Claude project.
- **Search engines:** every page carries `noindex, nofollow`. Remove the tag before the production launch.

## Editing

1. Edit a page in `src/pages/`, or the styles and scripts in `src/assets/`.
2. Run `python3 build.py`. It wraps each page in the shared header and footer and writes the output to `docs/`.
3. Commit and push both `src/` and `docs/`.

Each page starts with a header comment:

```
<!-- title: Page title | desc: Meta description | nav: procure -->
```

## Status labels

Each feature carries one of these pills:

| Pill | Meaning |
|---|---|
| `pill-live` | Live |
| `pill-soon` | Coming soon |
| `pill-rolling` | Rolling out (HQ) |
| `pill-tbc` | Status, number or permission still to confirm. Remove every one of these before launch. |

## Before launch

- [ ] Confirm the status of each agent, starting with the Invoice Agent.
- [ ] Get re-confirmed permission for the TamJai SamGor and Better Craft Co. quotes, and re-verify the "150k+ orders" figure.
- [ ] Approve pricing. Supply pricing is still undecided.
- [ ] Confirm EDGE pre-approval, and confirm whether MYOB is live.
- [ ] Swap the Fern and Spring hex values for the exact Design System tokens.
- [ ] Connect the forms to signup and the CRM, and link Log in.
- [ ] Remove the staging banner and the noindex tag.
