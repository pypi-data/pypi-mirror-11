Pekaboo
========

Expose hardware info through HTTP.

Install
=======

Here are the instructions for a manual install on CentOS 7.

.. code-block:: bash

  sudo groupadd dmidecode
  sudo useradd -M -G dmidecode peekaboo
  sudo tee -a /etc/sudoers.d/dmidecode << EOF >/dev/null
  %dmidecode ALL=(ALL) NOPASSWD:/usr/sbin/dmidecode
  EOF
  sudo yum install -y libselinux-utils redhat-lsb python-devel python-pip gcc
  sudo pip install peekaboo
  sudo cp /usr/share/peekaboo/contrib/peekaboo.service /usr/lib/systemd/system/peekaboo.service
  sudo systemctl enable peekaboo
  sudo systemctl start peekaboo

You can also install it using:

.. code-block:: bash

  curl https://raw.githubusercontent.com/mickep76/peekaboo/master/setup_centos7.sh | sudo bash

Run using Docker
================

You can quickly test it by running it inside a Docker container:


Build docker image
==================

.. code-block:: bash

  docker build -t peekaboo:latest .

Run docker image
================

.. code-block:: bash

  docker run -d -p 5050:5050 --name=peekaboo peekaboo:latest

Stop container
==============

.. code-block:: bash

  docker stop peekaboo

Query
=====

Query using YAML:

.. code-block:: bash

  curl -i http://<host>:5050/info
  curl -i http://<host>:5050/info/tree
  curl -i http://<host>:5050/status
  curl -i http://<host>:5050/status/tree

Query using JSON:

.. code-block:: bash

  curl -i -H "Accept: application/json" http://<host>:5050/info
  curl -i -H "Accept: application/json" http://<host>:5050/info/tree
  curl -i -H "Accept: application/json" http://<host>:5050/status
  curl -i -H "Accept: application/json" http://<host>:5050/status/tree
