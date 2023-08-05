#!/usr/bin/env python3
# coding: utf-8

import asyncore
import click
import falcon
import logging
import mimetypes
import netifaces
import os
import pwd
import random
import re
import signal
import socket
import subprocess
import sys
import time
from certidude.helpers import expand_paths, \
    certidude_request_certificate
from certidude.signer import SignServer
from certidude.wrappers import CertificateAuthorityConfig, \
    CertificateAuthority, Certificate, subject2dn, Request
from datetime import datetime
from humanize import naturaltime
from ipaddress import ip_network
from jinja2 import Environment, PackageLoader
from time import sleep
from setproctitle import setproctitle
from OpenSSL import crypto

env = Environment(loader=PackageLoader("certidude", "templates"), trim_blocks=True)

# Big fat warning:
# m2crypto overflows around 2030 because on 32-bit systems
# m2crypto does not support hardware engine support (?)
# m2crypto CRL object is pretty much useless

# pyopenssl has no straight-forward methods for getting RSA key modulus

# pyopenssl 0.13 bundled with Ubuntu 14.04 has no get_extension_count() for X509Req objects
assert hasattr(crypto.X509Req(), "get_extensions"), "You're running too old version of pyopenssl, upgrade to 0.15+"

# http://www.mad-hacking.net/documentation/linux/security/ssl-tls/creating-ca.xml
# https://kjur.github.io/jsrsasign/
# keyUsage, extendedKeyUsage - https://www.openssl.org/docs/apps/x509v3_config.html
# strongSwan key paths - https://wiki.strongswan.org/projects/1/wiki/SimpleCA

config = CertificateAuthorityConfig("/etc/ssl/openssl.cnf")

# Parse command-line argument defaults from environment
HOSTNAME = socket.gethostname()
USERNAME = os.environ.get("USER")
NOW = datetime.utcnow().replace(tzinfo=None)
FIRST_NAME = None
SURNAME = None
EMAIL = None

if USERNAME:
    EMAIL = USERNAME + "@" + HOSTNAME

if os.getuid() >= 1000:
    _, _, _, _, gecos, _, _ = pwd.getpwnam(USERNAME)
    if " " in gecos:
        FIRST_NAME, SURNAME = gecos.split(" ", 1)
    else:
        FIRST_NAME = gecos

DEFAULT_ROUTE, PRIMARY_INTERFACE = netifaces.gateways().get("default").get(2)
PRIMARY_ALIASES = netifaces.ifaddresses(PRIMARY_INTERFACE).get(2)
PRIMARY_ADDRESS = PRIMARY_ALIASES[0].get("addr")

@click.command("spawn", help="Run privilege isolated signer processes")
@click.option("-k", "--kill", default=False, is_flag=True, help="Kill previous instances")
@click.option("-n", "--no-interaction", default=True, is_flag=True, help="Don't load password protected keys")
def certidude_spawn(kill, no_interaction):
    """
    Spawn processes for signers
    """

    # Process directories
    run_dir = "/run/certidude"
    signer_dir = os.path.join(run_dir, "signer")
    chroot_dir = os.path.join(signer_dir, "jail")

    # Prepare signer PID-s directory
    if not os.path.exists(signer_dir):
        click.echo("Creating: %s" % signer_dir)
        os.makedirs(signer_dir)

    os.umask(0o027)
    uid = os.getuid()
    assert uid == 0, "Not running as root"

    # Preload charmap encoding for byte_string() function of pyOpenSSL
    # in order to enable chrooting
    "".encode("charmap")

    # Prepare chroot directories
    if not os.path.exists(os.path.join(chroot_dir, "dev")):
        os.makedirs(os.path.join(chroot_dir, "dev"))
    if not os.path.exists(os.path.join(chroot_dir, "dev", "urandom")):
        # TODO: use os.mknod instead
        os.system("mknod -m 444 %s c 1 9" % os.path.join(chroot_dir, "dev", "urandom"))

    for ca in config.all_authorities():
        socket_path = os.path.join(signer_dir, ca.slug + ".sock")
        pidfile_path = os.path.join(signer_dir, ca.slug + ".pid")

        try:
            with open(pidfile_path) as fh:
                pid = int(fh.readline())
                os.kill(pid, 0)
                click.echo("Found process with PID %d for %s" % (pid, ca.slug))
        except (ValueError, ProcessLookupError, FileNotFoundError):
            pid = 0

        if pid > 0:
            if kill:
                try:
                    click.echo("Killing %d" % pid)
                    os.kill(pid, signal.SIGTERM)
                    sleep(1)
                    os.kill(pid, signal.SIGKILL)
                    sleep(1)
                except ProcessLookupError:
                    pass
            else:
                continue

        child_pid = os.fork()

        if child_pid == 0:
            with open(pidfile_path, "w") as fh:
                fh.write("%d\n" % os.getpid())

            setproctitle("%s spawn %s" % (sys.argv[0], ca.slug))
            logging.basicConfig(
                filename="/var/log/certidude-%s.log" % ca.slug,
                level=logging.INFO)
            server = SignServer(socket_path, ca.private_key, ca.certificate.path,
                ca.certificate_lifetime, ca.basic_constraints, ca.key_usage,
                ca.extended_key_usage, ca.revocation_list_lifetime)
            asyncore.loop()
        else:
            click.echo("Spawned certidude signer process with PID %d at %s" % (child_pid, socket_path))


@click.command("client", help="Setup X.509 certificates for application")
@click.argument("url") #, help="Certidude authority endpoint URL")
@click.option("--common-name", "-cn", default=HOSTNAME, help="Common name, '%s' by default" % HOSTNAME)
@click.option("--org-unit", "-ou", help="Organizational unit")
@click.option("--email-address", "-m", default=EMAIL, help="E-mail associated with the request, '%s' by default" % EMAIL)
@click.option("--given-name", "-gn", default=FIRST_NAME, help="Given name of the person associted with the certificate, '%s' by default" % FIRST_NAME)
@click.option("--surname", "-sn", default=SURNAME, help="Surname of the person associted with the certificate, '%s' by default" % SURNAME)
@click.option("--key-usage", "-ku", help="Key usage attributes, none requested by default")
@click.option("--extended-key-usage", "-eku", help="Extended key usage attributes, none requested by default")
@click.option("--quiet", "-q", default=False, is_flag=True, help="Disable verbose output")
@click.option("--autosign", "-s", default=False, is_flag=True, help="Request for automatic signing if available")
@click.option("--wait", "-w", default=False, is_flag=True, help="Wait for certificate, by default return immideately")
@click.option("--key-path", "-k", default=HOSTNAME + ".key", help="Key path, %s.key by default" % HOSTNAME)
@click.option("--request-path", "-r", default=HOSTNAME + ".csr", help="Request path, %s.csr by default" % HOSTNAME)
@click.option("--certificate-path", "-c", default=HOSTNAME + ".crt", help="Certificate path, %s.crt by default" % HOSTNAME)
@click.option("--authority-path", "-a", default="ca.crt", help="Certificate authority certificate path, ca.crt by default")
def certidude_setup_client(quiet, **kwargs):
    return certidude_request_certificate(**kwargs)


@click.command("server", help="Set up OpenVPN server")
@click.argument("url")
@click.option("--common-name", "-cn", default=HOSTNAME, help="Common name, %s by default" % HOSTNAME)
@click.option("--org-unit", "-ou", help="Organizational unit")
@click.option("--email-address", "-m", default=EMAIL, help="E-mail associated with the request, '%s' by default" % EMAIL)
@click.option("--subnet", "-s", default="192.168.33.0/24", type=ip_network, help="OpenVPN subnet, 192.168.33.0/24 by default")
@click.option("--local", "-l", default=PRIMARY_ADDRESS, help="OpenVPN listening address, %s" % PRIMARY_ADDRESS)
@click.option("--port", "-p", default=1194, type=click.IntRange(1,60000), help="OpenVPN listening port, 1194 by default")
@click.option('--proto', "-t", default="udp", type=click.Choice(['udp', 'tcp']), help="OpenVPN transport protocol, UDP by default")
@click.option("--route", "-r", type=ip_network, multiple=True, help="Subnets to advertise via this connection, multiple allowed")
@click.option("--config", "-o",
    default="/etc/openvpn/site-to-client.conf",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="OpenVPN configuration file")
@click.option("--directory", "-d", default="/etc/openvpn/keys", help="Directory for keys, /etc/openvpn/keys by default")
@click.option("--key-path", "-key", default=HOSTNAME + ".key", help="Key path, %s.key relative to --directory by default" % HOSTNAME)
@click.option("--request-path", "-csr", default=HOSTNAME + ".csr", help="Request path, %s.csr relative to --directory by default" % HOSTNAME)
@click.option("--certificate-path", "-crt", default=HOSTNAME + ".crt", help="Certificate path, %s.crt relative to --directory by default" % HOSTNAME)
@click.option("--dhparam-path", "-dh", default="dhparam2048.pem", help="Diffie/Hellman parameters path, dhparam2048.pem relative to --directory by default")
@click.option("--authority-path", "-ca", default="ca.crt", help="Certificate authority certificate path, ca.crt relative to --dir by default")
@expand_paths()
def certidude_setup_openvpn_server(url, config, subnet, route, email_address, common_name, org_unit, directory, key_path, request_path, certificate_path, authority_path, dhparam_path, local, proto, port):
    # TODO: Intelligent way of getting last IP address in the subnet
    subnet_first = None
    subnet_last = None
    subnet_second = None
    for addr in subnet.hosts():
        if not subnet_first:
            subnet_first = addr
            continue
        if not subnet_second:
            subnet_second = addr
        subnet_last = addr

    if not os.path.exists(certificate_path):
        click.echo("As OpenVPN server certificate needs specific key usage extensions please")
        click.echo("use following command to sign on Certidude server instead of web interface:")
        click.echo()
        click.echo("  certidude sign %s" % common_name)

    retval = certidude_request_certificate(
        url,
        key_path,
        request_path,
        certificate_path,
        authority_path,
        common_name,
        org_unit,
        email_address,
        key_usage="nonRepudiation,digitalSignature,keyEncipherment",
        extended_key_usage="serverAuth,ikeIntermediate",
        wait=True)

    if not os.path.exists(dhparam_path):
        cmd = "openssl", "dhparam", "-out", dhparam_path, "2048"
        subprocess.check_call(cmd)

    if retval:
        return retval

    # TODO: Add dhparam
    config.write(env.get_template("openvpn-site-to-client.ovpn").render(locals()))

    click.echo("Generated %s" % config.name)
    click.echo()
    click.echo("Inspect newly created %s and start OpenVPN service:" % config.name)
    click.echo()
    click.secho("  service openvpn restart", bold=True)
    click.echo()


@click.command("client", help="Set up OpenVPN client")
@click.argument("url")
@click.argument("remote")
@click.option('--proto', "-t", default="udp", type=click.Choice(['udp', 'tcp']), help="OpenVPN transport protocol, UDP by default")
@click.option("--common-name", "-cn", default=HOSTNAME, help="Common name, %s by default" % HOSTNAME)
@click.option("--org-unit", "-ou", help="Organizational unit")
@click.option("--email-address", "-m", default=EMAIL, help="E-mail associated with the request, '%s' by default" % EMAIL)
@click.option("--config", "-o",
    default="/etc/openvpn/client-to-site.conf",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="OpenVPN configuration file")
@click.option("--directory", "-d", default="/etc/openvpn/keys", help="Directory for keys, /etc/openvpn/keys by default")
@click.option("--key-path", "-k", default=HOSTNAME + ".key", help="Key path, %s.key relative to --directory by default" % HOSTNAME)
@click.option("--request-path", "-r", default=HOSTNAME + ".csr", help="Request path, %s.csr relative to --directory by default" % HOSTNAME)
@click.option("--certificate-path", "-c", default=HOSTNAME + ".crt", help="Certificate path, %s.crt relative to --directory by default" % HOSTNAME)
@click.option("--authority-path", "-a", default="ca.crt", help="Certificate authority certificate path, ca.crt relative to --dir by default")
@expand_paths()
def certidude_setup_openvpn_client(url, config, email_address, common_name, org_unit, directory, key_path, request_path, certificate_path, authority_path, proto, remote):

    retval = certidude_request_certificate(
        url,
        key_path,
        request_path,
        certificate_path,
        authority_path,
        common_name,
        org_unit,
        email_address,
        wait=True)

    if retval:
        return retval

    # TODO: Add dhparam
    config.write(env.get_template("openvpn-client-to-site.ovpn").render(locals()))

    click.echo("Generated %s" % config.name)
    click.echo()
    click.echo("Inspect newly created %s and start OpenVPN service:" % config.name)
    click.echo()
    click.echo("  service openvpn restart")
    click.echo()


@click.command("server", help="Set up strongSwan server")
@click.argument("url")
@click.option("--common-name", "-cn", default=HOSTNAME, help="Common name, %s by default" % HOSTNAME)
@click.option("--org-unit", "-ou", help="Organizational unit")
@click.option("--fqdn", "-f", default=HOSTNAME, help="Fully qualified hostname, %s by default" % PRIMARY_ADDRESS)
@click.option("--email-address", "-m", default=EMAIL, help="E-mail associated with the request, %s by default" % EMAIL)
@click.option("--subnet", "-s", default="192.168.33.0/24", type=ip_network, help="IPsec virtual subnet, 192.168.33.0/24 by default")
@click.option("--local", "-l", default=PRIMARY_ADDRESS, help="IPsec gateway address, %s" % PRIMARY_ADDRESS)
@click.option("--route", "-r", type=ip_network, multiple=True, help="Subnets to advertise via this connection, multiple allowed")
@click.option("--config", "-o",
    default="/etc/ipsec.conf",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="strongSwan configuration file, /etc/ipsec.conf by default")
@click.option("--secrets", "-s",
    default="/etc/ipsec.secrets",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="strongSwan secrets file, /etc/ipsec.secrets by default")
@click.option("--directory", "-d", default="/etc/ipsec.d", help="Directory for keys, /etc/ipsec.d by default")
@click.option("--key-path", "-key", default="private/%s.pem" % HOSTNAME, help="Key path, private/%s.pem by default" % HOSTNAME)
@click.option("--request-path", "-csr", default="reqs/%s.pem" % HOSTNAME, help="Request path, reqs/%s.pem by default" % HOSTNAME)
@click.option("--certificate-path", "-crt", default="certs/%s.pem" % HOSTNAME, help="Certificate path, certs/%s.pem by default" % HOSTNAME)
@click.option("--authority-path", "-ca", default="cacerts/ca.pem", help="Certificate authority certificate path, cacerts/ca.pem by default")
@expand_paths()
def certidude_setup_strongswan_server(url, config, secrets, subnet, route, email_address, common_name, org_unit, directory, key_path, request_path, certificate_path, authority_path, local, ip_address, fqdn):

    config.write(env.get_template("strongswan-site-to-client.conf").render(locals()))

    if not os.path.exists(certificate_path):
        click.echo("As strongSwan server certificate needs specific key usage extensions please")
        click.echo("use following command to sign on Certidude server instead of web interface:")
        click.echo()
        click.echo("  certidude sign %s" % common_name)

    retval = certidude_request_certificate(
        url,
        key_path,
        request_path,
        certificate_path,
        authority_path,
        common_name,
        org_unit,
        email_address,
        key_usage="nonRepudiation,digitalSignature,keyEncipherment",
        extended_key_usage="serverAuth,ikeIntermediate",
        ipv4_address=None if local.is_private else local,
        dns=None if local.is_private or "." not in fdqn else fdqn,
        wait=True)

    if retval:
        return retval


    click.echo("Generated %s" % config.name)
    click.echo()
    click.echo("Inspect newly created %s and start strongSwan service:" % config.name)
    click.echo()
    click.echo("  apt-get install strongswan strongswan-starter strongswan-ikev2")
    click.secho("  service strongswan restart", bold=True)
    click.echo()


@click.command("client", help="Set up strongSwan client")
@click.argument("url")
@click.argument("remote")
@click.option("--common-name", "-cn", default=HOSTNAME, help="Common name, %s by default" % HOSTNAME)
@click.option("--org-unit", "-ou", help="Organizational unit")
@click.option("--email-address", "-m", default=EMAIL, help="E-mail associated with the request, '%s' by default" % EMAIL)
@click.option("--config", "-o",
    default="/etc/ipsec.conf",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="strongSwan configuration file, /etc/ipsec.conf by default")
@click.option("--secrets", "-s",
    default="/etc/ipsec.secrets",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="strongSwan secrets file, /etc/ipsec.secrets by default")
@click.option("--dpdaction", "-d",
    default="restart",
    type=click.Choice(["none", "clear", "hold", "restart"]),
    help="Action upon dead peer detection; either none, clear, hold or restart")
@click.option("--auto", "-a",
    default="start",
    type=click.Choice(["ignore", "add", "route", "start"]),
    help="Operation at startup; either ignore, add, route or start")
@click.option("--directory", "-d", default="/etc/ipsec.d", help="Directory for keys, /etc/ipsec.d by default")
@click.option("--key-path", "-key", default="private/%s.pem" % HOSTNAME, help="Key path, private/%s.pem by default" % HOSTNAME)
@click.option("--request-path", "-csr", default="reqs/%s.pem" % HOSTNAME, help="Request path, reqs/%s.pem by default" % HOSTNAME)
@click.option("--certificate-path", "-crt", default="certs/%s.pem" % HOSTNAME, help="Certificate path, certs/%s.pem by default" % HOSTNAME)
@click.option("--authority-path", "-ca", default="cacerts/ca.pem", help="Certificate authority certificate path, cacerts/ca.pem by default")
@expand_paths()
def certidude_setup_strongswan_client(url, config, secrets, email_address, common_name, org_unit, directory, key_path, request_path, certificate_path, authority_path, remote, auto, dpdaction):

    retval = certidude_request_certificate(
        url,
        key_path,
        request_path,
        certificate_path,
        authority_path,
        common_name,
        org_unit,
        email_address,
        wait=True)

    if retval:
        return retval

    # TODO: Add dhparam
    config.write(env.get_template("strongswan-client-to-site.conf").render(locals()))

    click.echo("Generated %s" % config.name)
    click.echo()
    click.echo("Inspect newly created %s and start strongSwan service:" % config.name)
    click.echo()
    click.echo("  apt-get install strongswan strongswan-starter")
    click.echo("  service strongswan restart")
    click.echo()


@click.command("production", help="Set up nginx and uwsgi")
@click.option("--username", default="certidude", help="Service user account, created if necessary, 'certidude' by default")
@click.option("--hostname", default=HOSTNAME, help="nginx hostname, '%s' by default" % HOSTNAME)
@click.option("--static-path", default=os.path.join(os.path.dirname(__file__), "static"), help="Static files")
@click.option("--nginx-config", "-n",
    default="/etc/nginx/nginx.conf",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="nginx configuration, /etc/nginx/nginx.conf by default")
@click.option("--uwsgi-config", "-u",
    default="/etc/uwsgi/apps-available/certidude.ini",
    type=click.File(mode="w", atomic=True, lazy=True),
    help="uwsgi configuration, /etc/uwsgi/ by default")
@click.option("--push-server", help="Push server URL, in case of different nginx instance")
def certidude_setup_production(username, hostname, push_server, nginx_config, uwsgi_config, static_path):
    try:
        pwd.getpwnam(username)
        click.echo("Username '%s' already exists, excellent!" % username)
    except KeyError:
        cmd = "adduser", "--system",  "--no-create-home", "--group", username
        subprocess.check_call(cmd)

#    cmd = "gpasswd", "-a", username, "www-data"
#    subprocess.check_call(cmd)

    if not static_path.endswith("/"):
        static_path += "/"

    nginx_config.write(env.get_template("nginx.conf").render(locals()))
    click.echo("Generated: %s" % nginx_config.name)
    uwsgi_config.write(env.get_template("uwsgi.ini").render(locals()))
    click.echo("Generated: %s" % uwsgi_config.name)

    if os.path.exists("/etc/uwsgi/apps-enabled/certidude.ini"):
        os.unlink("/etc/uwsgi/apps-enabled/certidude.ini")
    os.symlink(uwsgi_config.name, "/etc/uwsgi/apps-enabled/certidude.ini")
    click.echo("Symlinked %s -> /etc/uwsgi/apps-enabled/certidude.ini" % uwsgi_config.name)

    if not push_server:
        click.echo("Remember to install nginx with wandenberg/nginx-push-stream-module!")


@click.command("authority", help="Set up Certificate Authority in a directory")
@click.option("--group", "-g", default="certidude", help="Group for file permissions, certidude by default")
@click.option("--parent", "-p", help="Parent CA, none by default")
@click.option("--common-name", "-cn", default=HOSTNAME, help="Common name, hostname by default")
@click.option("--country", "-c", default="ee", help="Country, Estonia by default")
@click.option("--state", "-s", default="Harjumaa", help="State or country, Harjumaa by default")
@click.option("--locality", "-l", default="Tallinn", help="City or locality, Tallinn by default")
@click.option("--authority-lifetime", default=20*365, help="Authority certificate lifetime in days, 7300 days (20 years) by default")
@click.option("--certificate-lifetime", default=5*365, help="Certificate lifetime in days, 1825 days (5 years) by default")
@click.option("--revocation-list-lifetime", default=1, help="Revocation list lifetime in days, 1 day by default")
@click.option("--organization", "-o", default="Example LLC", help="Company or organization name")
@click.option("--organizational-unit", "-ou", default="Certification Department")
@click.option("--pkcs11", default=False, is_flag=True, help="Use PKCS#11 token instead of files")
@click.option("--crl-distribution-url", default=None, help="CRL distribution URL")
@click.option("--ocsp-responder-url", default=None, help="OCSP responder URL")
@click.option("--email-address", default=EMAIL, help="CA e-mail address")
@click.option("--inbox", default="imap://user:pass@host:port/INBOX", help="Inbound e-mail server")
@click.option("--outbox", default="smtp://localhost", help="Outbound e-mail server")
@click.argument("directory")
def certidude_setup_authority(parent, country, state, locality, organization, organizational_unit, common_name, directory, certificate_lifetime, authority_lifetime, revocation_list_lifetime, pkcs11, group, crl_distribution_url, ocsp_responder_url, email_address, inbox, outbox):
    logging.info("Creating certificate authority in %s", directory)
    _, _, uid, gid, gecos, root, shell = pwd.getpwnam(group)
    os.setgid(gid)

    click.echo("Generating 4096-bit RSA key...")

    if pkcs11:
        raise NotImplementedError("Hardware token support not yet implemented!")
    else:
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 4096)

    slug = os.path.basename(directory)

    if not crl_distribution_url:
        crl_distribution_url = "http://%s/api/%s/revoked/" % (common_name, slug)

    # File paths
    ca_key = os.path.join(directory, "ca_key.pem")
    ca_crt = os.path.join(directory, "ca_crt.pem")
    ca_crl = os.path.join(directory, "ca_crl.pem")
    crl_distribution_points = "URI:%s" % crl_distribution_url

    ca = crypto.X509()
    ca.set_version(2) # This corresponds to X.509v3
    ca.set_serial_number(1)
    ca.get_subject().CN = common_name
    ca.get_subject().C = country
    ca.get_subject().ST = state
    ca.get_subject().L = locality
    ca.get_subject().O = organization
    ca.get_subject().OU = organizational_unit
    ca.gmtime_adj_notBefore(0)
    ca.gmtime_adj_notAfter(authority_lifetime * 24 * 60 * 60)
    ca.set_issuer(ca.get_subject())
    ca.set_pubkey(key)
    ca.add_extensions([
        crypto.X509Extension(
            b"basicConstraints",
            True,
            b"CA:TRUE"),
        crypto.X509Extension(
            b"keyUsage",
            True,
            b"keyCertSign, cRLSign"),
        crypto.X509Extension(
            b"subjectKeyIdentifier",
            False,
            b"hash",
            subject = ca),
        crypto.X509Extension(
            b"crlDistributionPoints",
            False,
            crl_distribution_points.encode("ascii"))
    ])

    if email_address:
        subject_alt_name = "email:%s" % email_address
        ca.add_extensions([
            crypto.X509Extension(
                b"subjectAltName",
                False,
                subject_alt_name.encode("ascii"))
        ])

    if ocsp_responder_url:
        raise NotImplementedError()

    """
        ocsp_responder_url = "http://%s/api/%s/ocsp/" % (common_name, slug)
        authority_info_access = "OCSP;URI:%s" % ocsp_responder_url
        ca.add_extensions([
            crypto.X509Extension(
                b"authorityInfoAccess",
                False,
                authority_info_access.encode("ascii"))
        ])
    """

    click.echo("Signing %s..." % subject2dn(ca.get_subject()))

    # openssl x509 -in ca_crt.pem -outform DER | sha1sum
    # openssl x509 -fingerprint -in ca_crt.pem

    ca.sign(key, "sha1")

    os.umask(0o027)
    if not os.path.exists(directory):
        os.makedirs(directory)

    os.umask(0o007)

    for subdir in ("signed", "requests", "revoked"):
        if not os.path.exists(os.path.join(directory, subdir)):
            os.mkdir(os.path.join(directory, subdir))
    with open(ca_crl, "wb") as fh:
        crl = crypto.CRL()
        fh.write(crl.export(ca, key, days=revocation_list_lifetime))
    with open(os.path.join(directory, "serial"), "w") as fh:
        fh.write("1")

    os.umask(0o027)
    with open(ca_crt, "wb") as fh:
        fh.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca))


    os.umask(0o077)
    with open(ca_key, "wb") as fh:
        fh.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    click.echo("Insert following to /etc/ssl/openssl.cnf:")
    click.echo()
    click.secho(env.get_template("openssl.cnf").render(locals()), fg="blue")

    click.echo()
    click.echo("Use following commands to inspect the newly created files:")
    click.echo()
    click.echo("  openssl crl -inform PEM -text -noout -in %s" % ca_crl)
    click.echo("  openssl x509 -text -noout -in %s" % ca_crt)
    click.echo("  openssl rsa -check -in %s" % ca_key)
    click.echo("  openssl verify -CAfile %s %s" % (ca_crt, ca_crt))
    click.echo()
    click.echo("Use following to launch privilege isolated signer processes:")
    click.echo()
    click.echo("  certidude spawn")
    click.echo()
    click.echo("Use following command to serve CA read-only:")
    click.echo()
    click.echo("  certidude serve")


@click.command("list", help="List certificates")
@click.argument("ca", nargs=-1)
@click.option("--show-key-type", "-k", default=False, is_flag=True, help="Show key type and length")
@click.option("--show-path", "-p", default=False, is_flag=True, help="Show filesystem paths")
@click.option("--show-extensions", "-e", default=False, is_flag=True, help="Show X.509 Certificate Extensions")
def certidude_list(ca, show_key_type, show_extensions, show_path):
    from pycountry import countries
    def dump_common(j):
        if show_path:
            click.echo(" |    |   Path: %s" % j.path)

        person = [j for j in (j.given_name, j.surname) if j]
        if person:
            click.echo(" |    |   Associated person: %s" % " ".join(person) + (" <%s>" % j.email_address if j.email_address else ""))
        elif j.email_address:
            click.echo(" |    |   Associated e-mail: " + j.email_address)

        bits = [j for j in (
            countries.get(alpha2=j.country_code.upper()).name if
            j.country_code else "",
            j.state_or_county,
            j.city,
            j.organization,
            j.organizational_unit) if j]
        if bits:
            click.echo(" |    |   Organization: %s" % ", ".join(bits))

        if show_key_type:
            click.echo(" |    |   Key type: %s-bit %s" % (j.key_length, j.key_type))

        if show_extensions:
            for key, value, data in j.extensions:
                click.echo((" |    |   Extension " + key + ":").ljust(50) + " " + value)
        elif j.key_usage:
            click.echo(" |    |   Key usage: " + j.key_usage)
        click.echo(" |    |")

    for ca in config.all_authorities():
        click.echo("Certificate authority " + click.style(ca.slug, fg="blue"))
#        if ca.certificate.email_address:
#            click.echo("  \u2709 %s" % ca.certificate.email_address)

        if ca.certificate.signed < NOW and ca.certificate.expires > NOW:
            print(ca.certificate.expires)
            click.echo(" | \u2713 Certificate: " + click.style("valid", fg="green") + ", %s" % ca.certificate.expires)
        elif NOW > ca.certificate.expires:
            click.echo(" | \u2717 Certificate: " + click.style("expired", fg="red"))
        else:
            click.echo(" | \u2717 Certificate: " + click.style("not valid yet", fg="red"))

        if os.path.exists(ca.private_key):
            click.echo(" | \u2713 Private key " + ca.private_key + ": " + click.style("okay", fg="green"))
            # TODO: Check permissions
        else:
            click.echo(" | \u2717 Private key " + ca.private_key + ": " + click.style("does not exist", fg="red"))

        if os.path.isdir(ca.signed_dir):
            click.echo(" | \u2713 Signed certificates directory " + ca.signed_dir + ": " + click.style("okay", fg="green"))
        else:
            click.echo(" | \u2717 Signed certificates directory " + ca.signed_dir + ": " + click.style("does not exist", fg="red"))

        if ca.revoked_dir:
            click.echo(" |   Revoked certificates directory: %s" % ca.revoked_dir)

        click.echo(" +-- Pending requests")

        for j in ca.get_requests():
            click.echo(" |    +-- Request " + click.style(j.common_name, fg="blue"))
            click.echo(" |    |   Submitted: %s, %s" % (naturaltime(j.created), j.created))
            dump_common(j)

        click.echo(" +-- Signed certificates")

        for j in ca.get_signed():
            click.echo(" |    +-- Certificate " + click.style(j.common_name, fg="blue") + " " + click.style(":".join(re.findall("\d\d", j.serial_number)), fg="white"))

            if j.signed < NOW and j.expires > NOW:
                click.echo(" |    | \u2713 Certificate " + click.style("valid", fg="green") + " " + naturaltime(j.expires))
            elif NOW > j.expires:
                click.echo(" |    | \u2717 Certificate " + click.style("expired", fg="red") + " " + naturaltime(j.expires))
            else:
                click.echo(" |    | \u2717 Certificate " + click.style("not valid yet", fg="red"))
            dump_common(j)

        click.echo(" +-- Revocations")

        for j in ca.get_revoked():
            click.echo(" |    +-- Revocation " + click.style(j.common_name, fg="blue") + " " + click.style(":".join(re.findall("\d\d", j.serial_number)), fg="white"))
     #       click.echo(" |    |   Serial: %s" % ":".join(re.findall("\d\d", j.serial_number)))
            if show_path:
                click.echo(" |    |   Path: %s" % j.path)
            click.echo(" |    |   Revoked: %s%s" % (naturaltime(NOW-j.changed), click.style(", %s" % j.changed, fg="white")))
            dump_common(j)

        click.echo()

@click.command("list", help="List Certificate Authorities")
@click.argument("ca")
@config.pop_certificate_authority()
def cert_list(ca):

    mapping = {}

    click.echo("Listing certificates for: %s" % ca.certificate.subject.CN)

    for serial, reason, timestamp in ca.get_revoked():
        mapping[serial] = None, reason

    for certificate in ca.get_signed():
        mapping[certificate.serial] = certificate, None

    for serial, (certificate, reason) in sorted(mapping.items(), key=lambda j:j[0]):
        if not reason:
            click.echo("  %03d. %s %s" % (serial, certificate.subject.CN, (certificate.not_after-NOW)))
        else:
            click.echo("  %03d. Revoked due to: %s" % (serial, reason))

    for request in ca.get_requests():
        click.echo("  ⌛  %s" % request.subject.CN)

@click.command("sign", help="Sign certificates")
@click.argument("common_name")
@click.option("--overwrite", "-o", default=False, is_flag=True, help="Revoke valid certificate with same CN")
@click.option("--lifetime", "-l", help="Lifetime")
def certidude_sign(common_name, overwrite, lifetime):
    def iterate():
        for ca in config.all_authorities():
            for request in ca.get_requests():
                if request.common_name != common_name:
                    continue
                print(request.fingerprint(), request.common_name, request.path, request.key_usage)
                yield ca, request

    results = tuple(iterate())
    click.echo()

    click.echo("Press Ctrl-C to cancel singing these requests...")
    sys.stdin.readline()

    for ca, request in results:
        if request.signable:
            # Sign via signer process
            cert = ca.sign(request)
        else:
            # Sign directly using private key
            cert = ca.sign2(request, overwrite, True, lifetime)

        click.echo("Signed %s" % cert.distinguished_name)
        for key, value, data in cert.extensions:
            click.echo("Added extension %s: %s" % (key, value))
        click.echo()

class StaticResource(object):
    def __init__(self, root):
        self.root = os.path.realpath(root)
        click.echo("Serving static from: %s" % self.root)

    def __call__(self, req, resp):

        path = os.path.realpath(os.path.join(self.root, req.path[1:]))
        if not path.startswith(self.root):
            raise falcon.HTTPForbidden

        print("Serving:", path)
        if os.path.exists(path):
            content_type, content_encoding = mimetypes.guess_type(path)
            if content_type:
                resp.append_header("Content-Type", content_type)
            if content_encoding:
                resp.append_header("Content-Encoding", content_encoding)
            resp.append_header("Content-Disposition", "attachment")
            resp.stream = open(path, "rb")
        else:
            resp.status = falcon.HTTP_404
            resp.body = "File '%s' not found" % req.path

@click.command("serve", help="Run built-in HTTP server")
@click.option("-u", "--user", default="certidude", help="Run as user")
@click.option("-p", "--port", default=80, help="Listen port")
@click.option("-l", "--listen", default="0.0.0.0", help="Listen address")
@click.option("-s", "--enable-signature", default=False, is_flag=True, help="Allow signing operations with private key of CA")
def certidude_serve(user, port, listen, enable_signature):

    logging.basicConfig(
        filename='/var/log/certidude.log',
        level=logging.DEBUG)

    click.echo("Serving API at %s:%d" % (listen, port))
    import pwd
    import falcon
    from wsgiref.simple_server import make_server, WSGIServer
    from socketserver import ThreadingMixIn
    from certidude.api import CertificateAuthorityResource, \
        RequestDetailResource, RequestListResource, \
        SignedCertificateDetailResource, SignedCertificateListResource, \
        RevocationListResource, IndexResource, ApplicationConfigurationResource, \
        CertificateStatusResource

    class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
        pass

    click.echo("Listening on %s:%d" % (listen, port))

    app = falcon.API()
    app.add_route("/api/{ca}/ocsp/", CertificateStatusResource(config))
    app.add_route("/api/{ca}/signed/{cn}/openvpn", ApplicationConfigurationResource(config))
    app.add_route("/api/{ca}/certificate/", CertificateAuthorityResource(config))
    app.add_route("/api/{ca}/revoked/", RevocationListResource(config))
    app.add_route("/api/{ca}/signed/{cn}/", SignedCertificateDetailResource(config))
    app.add_route("/api/{ca}/signed/", SignedCertificateListResource(config))
    app.add_route("/api/{ca}/request/{cn}/", RequestDetailResource(config))
    app.add_route("/api/{ca}/request/", RequestListResource(config))
    app.add_route("/api/{ca}/", IndexResource(config))

    app.add_sink(StaticResource(os.path.join(os.path.dirname(__file__), "static")))
    httpd = make_server(listen, port, app, ThreadingWSGIServer)
    if user:
        _, _, uid, gid, gecos, root, shell = pwd.getpwnam(user)
        if uid == 0:
            click.echo("Please specify unprivileged user")
            exit(254)
        click.echo("Switching to user %s (uid=%d, gid=%d)" % (user, uid, gid))
        os.setgid(gid)
        os.setuid(uid)
        os.umask(0o007)
    elif os.getuid() == 0:
        click.echo("Warning: running as root, this is not reccommended!")
    httpd.serve_forever()

@click.group("strongswan", help="strongSwan helpers")
def certidude_setup_strongswan(): pass

@click.group("openvpn", help="OpenVPN helpers")
def certidude_setup_openvpn(): pass

@click.group("setup", help="Getting started section")
def certidude_setup(): pass

@click.group()
def entry_point(): pass

certidude_setup_strongswan.add_command(certidude_setup_strongswan_server)
certidude_setup_strongswan.add_command(certidude_setup_strongswan_client)
certidude_setup_openvpn.add_command(certidude_setup_openvpn_server)
certidude_setup_openvpn.add_command(certidude_setup_openvpn_client)
certidude_setup.add_command(certidude_setup_authority)
certidude_setup.add_command(certidude_setup_openvpn)
certidude_setup.add_command(certidude_setup_strongswan)
certidude_setup.add_command(certidude_setup_client)
certidude_setup.add_command(certidude_setup_production)
entry_point.add_command(certidude_setup)
entry_point.add_command(certidude_serve)
entry_point.add_command(certidude_spawn)
entry_point.add_command(certidude_sign)
entry_point.add_command(certidude_list)
