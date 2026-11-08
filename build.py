"""Build the static website portfolio. Run with Python 3; no dependencies needed."""
from pathlib import Path
import shutil
import json
from html import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
(OUT / 'assets').mkdir(exist_ok=True)
for name in ('site.css', 'site.js'):
    shutil.copyfile(ROOT / 'src' / name, OUT / 'assets' / name)

NAV = [('', 'Startseite'), ('pensionsstall', 'Pensionsstall'), ('reitschule', 'Reitschule'), ('ausbildung', 'Ausbildung'), ('ueber-uns', 'Über uns'), ('kontakt', 'Kontakt')]
ALIASES = {'anlage-und-weiden': 'pensionsstall', 'team': 'ueber-uns'}
IMAGES = set()
current = ''

def url(path=''):
    return ('../' if current else './') + path

def image(name, alt, eager=False, position=None):
    IMAGES.add(name)
    style = f' style="object-position:{position}"' if position else ''
    priority = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return f'<img src="{url("assets/" + name + ".jpeg")}" alt="{escape(alt)}" {priority} decoding="async"{style}>'

# Display-only crops remove screenshot borders; original JPEG bytes stay intact.
PHOTO_FRAMES = {
    'reiterin-mit-pferd-im-bach': (736, 1600, 310, 1290),
    'pensionsstall-anbindeplaetze-am-hof': (736, 1600, 310, 1291),
    'stallgemeinschaft-feier-mit-blumen': (900, 1600, 500, 1138),
    'aussenreitplatz-uebersicht-01': (942, 2048, 670, 1378),
    'pensionsstall-reitplatz-bewaesserung': (736, 1600, 524, 1076),
    'pensionsstall-reitplatz-herbstblick': (1600, 1200, 0, 1200),

    'pensionsstall-paddockboxen': (736, 1600, 309, 1291),
    'pensionsstall-aussenpaddocks': (942, 2048, 628, 1421),
    'stallgasse-mit-boxen': (942, 2048, 395, 1653),
    'aussenreitplatz-panorama': (942, 2048, 593, 1454),
    'longierhalle-innenansicht': (2048, 1536, 0, 1536),
    'waschbox-innenansicht': (942, 2048, 395, 1653),
    'pferdelaufband-ueberdacht': (2048, 1536, 0, 1536),
    'paddocks-entlang-des-hofwegs': (944, 2048, 391, 1656),
    'pensionsstall-unterstand-mit-einstreu': (736, 1600, 524, 1076),
    'pensionsstall-waldweg-vom-pferd': (1200, 1600, 0, 1600),
    'pensionsstall-pferde-auf-sommerweide': (1600, 1200, 0, 1200),
    'pensionsstall-reithalle-lichtdurchflutet': (738, 1600, 523, 1077),
    'pensionsstall-rundes-holzgebaeude': (1600, 1200, 0, 1200),
    'pensionsstall-sandauslauf-mit-unterstand': (1600, 1200, 0, 1200),
    'pensionsstall-solebox-bauphase': (736, 1600, 309, 1291),

    'reiterin-auf-pferd-mit-turnierschleife': (738, 1600, 100, 1600),
    'dressurreiten-vor-zuschauern': (1179, 774, 8, 774),
    'gruppenfoto-drei-personen': (736, 1600, 332, 1214),
    'springreiten-schimmel-ueber-hindernis': (736, 1600, 0, 1574),
    'springtraining-auf-aussenplatz': (736, 1600, 108, 1493),
}

def photo_frame(name, alt, width, height, eager=False):
    width, height, top, bottom = PHOTO_FRAMES.get(name, (width, height, 0, height))
    visible = bottom - top
    return f'<div class="photo-frame" style="aspect-ratio:{width}/{visible};--photo-top:{-100*top/visible:.4f}%;--photo-height:{100*height/visible:.4f}%">{image(name,alt,eager)}</div>'

def training_photos():
    photos = [
        ('stallgemeinschaft-gemeinsam-mit-pferden','Zwei Reiterinnen in Turnierkleidung mit einem dunklen Pferd und einem Schimmel',1200,1600),
        ('reitturnier-pferde-mit-schleifen','Zwei Reiterinnen mit Pferden und Schleifen in einer Reithalle',792,1056),
        ('springreiten-schimmel-ueber-hindernis','Reiter auf einem Schimmel über einem bunten Hindernis',736,1600),
        ('schimmel-mit-schleife-in-reithalle','Reiterin auf einem Schimmel mit Decke und gelber Schleife in der Halle',777,1600),
        ('springtraining-auf-aussenplatz','Pferd und Reiter beim Sprung auf einem sandigen Außenplatz',736,1600),
        ('reiterin-mit-schleifenpferd-auf-wiese','Reiterin auf einem dunklen Pferd mit Schleife auf einer Wiese',1200,1600),
        ('springreiten-braunes-pferd-im-parcours','Reiter und braunes Pferd über einem Hindernis im Parcours',640,640),
        ('reitturnier-collage-dressur-und-schleife','Zwei Fotos: Dressurreiten und ein Pferd mit Reiterin, Decke und Schleife',1440,1440),
        ('reiterin-mit-pferd-und-roter-decke','Reiterin mit Rose neben einem dunklen Pferd mit roter Decke',1200,1600),
        ('reiterin-auf-pferd-mit-turnierschleife','Reiterin auf einem dunklen Pferd mit blauer Decke und Turnierschleife',738,1600),
        ('dressurreiten-vor-zuschauern','Reiterin auf einem braunen Pferd beim Dressurreiten vor Zuschauern',1179,774),
        ('turnier-reiterin-mit-begleitung-und-braunem-pferd','Reiterin in Turnierkleidung auf einem braunen Pferd mit einer Begleitperson auf dem Turniergelände',768,1024),
        ('ausritt-reiterin-auf-haflinger','Reiterin mit Helm auf einem Haflinger auf einer von Bäumen gesäumten Straße',1200,1600),
    ]
    figures = ''.join(f'<figure>{photo_frame(name,alt,w,h)}</figure>' for name,alt,w,h in photos)
    return f'<section class="wrap section" id="einblicke"><div class="training-gallery-head"><p class="eyebrow">Dressur, Springen &amp; Turniermomente</p><h2>Pferd und Reiter in Bewegung.</h2></div><div class="training-photos">{figures}</div></section>'

def link(path, text, kind='text-link'):
    return f'<a class="{kind}" href="{url(path)}">{text}<span aria-hidden="true">↗</span></a>'

def brand():
    return f'''<a class="brand" href="{url()}" aria-label="Reiterhof Georg – Startseite"><svg class="brand-mark" viewBox="0 0 40 50" aria-hidden="true"><path d="M6 44V19C6 1 34 1 34 19v25M10 44V20C10 7 30 7 30 20v24M6 44h7m14 0h7M16 35V24l-3-3 5-9 4 5 6 3-2 5h-5v10"/></svg><span class="brand-name"><span class="brand-small">REITERHOF</span>Georg</span></a>'''

def header():
    links = ''.join(f'<a href="{url(slug + "/" if slug else "")}"'+(' aria-current="page"' if ALIASES.get(current, current) == slug else '')+f'>{label}</a>' for slug, label in NAV)
    return f'''<a class="skip" href="#inhalt">Zum Inhalt springen</a><header class="header"><div class="wrap header-inner">{brand()}<a class="mobile-contact" href="{url('kontakt/')}">Kontakt</a><button class="menu-button" type="button" aria-expanded="false" aria-controls="navigation">Menü ☰</button><nav class="nav" id="navigation" aria-label="Hauptnavigation">{links}</nav></div></header>'''

def footer():
    return f'''<footer class="footer"><div class="wrap"><div class="footer-top"><div>{brand()}<p class="footer-description">Pferde. Menschen. Ein Ort zum Ankommen.</p></div><div class="footer-links"><div>{''.join(f'<a href="{url(s + "/" if s else "")}">{t}</a>' for s,t in NAV[1:3])}</div><div>{''.join(f'<a href="{url(s + "/")}">{t}</a>' for s,t in NAV[3:])}</div></div></div><div class="footer-bottom"><span>© 2026 Reiterhof Georg</span><span><a href="{url('impressum/')}">Impressum</a> &nbsp; / &nbsp; <a href="{url('datenschutz/')}">Datenschutz</a></span></div></div></footer>'''

def cta(title='Den Hof persönlich kennenlernen.', action='Besichtigung anfragen'):
    return f'<section class="cta"><div class="wrap"><div><p class="eyebrow">Wir freuen uns auf Ihre Anfrage</p><h2>{title}</h2></div>{link("kontakt/",action,"button")}</div></section>'

def pagehead(kicker, title, text):
    return f'<div class="wrap page-head"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lead">{text}</p></div>'

def subnav(items):
    return '<nav class="subnav wrap" aria-label="Abschnitte dieser Seite">'+''.join(f'<a href="#{slug}">{label}</a>' for slug,label in items)+'</nav>'

def gallery_photos(photos, framed=False, uniform=False):
    figures = []
    for name, caption, alt in photos:
        if framed or name in PHOTO_FRAMES:
            width, height, _, _ = PHOTO_FRAMES[name]
            picture = photo_frame(name, alt, width, height)
            if uniform:
                picture = f'<div class="image">{picture}</div>'
        else:
            picture = f'<div class="image">{image(name,alt)}</div>'
        figures.append(f'<figure>{picture}<figcaption>{caption}</figcaption></figure>')
    return '<div class="gallery-grid">' + ''.join(figures) + '</div>'

def gallery(ident, kicker, title, text, photos, framed=False):
    return f'<section class="gallery-section" id="{ident}"><div class="gallery-head"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2></div><p>{text}</p></div>{gallery_photos(photos, framed, uniform=ident == 'hofleben')}</section>'


def home():
    features = [
        ('01', 'Pensionsstall', 'pensionsstall-paddockboxen', 'Paddockboxen mit einzeln eingezäunten Ausläufen vor den Boxentüren', 'Haltungsformen, Reitanlage und Versorgung: Finden Sie einen passenden Platz für Ihr Pferd.', 'pensionsstall/'),
        ('02', 'Reitschule', 'reitschule-reitgruppe-in-der-halle', 'Drei Reiterinnen mit ihren Pferden in der Reithalle', 'Unterricht auf unseren Reitschulpferden. Besprechen Sie mit uns Ihren Einstieg und Ihre Wünsche.', 'reitschule/'),
        ('03', 'Ausbildung', 'aussenreitplatz-panorama', 'Der Außenreitplatz des Hofs', 'Dressur- und Springunterricht für ambitionierte Freizeitreiter – mit Blick auf Pferd und Reiter.', 'ausbildung/')]
    cards = ''.join(f'<article><a class="feature-photo" href="{url(target)}" aria-label="{title} entdecken">{image(img,alt)}</a><div class="feature-body"><p class="number">{n} / UNSERE ANGEBOTE</p><h3>{title}</h3><p>{text}</p>{link(target,"Mehr erfahren")}</div></article>' for n,title,img,alt,text,target in features)
    return f'''<section class="hero">{image('hofzufahrt-mit-stallgebaeude','Hofzufahrt und Stallgebäude des Reiterhofs Georg',True)}<div class="wrap hero-content"><p class="eyebrow">Willkommen in Hofheim-Lorsbach</p><h1>Reiterhof Georg.<br>Für Pferd und Mensch.</h1><p>Familiengeführt. Landwirtschaftlich verwurzelt.<br>Mit Leidenschaft für Pferde.</p><div class="hero-actions">{link('pensionsstall/','Pensionsstall entdecken','button')}{link('kontakt/','Kontakt aufnehmen')}</div></div><span class="hero-foot">Pensionsstall · Reitschule · Ausbildung</span></section>
    <section class="wrap intro" id="hof"><div><p class="eyebrow">Familienbetrieb &amp; Landwirtschaft</p><h2>Mit dem Hof<br>verbunden.</h2></div><p>Als familiengeführter Reiterhof mit eigenem landwirtschaftlichem Betrieb verbinden wir die Liebe zu Pferden mit der täglichen Arbeit in der Landwirtschaft. Unser Heu und Stroh produzieren wir selbst. Verschiedene Haltungsformen, unsere Reitanlage und der Unterricht schaffen Raum für Pferd und Reiter.</p></section>
    <section class="harvest"><div class="wrap harvest-inner"><p class="eyebrow">Aus eigener Erzeugung</p><h2>Unser Heu.<br>Unser Stroh.</h2><div><p>Die eigene Heu- und Stroherzeugung ist ein fester Teil unseres Hofalltags. So gehören Landwirtschaft und Pferdehaltung bei uns zusammen.</p>{link('ueber-uns/#landwirtschaft','Unsere Landwirtschaft kennenlernen')}</div></div></section>
    <section class="wrap overview offers"><div class="section-head"><div><p class="eyebrow">Drei Wege zu uns</p><h2>Was führt Sie auf den Hof?</h2></div></div><div class="feature-grid">{cards}</div></section>
    <section class="wrap gallery-section" id="hofleben"><div class="gallery-head"><div><p class="eyebrow">Einblicke ins Hofleben</p><h2>Ein Eindruck von unserem Alltag.</h2></div><p>Auf der Weide, auf dem Reitplatz und am Wasser: Entdecken Sie die unterschiedlichen Seiten unseres Hoflebens.</p></div>{gallery_photos([('pferd-auf-sommerweide','Sommer auf der Weide','Ein Pferd grast auf einer grünen Weide'),('pensionsstall-reitplatz-herbstblick','Draußen reiten','Außenreitplatz mit herbstlichen Bäumen im Hintergrund'),('reiterin-mit-pferd-im-bach','Mit dem Pferd im Bach','Reiterin auf einem dunklen Pferd in einem von Bäumen gesäumten Bach')], uniform=True)}<div class="trail-section" id="ausreitgelaende"><div class="gallery-head"><div><p class="eyebrow">Direkt vor dem Hoftor</p><h3>Ausreitgelände<br>an den Ausläufern des Taunus.</h3></div><p>Unser Ausreitgelände beginnt direkt vor dem Hoftor. Waldwege und viel Natur an den Ausläufern des Taunus bieten Raum für gemeinsame Ausritte und eine abwechslungsreiche Zeit mit dem Pferd.</p></div>{gallery_photos([('ausritt-reiterin-auf-waldweg-im-taunus','Unterwegs im Taunus','Reiterin auf einem dunklen Pferd auf einem grünen Waldweg'),('ausritt-waldweg-aus-dem-sattel','Der Blick aus dem Sattel','Blick zwischen Pferdeohren auf einen Waldweg'),('reitschule-ausritt-im-sommerwald','Gemeinsam ins Grüne','Pferde und Reiter auf einem sonnigen Waldweg')], uniform=True)}</div></section>
    <section class="wrap personal people-intro"><figure>{photo_frame('gruppenfoto-drei-personen','Drei Personen stehen gemeinsam für ein Gruppenfoto',736,1600)}</figure><div><p class="eyebrow">Über uns</p><h2>Ein Hof lebt von<br>seinen Menschen.</h2><p>Familienbetrieb, Landwirtschaft und die gemeinsame Zeit mit Pferden prägen unseren Hof. Lernen Sie uns persönlich kennen.</p>{link('ueber-uns/','Mehr über uns')}</div></section>{cta()}'''

def facilities():
    forms = ['Innenboxen', 'Außenboxen', 'Fensterboxen', 'Paddockboxen', 'Mini-Offenställe']
    form_cards = ''.join(f'<li><span class="number">0{i}</span><h3>{name}</h3></li>' for i,name in enumerate(forms,1))
    body = pagehead('Pensionsstall','Ein Platz fürs Pferd.<br>Ein Hof zum Ankommen.','Entdecken Sie unsere Haltungsformen, Reitflächen und die Versorgung am Hof. Welche Unterbringung zu Ihrem Pferd passt, besprechen wir gerne persönlich.')
    body += subnav([('haltungsformen','Haltungsformen'),('reiten','Reitanlage'),('versorgung','Ausstattung & Versorgung'),('weiden','Weiden & Auslauf'),('anfragen','Pensionsplätze')])
    body += f'''<div class="wrap"><section class="gallery-section" id="haltungsformen"><div class="gallery-head"><div><p class="eyebrow">01 / Haltungsformen</p><h2>So kann Ihr Pferd<br>bei uns wohnen.</h2></div><p>Innenboxen, Außenboxen, Fensterboxen, Paddockboxen und Mini-Offenställe mit Hütten und Auslauf: Sprechen Sie mit uns über die Unterschiede und die passende Unterbringung. Heu und Stroh stammen aus eigener Erzeugung. Ihr Pferd kann bei uns auf Stroh oder Spänen eingestallt werden. Für Allergiker können wir das Heu nass machen.</p></div><div class="pension-housing" id="stallungen">{gallery_photos([('stallgasse-mit-boxen','Einblick in unsere Stallungen','Stallgasse mit Boxentüren auf beiden Seiten'),('pensionsstall-paddockboxen','Paddockboxen','Paddockboxen mit einzeln eingezäunten Ausläufen vor den Boxentüren'),('pensionsstall-sandauslauf-mit-unterstand','Mini-Offenstall mit Auslauf','Mini-Offenstall mit einer Hütte links im Bild und eingezäuntem Auslauf davor'),('pensionsstall-unterstand-mit-einstreu','Einblick in einen Mini-Offenstall','Hütte eines Mini-Offenstalls mit zwei offenen, eingestreuten Bereichen')], True)}</div><ul class="housing-list">{form_cards}</ul></section>'''
    body += gallery('reiten','02 / Unsere Reitanlage','Raum für Bewegung.','Reithalle, Außenreitplatz und die runde Longierhalle bieten Raum für Unterricht und Training. Wir bieten Unterricht auf Reitschulpferden sowie Dressur- und Springunterricht für ambitionierte Freizeitreiter an.', [('pensionsstall-reithalle-lichtdurchflutet','Reithalle','Helle Reithalle mit Sandboden und Tageslicht unter dem Dach'),('aussenreitplatz-panorama','Außenreitplatz','Sandiger Außenreitplatz vor einer Baumkulisse'),('aussenreitplatz-uebersicht-01','Reitplatz am Waldrand','Sandiger Reitplatz mit weißer Einzäunung vor herbstlichen Bäumen'),('pensionsstall-reitplatz-bewaesserung','Sommer auf dem Reitplatz','Bewässerung des Reitplatzes mit einem Regenbogen im Sprühnebel'),('pensionsstall-reitplatz-herbstblick','Ein weiterer Blick auf den Reitplatz','Reitplatz mit weißer Einzäunung zwischen Bäumen im Herbstlicht'),('longierhalle-innenansicht','Longierhalle','Innenansicht der runden Longierhalle'),('pensionsstall-rundes-holzgebaeude','An der Reitanlage','Rundes Holzgebäude mit offenem Eingang an einem Hofweg'),('reiterin-mit-pferd-im-bach','Mit dem Pferd im Bach','Reiterin auf einem dunklen Pferd in einem von Bäumen gesäumten Bach')], framed=True)
    body += gallery('versorgung','03 / Ausstattung & Versorgung','Was zum Hofalltag gehört.','Waschbox, Solarium und Laufband ergänzen die Anlage. Auf der gepflasterten Fläche am Hof stehen Anbindeplätze zur Verfügung. Die passende Versorgung, den Leistungsumfang und die Nutzung der Ausstattung besprechen wir gerne persönlich.', [('pensionsstall-anbindeplaetze-am-hof','Zusätzliche Anbindeflächen','Gepflasterte Fläche mit Anbindestange unter Bäumen und Stahlgitter im Hintergrund'),('waschbox-innenansicht','Waschbox','Geflieste Waschbox mit Wasserschläuchen'),('pferdelaufband-ueberdacht','Überdachtes Pferdelaufband','Pferdelaufband unter einem Dach'),('pensionsstall-solebox-bauphase','Solebox – Aufnahme aus der Bauphase','Blick in die Solebox während der Bauphase')], framed=True)
    body += gallery('weiden','04 / Weiden & Auslauf','Draußen sein.','Unsere Sommerweiden stehen zum selbstständigen Herausstellen der Pferde zur Verfügung. Die Pferde können auch rund um die Uhr (24/7) auf der Koppel bleiben. Die Weidesaison dauert in der Regel von Mai bis November. Preise auf Anfrage.', [('pensionsstall-pferde-auf-sommerweide','Sommerweide','Zwei Pferde grasen auf einer grünen Weide am Waldrand'),('pensionsstall-waldweg-vom-pferd','Unterwegs in der Umgebung','Blick zwischen Pferdeohren auf einen Waldweg')], framed=True)
    body += f'''<section class="personal pension-outdoor" id="umgebung"><figure>{photo_frame('pensionsstall-aussenpaddocks','Separat eingezäunte Außenpaddocks ohne angeschlossene Boxen',942,2048)}</figure><div><p class="eyebrow">Auslauf direkt am Stall</p><h2>Paddocks &amp;<br>Paddockservice.</h2><p>Unsere Allwetterpaddocks direkt am Stall ermöglichen den Pferden das ganze Jahr über Auslauf im Freien. Unter der Woche bieten wir dafür einen Paddockservice an.</p>{link('kontakt/','Leistungen anfragen')}</div></section><section class="section services" id="anfragen"><div><p class="eyebrow">05 / Pensionsplätze &amp; Anfragen</p><h2>Passt unser Hof<br>zu Ihrem Pferd?</h2></div><div><p>Erzählen Sie uns von Ihrem Pferd, der gewünschten Haltungsform und dem möglichen Einzugstermin. Preise, freie Plätze und den Leistungsumfang klären wir persönlich.</p>{link('kontakt/','Pensionsplatz anfragen','button dark')}</div></section></div>{cta()}'''
    return body

def school_photos(group):
    groups = {
        'partner': [
            ('reitschule-pferd-mit-roter-schleife', 'Braunes gesatteltes Pferd mit einer roten Schleife an der Ohrenhaube', 'Ein Moment vor dem Reiten', 1200, 1600),
            ('reitschule-reiten-auf-geschecktem-pony', 'Junge Reiterin auf einem gescheckten Pony in der Halle', 'Im Sattel', 1200, 1600),
            ('ausritt-reiterin-auf-haflinger', 'Reiterin mit Helm auf einem Haflinger auf einer von Bäumen gesäumten Straße', 'Gemeinsam unterwegs', 1200, 1600),
        ],
        'reiten': [
            ('reitschule-reiten-am-waldrand', 'Reiterin auf einem braunen Pferd auf einem Sandplatz am Waldrand', 'Zeit im Sattel', 1200, 1600),
            ('reitschule-begleitung-in-der-reithalle', 'Person begleitet Pferd und Reiterin in einer hellen Reithalle', 'Mit Begleitung in der Halle', 1600, 777),
        ],
        'unterwegs': [
            ('reitschule-ausritt-auf-waldweg', 'Reitgruppe auf einem Waldweg zwischen unbelaubten Bäumen', 'Unterwegs im Wald', 1200, 1600),
            ('reitschule-ausritt-im-sommerwald', 'Mehrere Pferde und Reiter auf einem sonnigen Waldweg', 'Gemeinsam ins Grüne', 1200, 1600),
            ('reitschule-reitgruppe-auf-waldweg', 'Blick zurück auf eine Reitgruppe auf einem grünen Waldweg', 'Zusammen unterwegs', 1200, 1600),
            ('reitschule-pferde-gemeinsam-fuehren', 'Mehrere Personen führen Pferde auf einem Weg am Gebäude', 'Gemeinsam mit den Pferden', 1200, 1600),
        ],
        'umgang': [
            ('reitschule-fuehren-in-der-halle', 'Zwei Personen führen Pferde durch eine Reithalle', 'Auch vom Boden aus', 1600, 1200),
            ('reitschule-geschecktes-pony-in-der-halle', 'Geschecktes Pony wird in der Halle geführt', 'Miteinander vertraut werden', 1600, 1200),
        ],
    }
    return '<div class="school-photos">'+''.join(f'<figure>{photo_frame(name,alt,w,h)}</figure>' for name,alt,caption,w,h in groups[group])+'</div>'

def school():
    return pagehead('Reitschule','Zeit fürs Reiten.<br>Raum zum Lernen.','Wir bieten Unterricht auf Reitschulpferden an. Erzählen Sie uns von Ihrer Erfahrung und Ihren Wünschen – gemeinsam besprechen wir den Einstieg.')+subnav([('unterricht','Unterricht'),('schulpferde','Schulpferde'),('einblicke','Einblicke'),('anmeldung','Anfrage & Kontakt')])+f'''<figure class="wrap training-lead">{photo_frame('reitschule-reitgruppe-in-der-halle','Drei Reiterinnen mit ihren Pferden in der Reithalle',1600,1200,True)}</figure><section class="wrap section services" id="unterricht"><div><p class="eyebrow">01 / Unterricht</p><h2>Jeder Weg<br>beginnt anders.</h2><p class="lead">Ob erste Reiterfahrung oder Wiedereinstieg: Fragen Sie nach den aktuellen Unterrichtsmöglichkeiten auf unseren Schulpferden.</p>{link('kontakt/','Reitunterricht anfragen','button dark')}</div><div><div class="service-row"><span>01</span><div><h3>Von sich erzählen</h3><p>Nennen Sie uns Alter, bisherige Reiterfahrung und Ihre Wünsche.</p></div></div><div class="service-row"><span>02</span><div><h3>Möglichkeiten besprechen</h3><p>Unterrichtsformen, passende Altersgruppen und verfügbare Zeiten stimmen wir persönlich ab.</p></div></div><div class="service-row"><span>03</span><div><h3>Weiterlernen auf dem eigenen Pferd</h3><p>Informationen zur weiteren Ausbildung mit eigenen Pferden finden Sie hier:</p>{link('ausbildung/#training','Zum Training für Pferd &amp; Reiter')}</div></div></div></section><section class="tinted section" id="schulpferde"><div class="wrap"><p class="eyebrow">02 / Unsere Schulpferde</p><h2>Die Partner im Unterricht.</h2><p class="section-copy">Welches Schulpferd und welcher Unterricht zu Ihnen passen, besprechen wir bei Ihrer Anfrage. Hier bekommen Sie erste Einblicke in die gemeinsame Zeit mit unseren Pferden.</p>{school_photos('partner')}</div></section><section class="wrap section school-impressions" id="einblicke"><p class="eyebrow">Einblicke in unsere Reitschule</p><h2>Im Sattel und<br>an der Seite des Pferdes.</h2><p class="section-copy">Momente aus der Halle, bei der Pflege und gemeinsam unterwegs.</p><h3>Beim Reiten</h3>{school_photos('reiten')}<h3>Zeit mit den Pferden</h3>{school_photos('umgang')}<h3>Gemeinsam unterwegs</h3>{school_photos('unterwegs')}<p class="note">Welche Unterrichtsformen und Aktivitäten aktuell möglich sind, besprechen wir gerne persönlich.</p></section><section class="wrap section services" id="anmeldung"><div><p class="eyebrow">03 / Anfrage &amp; Kontakt</p><h2>So fragen Sie<br>Reitunterricht an.</h2></div><div><p>Sie möchten bei uns reiten lernen oder wieder einsteigen? Schreiben Sie uns am besten zunächst per WhatsApp. Nennen Sie uns bitte Ihr Alter, Ihre bisherige Reiterfahrung, Ihre zeitlichen Möglichkeiten und Ihre Wünsche. So können wir Ihre Anfrage gezielt besprechen.</p><p>Sie erreichen uns auch telefonisch. Den weiteren Ablauf stimmen wir persönlich mit Ihnen ab.</p><div class="hero-actions" style="flex-wrap:wrap"><a class="text-link" href="https://wa.me/491772383373">Per WhatsApp schreiben <span aria-hidden="true">↗</span></a></div></div></section>{cta('Lust auf Zeit im Sattel?','Reitunterricht anfragen')}'''

def training():
    return pagehead('Ausbildung','Gemeinsam lernen.<br>Gezielt weiterkommen.','Dressur- und Springunterricht für ambitionierte Freizeitreiter. Sprechen Sie mit uns über Ihren Ausbildungsstand und Ihre Ziele.')+subnav([('training','Training für Pferd & Reiter'),('einblicke','Bilder aus dem Reitsport'),('beritt','Pferdeausbildung & Beritt'),('individuell','Individuelle Anfrage')])+f'''<figure class="wrap training-lead">{photo_frame('dressurreiten-auf-dem-viereck','Reiterin auf einem braunen Pferd beim Dressurreiten im Viereck',1600,1206,True)}</figure><section class="wrap section" id="training"><h2 class="eyebrow">01 / Training für Pferd &amp; Reiter</h2><div><div class="service-row"><span>01</span><div><h3>Dressurunterricht</h3><p>Für ambitionierte Freizeitreiter, die sich im Dressurreiten weiterentwickeln möchten.</p><p>In der Dressur können wir Erfolge bis S** nachweisen, darunter mehrere S-Siege.</p></div></div><div class="service-row"><span>02</span><div><h3>Springunterricht</h3><p>Für ambitionierte Freizeitreiter mit Interesse am Springtraining. Der Springunterricht findet vereinzelt und auf Anfrage statt. Voraussetzungen und passende Möglichkeiten besprechen wir persönlich.</p><p>Im Springen können wir Erfolge bis M** vorweisen.</p></div></div></div></section>{training_photos()}<section class="section tinted" id="beritt"><div class="wrap"><p class="eyebrow">02 / Pferdeausbildung &amp; Beritt</p><h2>Was braucht Ihr Pferd?</h2><p class="section-copy">Sie suchen Unterstützung bei der Ausbildung Ihres Pferdes? Beschreiben Sie uns den bisherigen Ausbildungsstand und Ihre Wünsche.</p></div></section><section class="wrap section services" id="individuell"><div><p class="eyebrow">03 / Individuelle Anfrage</p><h2>Ihre Wünsche.<br>Unser Gespräch.</h2></div><div><p>Teilen Sie uns Ihre Ziele, Ihre Reiterfahrung und die bisherigen Erfahrungen Ihres Pferdes mit. Unterrichtsform, Termine und Preise klären wir direkt mit Ihnen.</p>{link('kontakt/','Ausbildung anfragen','button dark')}</div></section>'''

def community_photos():
    photos = [
        ('hund-in-traktorkabine', 'Kleiner Hund sitzt in der offenen Kabine eines gelben Traktors', 1284, 1600),
        ('stallgemeinschaft-bunter-festwagen', 'Bunt geschmückter Wagen mit Pferdemotiv in der Reithalle', 1600, 1200),
        ('stallgemeinschaft-feier-mit-blumen', 'Drei Personen mit Blumensträußen bei einer gemeinsamen Feier', 900, 1600),
        ('stallgemeinschaft-geschmuecktes-hoffahrzeug', 'Person neben einem geschmückten grünen Hoffahrzeug', 1200, 1600),
        ('stallgemeinschaft-gemeinsam-mit-pferden', 'Zwei Personen in Reitkleidung führen ihre Pferde nebeneinander', 1200, 1600),
    ]
    return '<div class="school-photos">'+''.join(f'<figure>{photo_frame(name,alt,w,h)}</figure>' for name,alt,w,h in photos)+'</div>'

def about():
    return pagehead('Über uns','Familiengeführt.<br>Mit dem Land verbunden.','Pferdehaltung und Landwirtschaft gehören auf dem Reiterhof Georg zusammen. Unser Hof ist Familienbetrieb und ein Ort für die gemeinsame Zeit mit Pferden.')+subnav([('landwirtschaft','Familienbetrieb & Landwirtschaft'),('team','Team'),('stallgemeinschaft','Stallgemeinschaft')])+f'''<div class="wrap wide-image">{image('pensionsstall-pferde-auf-sommerweide','Zwei Pferde grasen auf einer grünen Weide am Waldrand',True)}</div><section class="wrap intro" id="landwirtschaft"><div><p class="eyebrow">01 / Familienbetrieb &amp; Landwirtschaft</p><h2>Unser Heu und Stroh<br>wachsen aus eigener Arbeit.</h2></div><p>Als familiengeführter Reiterhof betreiben wir eine eigene Landwirtschaft. Heu und Stroh produzieren wir selbst. Diese Verbindung prägt unsere tägliche Arbeit – auf den Flächen und im Stall.</p></section><section class="section tinted" id="team"><div class="wrap team-layout"><div><p class="eyebrow">02 / Unser Team</p><h2>Die Menschen hinter dem Hof.</h2><p class="section-copy">Lernen Sie uns bei einem persönlichen Gespräch kennen. Wir beantworten Ihre Fragen zum Stall, zum Unterricht und zum Hofalltag.</p>{link('kontakt/','Kontakt zum Hof')}</div><figure class="team-photo">{photo_frame('gruppenfoto-drei-personen','Drei Personen gemeinsam auf einem Gruppenfoto vom Hof',736,1600)}</figure></div></section><section class="wrap section" id="stallgemeinschaft"><div class="gallery-head"><div><p class="eyebrow">03 / Unsere Stallgemeinschaft</p><h2>Die Freude an Pferden<br>verbindet.</h2></div><p>Gemeinsame Zeit mit den Pferden, Begegnungen im Alltag und besondere Momente am Hof: Unsere Stallgemeinschaft lebt vom Miteinander. Machen Sie sich bei einem Besuch selbst ein Bild.</p></div><figure style="margin:0">{photo_frame('stallgemeinschaft-reitgruppe-in-der-halle','Gemeinsames Gruppenbild mit Pferden und Reitern in der Reithalle',1600,1062)}</figure>{community_photos()}</section>{cta()}'''

def contact():
    return pagehead('Kontakt','Lernen wir uns kennen.','Fragen zur Pferdepension, Interesse am Reitunterricht oder der Wunsch, den Hof zu besichtigen? Wir freuen uns auf Ihre Nachricht.')+f'''<section class="wrap contact-layout"><div><div class="contact-list"><div class="contact-item"><span class="label">Telefon</span><a href="tel:+491772383373">0177 2383373 ↗</a></div><div class="contact-item"><span class="label">Adresse</span><p>Reiterhof Georg<br>Lorsbacher Straße 66c<br>65719 Hofheim am Taunus - Lorsbach</p></div></div><figure class="contact-people"><div class="contact-portrait-crop">{image('gruppenfoto-drei-personen','Lisa Georg-Winstel links und Ralf Georg rechts im gemeinsamen Porträtausschnitt')}</div><figcaption>Lisa Georg-Winstel und Ralf Georg</figcaption></figure></div><aside class="contact-aside"><p class="eyebrow">Ihre Anfrage</p><h2>Worum geht es?</h2><p><strong><a class="topic-link" href="{url('pensionsstall/')}">Pferdepension <span aria-hidden="true">↗</span></a></strong><br>Erzählen Sie uns von Ihrem Pferd und Ihren Wünschen an einen Einstellplatz.</p><p><strong><a class="topic-link" href="{url('reitschule/')}">Reitschule <span aria-hidden="true">↗</span></a></strong><br>Nennen Sie uns Ihre Reiterfahrung und was Sie gerne lernen möchten.</p><p><strong><a class="topic-link" href="{url('ausbildung/')}">Ausbildung <span aria-hidden="true">↗</span></a></strong><br>Beschreiben Sie uns den Ausbildungsstand von Pferd und Reiter und Ihre Ziele.</p><p><strong>Besichtigung</strong><br>Bitte stimmen Sie einen Besuch vorab mit dem Hof ab.</p>{link('pensionsstall/','Vorab die Anlage entdecken')}</aside></section><section class="split tinted"><div class="split-photo">{image('waldweg-am-hof','Grüner Waldweg in der Umgebung des Hofs')}</div><div class="split-copy"><p class="eyebrow">Anfahrt</p><h2>Der Weg zum Hof.</h2><p>Planen Sie Ihre Anfahrt nach Hofheim-Lorsbach mit einem externen Routenplaner.</p><a class="button dark" href="https://www.google.com/maps/dir/?api=1&amp;destination=Lorsbacher+Stra%C3%9Fe+66c+65719+Hofheim" target="_blank" rel="noopener noreferrer">Route planen <span aria-hidden="true">↗</span></a></div></section>'''

def legal(kind):
    if kind=='impressum':
        return pagehead('Reiterhof Georg','Impressum','Angaben zum Betreiber und Kontakt.')+'<div class="wrap legal"><h2>Angaben gemäß § 5 DDG</h2><p>Reiterhof Georg<br>Landwirtschaftlicher Betrieb<br>Lorsbacher Straße 66C<br>65719 Hofheim am Taunus</p><p>Inhaber: Ralf Georg</p><h2>Kontakt</h2><p>Telefon: <a href="tel:+491772383373">0177 2383373</a><br>E-Mail: <a href="mailto:kontakt@reiterhof-georg.de">kontakt@reiterhof-georg.de</a></p></div>'
    return pagehead('Reiterhof Georg','Datenschutz','Informationen zum Umgang mit Ihren personenbezogenen Daten.') + (ROOT / 'src' / 'datenschutz.html').read_text(encoding='utf-8')

PAGES=[('', 'Reiterhof Georg',home),('pensionsstall','Pensionsstall',facilities),('reitschule','Reitschule',school),('ausbildung','Ausbildung',training),('ueber-uns','Über uns',about),('kontakt','Kontakt',contact),('anlage-und-weiden','Pensionsstall',facilities),('team','Über uns',about),('impressum','Impressum',lambda:legal('impressum')),('datenschutz','Datenschutz',lambda:legal('datenschutz'))]
for slug,title,render in PAGES:
    current=slug
    body=render()
    page=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="{escape(title)} – Reiterhof Georg in Hofheim am Taunus. Pensionsstall, Reitschule und Ausbildung."><meta name="theme-color" content="#f7f5ef"><title>{escape(title)}{' | Reiterhof Georg' if slug else ' | Pferde. Menschen. Natur.'}</title><link rel="icon" href="{url('assets/favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{url('assets/site.css')}"><script src="{url('assets/site.js')}" defer></script></head><body>{header()}<main id="inhalt">{body}</main>{footer()}</body></html>'''
    target=OUT/slug
    target.mkdir(exist_ok=True)
    (target/'index.html').write_text(page)
for name in IMAGES:
    shutil.copyfile(ROOT/'src'/'images'/f'{name}.jpeg',OUT/'assets'/f'{name}.jpeg')
(OUT/'assets'/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="8" fill="#f7f5ef"/><text x="24" y="35" text-anchor="middle" font-family="Georgia,serif" font-size="35" fill="#70533d">G</text></svg>')
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
print(json.dumps({'pages':len(PAGES),'images':len(IMAGES),'output':str(OUT)},ensure_ascii=False))
