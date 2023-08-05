import pyparsing as pp

from netlib import http_status, http_uastrings
from . import base, message

"""
    Normal HTTP requests:
        <method>:<path>:<header>:<body>
    e.g.:
        GET:/
        GET:/:h"foo"="bar"
        POST:/:h"foo"="bar":b'content body payload'

    Normal HTTP responses:
        <code>:<header>:<body>
    e.g.:
        200
        302:h"foo"="bar"
        404:h"foo"="bar":b'content body payload'

    Individual HTTP/2 frames:
        h2f:<payload_length>:<type>:<flags>:<stream_id>:<payload>
    e.g.:
        h2f:0:PING
        h2f:42:HEADERS:END_HEADERS:0x1234567:foo=bar,host=example.com
        h2f:42:DATA:END_STREAM,PADDED:0x1234567:'content body payload'
"""

def get_header(val, headers):
    """
        Header keys may be Values, so we have to "generate" them as we try the
        match.
    """
    for h in headers:
        k = h.key.get_generator({})
        if len(k) == len(val) and k[:].lower() == val.lower():
            return h
    return None


class _HeaderMixin(object):
    unique_name = None

    def values(self, settings):
        return (
            self.key.get_generator(settings),
            self.value.get_generator(settings),
        )

class _HTTP2Message(message.Message):
    @property
    def actions(self):
        return []  # self.toks(actions._Action)

    @property
    def headers(self):
        headers = self.toks(_HeaderMixin)

        if not self.raw:
            if not get_header("content-length", headers):
                if not self.body:
                    length = 0
                else:
                    length = len(self.body.string())
                headers.append(
                    Header(
                        base.TokValueLiteral("content-length"),
                        base.TokValueLiteral(str(length)),
                    )
                )
        return headers

    @property
    def raw(self):
        return bool(self.tok(Raw))

    @property
    def body(self):
        return self.tok(Body)

    def resolve(self, settings):
        return self


class Code(base.Integer):
    pass


class Method(base.OptionsOrValue):
    options = [
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
    ]


class Path(base.Value):
    pass


class Header(_HeaderMixin, base.KeyValue):
    preamble = "h"


class ShortcutContentType(_HeaderMixin, base.Value):
    preamble = "c"
    key = base.TokValueLiteral("content-type")


class ShortcutLocation(_HeaderMixin, base.Value):
    preamble = "l"
    key = base.TokValueLiteral("location")


class ShortcutUserAgent(_HeaderMixin, base.OptionsOrValue):
    preamble = "u"
    options = [i[1] for i in http_uastrings.UASTRINGS]
    key = base.TokValueLiteral("user-agent")

    def values(self, settings):
        value = self.value.val
        if self.option_used:
            value = http_uastrings.get_by_shortcut(value.lower())[2]

        return (
            self.key.get_generator(settings),
            value
        )


class Raw(base.CaselessLiteral):
    TOK = "r"


class Body(base.Value):
    preamble = "b"


class Times(base.Integer):
    preamble = "x"


class Response(_HTTP2Message):
    unique_name = None
    comps = (
        Header,
        Body,
        ShortcutContentType,
        ShortcutLocation,
        Raw,
    )

    def __init__(self, tokens):
        super(Response, self).__init__(tokens)
        self.rendered_values = None
        self.stream_id = 0

    @property
    def code(self):
        return self.tok(Code)

    @classmethod
    def expr(cls):
        parts = [i.expr() for i in cls.comps]
        atom = pp.MatchFirst(parts)
        resp = pp.And(
            [
                Code.expr(),
                pp.ZeroOrMore(base.Sep + atom)
            ]
        )
        resp = resp.setParseAction(cls)
        return resp

    def values(self, settings):
        if self.rendered_values:
            return self.rendered_values
        else:
            headers = [header.values(settings) for header in self.headers]

            body = self.body
            if body:
                body = body.string()

            self.rendered_values = settings.protocol.create_response(
                self.code.string(),
                self.stream_id,
                headers,
                body)
            return self.rendered_values

    def spec(self):
        return ":".join([i.spec() for i in self.tokens])


class NestedResponse(base.NestedMessage):
    preamble = "s"
    nest_type = Response


class Request(_HTTP2Message):
    comps = (
        Header,
        ShortcutContentType,
        ShortcutUserAgent,
        Raw,
        NestedResponse,
        Body,
        Times,
    )
    logattrs = ["method", "path"]

    def __init__(self, tokens):
        super(Request, self).__init__(tokens)
        self.rendered_values = None

    @property
    def method(self):
        return self.tok(Method)

    @property
    def path(self):
        return self.tok(Path)

    @property
    def nested_response(self):
        return self.tok(NestedResponse)

    @property
    def times(self):
        return self.tok(Times)

    @classmethod
    def expr(cls):
        parts = [i.expr() for i in cls.comps]
        atom = pp.MatchFirst(parts)
        resp = pp.And(
            [
                Method.expr(),
                base.Sep,
                Path.expr(),
                pp.ZeroOrMore(base.Sep + atom)
            ]
        )
        resp = resp.setParseAction(cls)
        return resp

    def values(self, settings):
        if self.rendered_values:
            return self.rendered_values
        else:
            path = self.path.string()
            if self.nested_response:
                path += self.nested_response.parsed.spec()

            headers = [header.values(settings) for header in self.headers]

            body = self.body
            if body:
                body = body.string()

            self.rendered_values = settings.protocol.create_request(
                self.method.string(),
                path,
                headers,
                body)
            return self.rendered_values

    def spec(self):
        return ":".join([i.spec() for i in self.tokens])

def make_error_response(reason, body=None):
    tokens = [
        Code("800"),
        Body(base.TokValueLiteral("pathod error: " + (body or reason))),
    ]
    return Response(tokens)


# class Frame(message.Message):
#     pass
