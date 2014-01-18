from committees.models import Committee


email_committee_map = {
    'itu@mcmun.org': 'itu',
    'unssa@mcmun.org': 'aging',
    'untc@mcmun.org': 'untc',
    'icao@mcmun.org': 'icao',
    'unhrc@mcmun.org': 'unhrc',
    'afdb@mcmun.org': 'afdb',
    'wwf@mcmun.org': 'wwf',
    'efms@mcmun.org': 'food',
    'disney@mcmun.org': 'disney',
    'kitchenaccords@mcmun.org': 'kitchen',
    'bid-uae@mcmun.org': '2020-dubai',
    'bid-prc@mcmun.org': '2020-guangzhou',
    'ufc@mcmun.org': 'ufc',
    'apple@mcmun.org': 'apple',
    'etatsgeneraux@mcmun.org': 'france',
    'thegreatempire@mcmun.org': 'great-empire',
    'defcon-usrok@mcmun.org': 'defcon-us-rok',
    'defcon-prcdprk@mcmun.org': 'defcon-prc-dprk',
    'unsc-1986@mcmun.org': 'ppr-unsc',
    'ppr-marcos@mcmun.org': 'ppr-af',
    'ppr-cardinal@mcmun.org': 'ppr-namfrel',
    'manifestdestiny-us@mcmun.org': 'manifest-destiny-us',
    'manifestdestiny-latinamerica@mcmun.org': 'manifest-destiny-sa',
    'icc@mcmun.org': 'icc',
    'adhoc@mcmun.org': 'adhoc',
}

def get_committee_from_email(email):
    slug = email_committee_map.get(email, None)
    if slug:
        return Committee.objects.get(slug=slug)
