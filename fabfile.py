from fabric.api import local, run, env, settings


def less():
    local("lessc mcmun/static/css/mcmun.less -x > mcmun/static/css/mcmun.css")

def up():
    local("python manage.py runserver")

def dump():
    local("python manage.py dumpdata --indent=4 > backup.json")

def static():
    local("python manage.py collectstatic --noinput")

def restart():
    local('kill -HUP `cat /tmp/gunicorn.pid`')

def stats():
    local('python manage.py get_registration_stats')

def pubcrawl():
    local('python manage.py get_pubcrawl_stats')
