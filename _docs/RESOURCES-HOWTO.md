# How to add a Resources post

Use these steps to turn a pasted article into a post on https://www.populosdata.com/resources/.

1. **Start a branch from `origin/main`.**
   `git fetch origin && git checkout -b post/<slug> origin/main`
   The slug is lowercase words joined by hyphens, for example `ooh-in-accra`.

2. **Copy the template.**
   `cp resources/_template.html resources/<slug>.html`
   Never edit or link `_template.html` itself. GitHub Pages does not publish files that start with `_`.

3. **Fill in every `REPLACE` value in `resources/<slug>.html`.**
   - `<title>` and `og:title`: `Post title | Populos`.
   - `meta description` and `og:description`: the same sentence, 120 to 155 characters, different from every other page.
   - `canonical` and `og:url`: `https://www.populosdata.com/resources/<slug>.html`.
   - `article:published_time` and the `<time datetime>`: `YYYY-MM-DD`. The visible date is written like `17 October 2026`.
   - `<h1>`: the post title. Keep exactly one `<h1>`.
   - The body goes inside `<div class="post-body">`, using `<h2>` for sections and `<p>` for paragraphs.
   - Delete the `<meta name="robots" content="noindex">` line and the two comment lines above it.
   - Search the file for `REPLACE`. There must be no matches left.

4. **Add the post to `resources/index.html`.**
   Copy the existing `<li>` block and put the new one **first** in the `<ul class="post-list">`, because the list is newest first. Set the link to `/resources/<slug>.html`, the date, the title, and a one-line summary.

5. **Add the post to `sitemap.xml`.**
   Add a `<url>` with `<loc>https://www.populosdata.com/resources/<slug>.html</loc>` and `<lastmod>YYYY-MM-DD</lastmod>`. Also update the `/resources/` entry's `<lastmod>`.
   Do not add `_template.html`. Do not add `welcome.html` while it is still the placeholder.

6. **Retire the placeholder** when the first real post goes in. Delete `resources/welcome.html` and its `<li>` from `resources/index.html`.

7. **Check before committing.**
   - Serve the site locally: `python -m http.server 8000`.
   - Open `/resources/` and the new post. Check there is one title, one H1 and one canonical, and that the description is 120 to 155 characters.
   - Make sure the page doesn't scroll sideways at 390px wide.
   - Confirm `sitemap.xml` still parses as XML.

8. **Commit only the files you changed, then open a PR.**
   `git add -- resources/<slug>.html resources/index.html sitemap.xml`
   `git commit -m "Add post: <title>" -- resources/<slug>.html resources/index.html sitemap.xml`
   `git push -u origin post/<slug>`, then open a PR to `main`. Do not merge until the PR has been reviewed.

**Content rules:** marketing copy only. Do not describe how measurement works: no formulas, constants, thresholds or scoring details. Do not add claims that haven't been approved.
