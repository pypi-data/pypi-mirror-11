import tempfile
import os
import re
import shutil
import cStringIO
from contextlib import contextmanager
from libpathod import utils, test, pathoc, pathod, language
from netlib import tcp
import requests

def treader(bytes):
    """
        Construct a tcp.Read object from bytes.
    """
    fp = cStringIO.StringIO(bytes)
    return tcp.Reader(fp)


class DaemonTests(object):
    noweb = False
    noapi = False
    nohang = False
    ssl = False
    timeout = None
    hexdump = False
    ssloptions = None
    nocraft = False

    @classmethod
    def setUpAll(klass):
        opts = klass.ssloptions or {}
        klass.confdir = tempfile.mkdtemp()
        opts["confdir"] = klass.confdir
        so = pathod.SSLOptions(**opts)
        klass.d = test.Daemon(
            staticdir=test_data.path("data"),
            anchors=[
                (re.compile("/anchor/.*"), "202:da")
            ],
            ssl=klass.ssl,
            ssloptions=so,
            sizelimit=1 * 1024 * 1024,
            noweb=klass.noweb,
            noapi=klass.noapi,
            nohang=klass.nohang,
            timeout=klass.timeout,
            hexdump=klass.hexdump,
            nocraft=klass.nocraft,
            logreq=True,
            logresp=True,
            explain=True
        )

    @classmethod
    def tearDownAll(self):
        self.d.shutdown()
        shutil.rmtree(self.confdir)

    def setUp(self):
        if not (self.noweb or self.noapi):
            self.d.clear_log()

    def getpath(self, path, params=None):
        scheme = "https" if self.ssl else "http"
        return requests.get(
            "%s://localhost:%s/%s" % (
                scheme,
                self.d.port,
                path
            ),
            verify=False,
            params=params
        )

    def get(self, spec):
        return requests.get(self.d.p(spec), verify=False)

    def pathoc(
        self,
        specs,
        timeout=None,
        connect_to=None,
        ssl=None,
        ws_read_limit=None,
        use_http2=False,
    ):
        """
            Returns a (messages, text log) tuple.
        """
        if ssl is None:
            ssl = self.ssl
        logfp = cStringIO.StringIO()
        c = pathoc.Pathoc(
            ("localhost", self.d.port),
            ssl=ssl,
            ws_read_limit=ws_read_limit,
            timeout=timeout,
            fp=logfp,
            use_http2=use_http2,
        )
        c.connect(connect_to)
        ret = []
        for i in specs:
            resp = c.request(i)
            if resp:
                ret.append(resp)
        for frm in c.wait():
            ret.append(frm)
        c.stop()
        return ret, logfp.getvalue()


@contextmanager
def tmpdir(*args, **kwargs):
    orig_workdir = os.getcwd()
    temp_workdir = tempfile.mkdtemp(*args, **kwargs)
    os.chdir(temp_workdir)

    yield temp_workdir

    os.chdir(orig_workdir)
    shutil.rmtree(temp_workdir)


def raises(exc, obj, *args, **kwargs):
    """
        Assert that a callable raises a specified exception.

        :exc An exception class or a string. If a class, assert that an
        exception of this type is raised. If a string, assert that the string
        occurs in the string representation of the exception, based on a
        case-insenstivie match.

        :obj A callable object.

        :args Arguments to be passsed to the callable.

        :kwargs Arguments to be passed to the callable.
    """
    try:
        obj(*args, **kwargs)
    except (Exception, SystemExit) as v:
        if isinstance(exc, basestring):
            if exc.lower() in str(v).lower():
                return
            else:
                raise AssertionError(
                    "Expected %s, but caught %s" % (
                        repr(str(exc)), v
                    )
                )
        else:
            if isinstance(v, exc):
                return
            else:
                raise AssertionError(
                    "Expected %s, but caught %s %s" % (
                        exc.__name__, v.__class__.__name__, str(v)
                    )
                )
    raise AssertionError("No exception raised.")

test_data = utils.Data(__name__)


def render(r, settings=language.Settings()):
    r = r.resolve(settings)
    s = cStringIO.StringIO()
    assert language.serve(r, s, settings)
    return s.getvalue()
