#!/usr/bin/env python3
"""
Sacred Traditions Press site builder — sacredtraditionspress.com

TO ADD A BOOK: add an entry to BOOKS below and re-run.
TO ADD A FORMAT: add it to that book's "buy" list.
TO CHANGE THE SIGNUP: edit FORM_EMBED.
Nothing else needs to change.
"""
import pathlib, json

SITE   = "https://sacredtraditionspress.com/"
PRESS  = "Sacred Traditions Press"
AUTHOR = "Gideon Gray"

AMAZON_STORE = "https://www.amazon.com/stores/Gideon-Gray/author/B0DZWBX2DQ"
FB_GROUP     = "https://www.facebook.com/groups/1303627020652590"
FB_GROUP_NAME= "The Inclusive Word"

# ============================== DATA ==============================

# Each book: clean title (NOT the retail subtitle), blurb, cover file,
# and the buy links in the order they should appear.
BOOKS = [
    {
        "title": "The Ethiopian Bible",
        "cover": "covers/ethiopian-cover.webp",
        "eyebrow": "All 90 books",
        "blurb": ("The Ethiopian Orthodox canon is the oldest and most complete in the world — "
                  "ninety books where most Bibles carry sixty-six. Enoch is here. So are Jubilees, "
                  "Meqabyan and the rest of what the Western canon set aside. Annotated throughout, "
                  "with the historical context for each text."),
        "buy": [
            ("Kindle",    "B0DXJCXS85"),
            ("Hardcover", "B0DXZSK6QY"),
            ("Paperback", "B0DYJXYV5F"),
        ],
    },
    {
        "title": "The Complete Geneva Bible",
        "cover": "covers/geneva-cover.webp",
        "eyebrow": "The complete 1560 text",
        "blurb": ("The English Bible of the Reformation, printed a half-century before the King "
                  "James and carried to America by the Pilgrims. This is the full 1560 text with "
                  "its original marginal notes — the commentary that made it the most "
                  "politically dangerous book of its century."),
        "buy": [
            ("Kindle",    "B0DXK4QDV8"),
            ("Hardcover", "B0DXZX1ZRQ"),
            ("Paperback", "B0DYV29CSS"),
        ],
    },
]

# The free study logbooks, shown beside the signup form.
LOGBOOKS = [
    ("Ethiopian Bible Study Logbook", "covers/ethiopian-logbook.webp"),
    ("Geneva Bible Study Logbook",    "covers/geneva-logbook.webp"),
]

# ===================================================================
#  MailerLite embedded form. Account 1124939, form 18498095.
#  If the form is ever rebuilt in MailerLite the action URL and the
#  success-callback id both change — replace this whole block.
# ===================================================================
FORM_ACTION = "https://assets.mailerlite.com/jsonp/1124939/forms/133955908687365387/subscribe"
FORM_ID     = "18498095"

FORM_EMBED = """      <div id="mlb2-%(fid)s" class="ml-form-embedContainer ml-subscribe-form ml-subscribe-form-%(fid)s">
        <div class="ml-form-embedWrapper embedForm">
          <div class="ml-form-embedBody row-form">
            <form class="ml-block-form" action="%(action)s" data-code="" method="post" target="_blank">
              <label class="sr-only" for="ml-email">Email address</label>
              <input id="ml-email" aria-label="email" aria-required="true" type="email"
                     class="form-control" name="fields[email]" placeholder="Email" autocomplete="email" required>
              <label class="sr-only" for="ml-name">First name</label>
              <input id="ml-name" aria-label="name" type="text"
                     class="form-control" name="fields[name]" placeholder="Name" autocomplete="given-name">
              <input type="hidden" name="ml-submit" value="1">
              <input type="hidden" name="anticsrf" value="true">
              <button type="submit" class="primary">Send me the logbooks</button>
            </form>
          </div>
          <div class="ml-form-successBody row-success" style="display:none">
            <p class="ml-success">Thank you. Your download link will be in your inbox any second now.</p>
          </div>
        </div>
      </div>""" % {"fid": FORM_ID, "action": FORM_ACTION}

# ============================ END DATA ============================


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def amazon(asin):
    return "https://www.amazon.com/dp/" + asin


# ---- book blocks
book_html = []
for b in BOOKS:
    btns = "\n".join(
        '            <a class="btn%s" href="%s" rel="noopener">%s</a>'
        % ("" if i == 0 else " alt", amazon(asin), esc(label))
        for i, (label, asin) in enumerate(b["buy"]))
    book_html.append("""      <article class="book">
        <a class="book-cover" href="%s" rel="noopener" tabindex="-1" aria-hidden="true">
          <img src="%s" width="200" height="259" alt="Cover of %s" loading="lazy">
        </a>
        <div class="book-body">
          <p class="eyebrow">%s</p>
          <h2>%s</h2>
          <p class="blurb">%s</p>
          <div class="btns">
%s
          </div>
        </div>
      </article>""" % (amazon(b["buy"][0][1]), b["cover"], esc(b["title"]),
                       esc(b["eyebrow"]), esc(b["title"]), esc(b["blurb"]), btns))

logbook_html = "\n".join(
    '        <img src="%s" width="165" height="214" alt="Cover of the %s" loading="lazy">'
    % (f, esc(t)) for t, f in LOGBOOKS)

ld = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": PRESS,
    "url": SITE,
    "description": "Publisher of annotated historical Bibles and non-canonical scripture, "
                   "including the Ethiopian Orthodox canon and the 1560 Geneva Bible.",
    "sameAs": [AMAZON_STORE, FB_GROUP],
    "parentOrganization": {"@type": "Organization", "name": "GO Publishing LLC"},
}

CSS = """
*{box-sizing:border-box;}
:root{
  --ground:#101722; --surface:#172030; --raised:#1D2838;
  --ink:#EFE8D9; --muted:#9FAABB; --gold:#C9A75E; --gold-lift:#DCBE78;
  --rule:#2A3647;
}
html{scroll-behavior:smooth;}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"DM Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;}
.site{padding:0 24px;}
.wrap{max-width:1060px;margin:0 auto;}
img{max-width:100%;display:block;}
a{color:inherit;}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px;}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0,0,0,0);white-space:nowrap;border:0;}

.eyebrow{font-size:10.5px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
  color:var(--gold);margin:0 0 14px;}

.masthead{padding-block:76px 48px;border-bottom:1px solid var(--rule);}
h1{font-family:"EB Garamond",Georgia,serif;font-weight:500;
  font-size:clamp(2.6rem,7vw,4.4rem);line-height:1.04;margin:0 0 20px;letter-spacing:-.01em;}
h1 .rule{display:block;width:72px;height:2px;background:var(--gold);margin:22px 0 0;}
.standfirst{font-family:"EB Garamond",Georgia,serif;font-style:italic;
  font-size:clamp(1.15rem,2.4vw,1.5rem);line-height:1.45;margin:0 0 20px;max-width:34ch;color:var(--gold);}
.lede{font-size:16px;line-height:1.8;color:var(--muted);margin:0;max-width:62ch;}
.lede strong{color:var(--ink);font-weight:500;}

.section-head{padding-block:56px 30px;}
.section-head h2{font-family:"EB Garamond",Georgia,serif;font-weight:500;
  font-size:clamp(1.7rem,3.6vw,2.5rem);line-height:1.15;margin:0 0 10px;}
.section-head p{margin:0;color:var(--muted);font-size:15.5px;max-width:58ch;}

.books{display:grid;gap:26px;padding-bottom:12px;}
.book{background:var(--surface);border:1px solid var(--rule);border-radius:6px;
  padding:32px;display:grid;grid-template-columns:200px 1fr;gap:34px;align-items:start;}
.book-cover{display:block;}
.book-cover img{width:200px;height:auto;border-radius:3px;
  box-shadow:0 14px 34px rgba(0,0,0,.55);border:1px solid rgba(201,167,94,.22);
  transition:transform .18s ease;}
.book:hover .book-cover img{transform:translateY(-3px);}
.book-body{min-width:0;}
.book h2{font-family:"EB Garamond",Georgia,serif;font-weight:500;
  font-size:clamp(1.5rem,3vw,2.05rem);line-height:1.12;margin:0 0 14px;}
.blurb{margin:0 0 24px;color:var(--muted);font-size:16px;line-height:1.75;max-width:60ch;}

.btns{display:flex;flex-wrap:wrap;gap:9px;}
.btn{display:inline-block;text-decoration:none;font-size:11.5px;font-weight:700;
  letter-spacing:.13em;text-transform:uppercase;padding:11px 19px;border-radius:3px;
  background:var(--gold);color:#101722;border:1px solid var(--gold);
  transition:background .16s ease,border-color .16s ease,color .16s ease;}
.btn:hover{background:var(--gold-lift);border-color:var(--gold-lift);}
.btn.alt{background:transparent;color:var(--ink);border-color:var(--rule);}
.btn.alt:hover{border-color:var(--gold);color:var(--gold);}

.signup{display:grid;grid-template-columns:1fr;gap:34px;align-items:center;
  background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:34px;}
.logbooks{display:flex;gap:16px;justify-content:flex-start;}
.logbooks img{width:165px;height:auto;border-radius:3px;
  box-shadow:0 14px 34px rgba(0,0,0,.55);border:1px solid rgba(201,167,94,.22);}
.signup-body h2{font-family:"EB Garamond",Georgia,serif;font-weight:500;
  font-size:clamp(1.5rem,3vw,2.05rem);line-height:1.15;margin:0 0 14px;}
.signup-body > p{font-size:15.5px;line-height:1.75;color:var(--muted);margin:0 0 24px;max-width:50ch;}

.ml-block-form{display:flex;flex-wrap:wrap;gap:9px;align-items:center;max-width:560px;margin:0;}
.ml-block-form input[type=email],.ml-block-form input[type=text]{
  flex:1 1 190px;min-width:0;background:var(--raised);border:1px solid var(--rule);
  color:var(--ink);border-radius:3px;padding:12px 13px;font-size:14.5px;
  font-family:inherit;}
.ml-block-form input::placeholder{color:#7D889A;}
.ml-block-form input:focus{border-color:var(--gold);outline:none;}
.ml-block-form button{flex:0 0 auto;cursor:pointer;font-family:inherit;
  font-size:11.5px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
  padding:13px 22px;border-radius:3px;background:var(--gold);color:#101722;
  border:1px solid var(--gold);transition:background .16s ease;}
.ml-block-form button:hover{background:var(--gold-lift);}
.ml-success{color:var(--gold);font-size:15.5px;margin:0;}
.fineprint{margin:16px 0 0;font-size:13px;color:#7D889A;}

footer{border-top:1px solid var(--rule);margin-top:64px;padding-block:40px 72px;}
footer p{margin:0 0 12px;font-size:14px;line-height:1.75;color:var(--muted);max-width:66ch;}
footer p:last-child{margin-bottom:0;}
footer a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--rule);}
footer a:hover{color:var(--gold);border-bottom-color:var(--gold);}

@media (min-width:720px){
  .signup{grid-template-columns:366px 1fr;gap:42px;}
}
@media (max-width:640px){
  .book{grid-template-columns:1fr;gap:22px;}
  .book-cover img{width:150px;}
  .logbooks img{width:132px;}
  .masthead{padding-block:52px 36px;}
  .signup{padding:26px;}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto;}
  .book-cover img,.btn{transition:none;}
  .book:hover .book-cover img{transform:none;}
}
"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sacred Traditions Press — the books of Gideon Gray</title>
<meta name="description" content="Sacred Traditions Press publishes annotated historical Bibles and non-canonical scripture by Gideon Gray — The Ethiopian Bible, all ninety books of the world's oldest canon, and the complete 1560 Geneva Bible.">
<link rel="canonical" href="__SITE__">
<meta property="og:title" content="Sacred Traditions Press — the books of Gideon Gray">
<meta property="og:description" content="Annotated historical Bibles and non-canonical scripture. The Ethiopian Bible and the complete 1560 Geneva Bible.">
<meta property="og:type" content="website">
<meta property="og:url" content="__SITE__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&display=swap">
<style>__CSS__</style>
</head>
<body>
<div class="site">
<div class="wrap">

  <header class="masthead">
    <p class="eyebrow">A GO Publishing LLC imprint</p>
    <h1>Sacred Traditions<br>Press<span class="rule"></span></h1>
    <p class="standfirst">A safe place to read the scriptures that got left out.</p>
    <p class="lede">We publish annotated editions of historical Bibles and the texts outside the
    Western canon, written by <strong>Gideon Gray</strong>. The aim is context, not conversion —
    where a book came from, who kept it, why it was set aside, and what it actually says.
    No agenda beyond the history and the fascination.</p>
  </header>

  <section id="books">
    <div class="section-head">
      <h2>The books</h2>
      <p>Each available in Kindle, hardcover and paperback.</p>
    </div>
    <div class="books">
__BOOKS__
    </div>
  </section>

  <section id="logbooks">
    <div class="section-head">
      <h2>Free study logbooks</h2>
      <p>Fifty-two printable pages for each volume — chapter summaries, key characters,
      key verses and notes, so a long read stays a structured one.</p>
    </div>
    <div class="signup">
      <div class="logbooks">
__LOGBOOKS__
      </div>
      <div class="signup-body">
        <h2>Systematically plan your reading</h2>
        <p>Join the list and we will send them over, along with the weekly devotional
        and word of anything new from the press.</p>
__FORM__
        <p class="fineprint">One email a week. Unsubscribe whenever you like.</p>
      </div>
    </div>
  </section>

  <footer>
    <p>Every title is available on Kindle, in hardcover and in paperback.
    Browse them all at the <a href="__STORE__" rel="noopener">Gideon Gray author store</a>.</p>
    <p>Nothing here is offered as religious instruction or as a statement of doctrine.
    These are historical texts, published with their context.</p>
    <p>Readers gather in <a href="__FBGROUP__" rel="noopener">__FBNAME__</a>, our group for
    devotionals and prayers beyond the canon.</p>
    <p>Published by GO Publishing LLC.</p>
  </footer>

</div>
</div>

<script>
  function ml_webform_success___FID__() {
    var $ = window.ml_jQuery || window.jQuery;
    if (!$) return;
    $('.ml-subscribe-form-__FID__ .row-success').show();
    $('.ml-subscribe-form-__FID__ .row-form').hide();
  }
</script>
<script src="https://groot.mailerlite.com/js/w/webforms.min.js?v2d8fb22bb5b3677f161552cd9e774127" type="text/javascript"></script>
<script>fetch("https://assets.mailerlite.com/jsonp/1124939/forms/133955908687365387/takel")</script>

<script type="application/ld+json">
__LD__
</script>
</body>
</html>
"""

html = (PAGE
        .replace("__CSS__", CSS.strip())
        .replace("__BOOKS__", "\n".join(book_html))
        .replace("__LOGBOOKS__", logbook_html)
        .replace("__FORM__", FORM_EMBED)
        .replace("__SITE__", SITE)
        .replace("__STORE__", AMAZON_STORE)
        .replace("__FBGROUP__", FB_GROUP)
        .replace("__FBNAME__", FB_GROUP_NAME)
        .replace("__FID__", FORM_ID)
        .replace("__LD__", json.dumps(ld, indent=2)))

out = pathlib.Path(__file__).parent / "index.html"
out.write_text(html, encoding="utf-8")
print("wrote %s  (%d books, %d logbooks, %d bytes)"
      % (out, len(BOOKS), len(LOGBOOKS), len(html)))
