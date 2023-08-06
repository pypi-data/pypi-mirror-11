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

