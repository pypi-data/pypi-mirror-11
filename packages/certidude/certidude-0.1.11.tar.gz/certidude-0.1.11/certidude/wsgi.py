
import os
import falcon
from certidude.wrappers import CertificateAuthorityConfig
from certidude.api import CertificateAuthorityResource, \
    RequestDetailResource, RequestListResource, \
    SignedCertificateDetailResource, SignedCertificateListResource, \
    RevocationListResource, IndexResource, ApplicationConfigurationResource, \
    CertificateStatusResource

# TODO: deduplicate routing code
# TODO: set up /run/certidude/api paths and permissions

config = CertificateAuthorityConfig("/etc/ssl/openssl.cnf")

assert os.getenv("CERTIDUDE_EVENT_SUBSCRIBE"), "Please set CERTIDUDE_EVENT_SUBSCRIBE to your web server's subscription URL"
assert os.getenv("CERTIDUDE_EVENT_PUBLISH"), "Please set CERTIDUDE_EVENT_PUBLISH to your web server's publishing URL"

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

