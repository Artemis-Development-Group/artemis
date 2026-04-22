class websockets {
  exec { 'add artemis ppa':
    command => 'add-apt-repository -y ppa:artemis/ppa',
    unless  => 'apt-cache policy | grep artemis/ppa',
    notify  => Exec['update apt cache'],
  }

  $dependencies = [
    'python',
    'python-baseplate',
    'python-coverage',
    'python-gevent',
    'python-gevent-websocket',
    'python-haigha',
    'python-manhole',
    'python-mock',
    'python-nose',
    'python-raven',
    'python-setuptools',
    'python-webtest',
  ]

  package { $dependencies:
    ensure => installed,
    before => Exec['build app'],
  }

  exec { 'build app':
    user    => $::user,
    cwd     => $::project_path,
    command => 'python setup.py build',
    before  => Exec['install app'],
  }

  exec { 'install app':
    user    => $::user,
    cwd     => $::project_path,
    command => 'python setup.py develop --user',
  }
}
