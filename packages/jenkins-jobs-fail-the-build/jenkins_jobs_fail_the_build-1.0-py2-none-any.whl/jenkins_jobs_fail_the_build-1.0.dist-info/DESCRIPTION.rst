################################################
Fail The Build Extension for Jenkins Job Builder
################################################

What is it?
===========

This package registers entry points that extend `Jenkins Job Builder`_ to support the Jenkins `Fail The Build Plugin`_.

.. _Jenkins Job Builder: http://ci.openstack.org/jenkins-job-builder/
.. _Fail The Build Plugin: https://wiki.jenkins-ci.org/display/JENKINS/Fail+The+Build+Plugin

Installation
============

::

    pip install jenkins-jobs-fail-the-build

Usage
=====

**Complete**::

    - job:
        name: 'MyJob'
        builders:
            - set-build-result: "ABORTED|CYCLE|FAILED|SUCCESS|UNSTABLE"



Credits
=======

``jenkins-jobs-fail-the-build`` was created by Enrico Mills

It's development is supported by `Socket Mobile <http://www.socketmobile.com>`_

Special thanks to `Hynek Schlawack <https://github.com/hynek>`_ whose 
`Sharing Your Labor of Love <https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/>`_
was instrumental in the publication of this package.


