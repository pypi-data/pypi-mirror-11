======
pykube
======

*Python client for Kubernetes*

.. image:: https://img.shields.io/pypi/dm/pykube.svg
    :target:  https://pypi.python.org/pypi/pykube/

.. image:: https://img.shields.io/pypi/v/pykube.svg
    :target:  https://pypi.python.org/pypi/pykube/

.. image:: https://img.shields.io/badge/license-apache-blue.svg
    :target:  https://pypi.python.org/pypi/pykube/


Client library written in Python to interface to Kubernetes.

Features
========

* HTTP interface using requests using kubeconfig for authentication

Requirements
============

* Python 2.7 or 3.4
* requests (included in ``install_requires``)
* PyYAML (included in ``install_requires``)

Example
=======

Given a kubeconfig at `/etc/kubectl-config/kubeconfig`:

    kind: Config
    apiVersion: v1
    clusters:
      - cluster:
          certificate-authority-data: "..."
          server: https://127.0.0.1
        name: cluster1
    users:
      - name: user1
        user:
          client-certificate-data: "..."
          client-key-data: "..."
          token: "..."
    contexts:
      - context:
          cluster: cluster1
          user: user1
        name: context1
