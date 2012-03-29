from fabric.api import local, run

def less():
	local('lessc css/splash.less -x > css/splash.css')

def deploy():
	pass
