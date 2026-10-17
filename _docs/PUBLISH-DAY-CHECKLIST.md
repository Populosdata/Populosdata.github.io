# Publish-day checklist for Resources articles

This file is for El. It is not served on the website: Jekyll skips folders that start with `_`. The repo is public, though, so anyone can read it on GitHub. For that reason it doesn't quote any wording that was removed from the articles.

Articles have no fixed release date. They go out in their planned `order` in `_resources/manifest.json`, **one per scheduled run at most**. An article is released only when **both** of these are true:
- `vetted` is `true`;
- it is the lowest planned order number not yet released.

If the next article in order is not vetted, nothing is released, even if a later article is vetted. At most one article is released per calendar day (UTC); a second run on the same day does nothing and says so in its log. The public date is the day of release, which the release stamps into `releasedOn`. To change the planned order, see `_docs/RESOURCES-HOWTO.md`.

**Only El sets `vetted` to `true`.** Before doing that for an article, confirm the items below for it.

## Wording held outside the repo (re-approve before restoring)
Some lines were removed or replaced with neutral wording before merge. The originals, with article and line, are in a restore file that El holds outside this repository. It isn't committed here, because the repo is public. To restore a line, El re-approves it, then it goes back in through a PR.

| Article | What was neutralised |
|---|---|
| 02 | Example audience figures in "Reach: the unduplicated crowd" |
| 03 | A computer-vision claim, the named rating factors, and the inline factor list |
| 04 | Two modelling terms in the transit and vehicular sections; "capital cities" corrected to "major cities" |
| 06 | Computer-vision claims (a section heading and two sentences), and the named rating factors |
| 07 | A specific measurement-window length |
| 08 | A reporting cadence, and a competitor-comparison sentence |
| 09 | A description of how the rules are stored internally |
| 10 | A computer-vision claim, and the description of how constants are stored (one section and one sentence) |

## Claims El confirms are true before vetting (listed in planned order)
- [ ] **01** "Populos is built to those same reference points." "Populos treats pedestrian traffic intensity, vehicular traffic intensity and the specific dynamics of transit points as first-class parts of the model."
- [ ] **02** "In the Populos model these are not four independent counts but one coherent chain."
- [ ] **03** "Populos scores every board on a single rating built from a set of physical and positional factors, each verified in the field."
- [ ] **04** "Populos models pedestrian traffic intensity and vehicular traffic intensity as distinct streams, each calibrated to Ghanaian data."
- [ ] **05** "Populos builds its socio-economic classification from Ghana's own census microdata and living-standards surveys, calibrated against syndicated audience measures."
- [ ] **06** "Populos rates every board on a single rating… each with transparent, defined scoring bands, versioned and signed off…" and "That single rating is applied once, never twice."
- [ ] **07** "A measurement currency like Populos does not replace marketing mix modelling or brand-lift work."
- [ ] **08** "Populos computes cost efficiency on quality-adjusted, deduplicated audience…"
- [ ] **09** "Populos is built deliberately as an agency-agnostic measurement currency." "Changes to the rules are versioned and signed off…"
- [ ] **10** "Populos treats verification and governance as core infrastructure, not paperwork." "Field data is captured under controlled conditions and cross-checked…"
- [ ] **All ten articles, "About Populos":** "Ghana's independent, agency-agnostic out-of-home audience measurement and intelligence platform, benchmarked to international standards including the Global Guidelines on OOH Audience Measurement and calibrated to the Ghanaian movement using national census and transport data."

## Images
No source images are in the repo. Every article uses the plain branded cover until El supplies Ghana photos. The list of held and withheld figures is in PR #8.

## Release mechanics
1. Set `"vetted": true` for the article in `_resources/manifest.json`, via a PR that El approves and merges.
2. The workflow **Release scheduled resources** runs at 05:15 UTC on Tuesdays and Thursdays. At each run it releases the next article in order, if that article is vetted. It can also be run by hand from the Actions tab: leave **dry_run** ticked to preview, untick it to publish.
3. After a release, check the live page, its card on `/resources/`, and `sitemap.xml`. All three should show the day of release.
