# grid [![Build Status](https://travis-ci.org/hephyvienna/ansible-role-grid.svg?branch=master)](https://travis-ci.org/hephyvienna/ansible-role-grid) [![Ansible Role](https://img.shields.io/ansible/role/40989.svg)](https://galaxy.ansible.com/hephyvienna/grid)

Ansible role for installation of grid repositories, certificates and voms definitions for WLCG/LCG site.

Inspired by the [Ansible Role UMD](https://github.com/EGI-Foundation/ansible-role-umd)

## Requirements

-   EL6/7
-   EPEL

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    grid_enable_repo: true

Set up the [grid repository](http://repository.egi.eu/category/umd_releases/distribution/umd-4/)
including [yum priorties](https://wiki.centos.org/PackageManagement/Yum/Priorities).

    grid_umd_version: 4

UMD version of the repository. Its most likely 4.

    grid_umd_exclude: []

List of packages to exclude from updates or installs.

    grid_umd_includepkgs: []

List of packages you want to only use from the UMD repository.

    grid_ca_policies_cvmfs: false

CA policies can be installed or used from the CVMFS repository grid.cern.ch

    grid_ca_polices_pkgs:
      - ca-policy-egi-core
      - ca-policy-lcg

RPMs of CA polices to be installed

    grid_install_fetchcrl: true

fetch-crl is only installed when IGTF trustanchors are requested.

    grid_fetchcrl_options: []

Options are passed as a hash. Following keys are possible.
-   agingtolerance: 24
-   nosymlinks: true
-   nowarnings: true
-   noerrors: false
-   http_proxy: <undef>
-   httptimeout: 30
-   parallelism: 4
-   logmode: syslog

Details for the parameters see [Nikhef Wiki](https://wiki.nikhef.nl/grid/FetchCRL3)

    grid_install_empty_ca_policy: true

When the trust anchors are taken from _cvmfs_ an empty ca package [empty-ca-policy](https://copr.fedorainfracloud.org/coprs/dliko/empty-ca-policy/) is installed to satisfy the
rpm dependencies of other packages. A link is enabeling
the CA packages from cvmfs.

    grid_vos: []

A list of Virtual Organisations (VOs) to be configured. The detail of the configuration is
taken from the [EGI Operation Portal](https://operations-portal.egi.eu/)

    grid_voinfo_url: http://cclavoisier01.in2p3.fr:8080/lavoisier/voVoms?accept=json

URL to retrieve the information on the VOs. Updating the VO Info is
performed offline and the new info has to be added to the repository,

    grid_install_voms_client: false

Install VOMS client packages. Usually not required, as packages will be
requested by other installations

    grid_voms_client_pkgs:
      - voms-clients-cpp
      - voms-clients-java

VOMS client packages to be installed.

    grid_host_certificate: {}

Install host certificate. The certificates is provided as hash
-   cert: path to host certificate
-   key: path to private host key. It should be secured with ansible-vault


    grid_enable_dummy_ca: false | true | hostcert

Install a insecure dummy ca certificate for CI. By _hostcert_ in addition a dummy host certificate will be installed. ___Not to be used in production__

    grid_dummy_ca:
      cert: DummyCA.crt
      key: DummyCA.key
      hash: be034f91

Dummy CA distributed with the role.

## Example Playbook

Configuration for a server without CVMFS

    - hosts: servers
      roles:
        - name: hephyvienna.grid
          vars:
            grid_vos:
              - cms
              - alice
              - belle
            grid_host_certificate:
              cert: server.crt
              key: server.key
        - name: hephyvienna.argus

Configuration for a worker node with CVMFS

    - hosts: workers
      roles:
        - name: hephyvienna.grid
          vars:
            grid_vos:
              - cms
              - alice
              - belle
            grid_ca_policies_cvmfs: true
        - name: hephyvienna.cvmfs
        - name: hephyvienna.grid-worker
          vars:
            grid_worker_role: wn

## License

MIT

## Author Information

Written by [Dietrich Liko](http://hephy.at/dliko) in May 2019

[Institute for High Energy Physics](http://www.hephy.at) of the
[Austrian Academy of Sciences](http://www.oeaw.ac.at)
