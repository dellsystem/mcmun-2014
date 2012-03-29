from fabric.api import local, run, env

env.hosts = ['mcmun@mcmun.org']

FILES = ['index.html', 'css/splash.css', 'img/dove.png', 'img/email.png', 'img/facebook.png', 'img/logo.png', 'img/twitter.png', 'css/fonts/*']

def prepare():
	local('lessc css/splash.less -x > css/splash.css')

def archive():
	local('tar czvf mcmun.tar.gz %s' % ' '.join(FILES))

def transfer():
	local('scp mcmun.tar.gz %s:mcmun.org/ROOT' % env.hosts[0])
	local('rm mcmun.tar.gz')

def unpack():
	run('cd mcmun.org/ROOT; tar xvzf mcmun.tar.gz')

def deploy():
	prepare()
	archive()
	transfer()
	unpack()
