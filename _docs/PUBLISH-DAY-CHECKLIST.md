# Publish-day checklist for Resources articles

This file is for El. It is not served on the website: Jekyll skips folders that start with `_`. The repo is public, though, so anyone can read it on GitHub.

An article goes live only when **both** of these are true in `_resources/manifest.json`:
- its `releaseDate` has arrived (UTC);
- `vetted` is `true`.

**Only El sets `vetted` to `true`.** Before doing that for an article, confirm that every claim listed for it below is true on the day.

## Claims El confirms are true on the day of release

### Computer-vision claims (flagged specifically, keep the text as written)
- [ ] **03** "Populos scores every board on a single rating built from field-verified and computer-vision-checked factors of run-up, situation, visibility, angle, size, condition, illumination and the competitive clutter around it."
- [ ] **06** "volatile ones like condition, competitive clutter are re-checked on every field visit and verified by computer vision."
- [ ] **06** "The strongest approach combines trained field observation with computer-vision verification…" (a general statement, sitting next to the Populos claims).
- [ ] **10** "Field data is captured under controlled conditions and cross-checked by computer vision, with the firm rule that automated systems flag and recommend while humans decide and every change is logged."
- [ ] **10, figure 1** says "Computer vision spots issues at scale". That image is held and not in the repo; check it again if it is ever released.

### Other claims about Populos
- [ ] **01** "Populos is built to those same reference points." "Populos treats pedestrian traffic intensity, vehicular traffic intensity and the specific dynamics of transit points as first-class parts of the model."
- [ ] **02** "In the Populos model these are not four independent counts but one coherent chain."
- [ ] **04** "Populos models pedestrian traffic intensity and vehicular traffic intensity as distinct streams, each calibrated to Ghanaian data."
- [ ] **05** "Populos builds its socio-economic classification from Ghana's own census microdata and living-standards surveys, calibrated against syndicated audience measures."
- [ ] **06** "Populos rates every board on a single rating… each with transparent, defined scoring bands, versioned and signed off…" and "That single rating is applied once, never twice."
- [ ] **07** "A measurement currency like Populos does not replace marketing mix modelling or brand-lift work."
- [ ] **08** "Populos computes cost efficiency on quality-adjusted, deduplicated audience…". The same paragraph says cost measures are "calculated on a consistent monthly basis", which is a reporting cadence. It also mentions "competitor cost comparisons".
- [ ] **09** "Populos is built deliberately as an agency-agnostic measurement currency." The same paragraph says "Constants and scoring bands are held in a controlled, versioned settings layer with change sign-off". That describes internal method. It also mentions "competitor context… presence-level information".
- [ ] **10** "Populos treats verification and governance as core infrastructure, not paperwork."
- [ ] **All ten articles, "About Populos":** "Ghana's independent, agency-agnostic out-of-home audience measurement and intelligence platform, benchmarked to international standards including the Global Guidelines on OOH Audience Measurement and calibrated to the Ghanaian movement using national census and transport data."

### Sentences El may want to edit (left exactly as in the plain text of record)
- **06**, second section: "It is the operational form of the visibility principle instead of a vague sense that one board is 'better', it produces…". When the original em dash was removed, this became a run-on sentence.
- **02**, worked example: "reaching half of its target audience an average of four times delivers 200 GRPs". This is a textbook example, not a Populos value.
- **07** "Judge an OOH flight in a two-week window, and you will capture only the e…". **This is a window length.** The figure carrying the same "2-week window" was withheld for that reason. 07 also has the narrative example "three weeks later searches the brand".
- **08** "calculated on a consistent monthly basis" is a reporting cadence. "the cost of reaching one percent of your specific target audience" is the standard definition of a reach point.
- **09 and 10** mention that constants, weightings and thresholds exist and are versioned, but give no values.
- **Excerpts over 160 characters**, which are also used as meta descriptions: 01 (184), 04 (162), 05 (178), 09 (181), 10 (183). Search engines will cut them short.

## Images
No source images are in the repo. Every article uses the plain branded cover until El supplies Ghana photos. The list of held and withheld figures is in the pull request that added this file.

## Release mechanics
1. Set `"vetted": true` for the article in `_resources/manifest.json`, via a PR that El approves and merges.
2. The workflow **Release scheduled resources** runs at 05:15 UTC on Tuesdays and Thursdays. It can also be run by hand from the Actions tab: leave **dry_run** ticked to preview, untick it to publish.
3. After a release, check the live page, its card on `/resources/`, and `sitemap.xml`.
