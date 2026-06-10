import sys

from proxycraft.shared.utilities.http_compat import HTTPMethod


def test_http_method_members():
    assert HTTPMethod.GET.value == "GET"
    assert HTTPMethod.POST.value == "POST"
    assert HTTPMethod.PUT.value == "PUT"
    assert HTTPMethod.DELETE.value == "DELETE"
    assert HTTPMethod.PATCH.value == "PATCH"
    assert HTTPMethod.HEAD.value == "HEAD"
    assert HTTPMethod.OPTIONS.value == "OPTIONS"
    assert HTTPMethod.CONNECT.value == "CONNECT"
    assert HTTPMethod.TRACE.value == "TRACE"


def test_http_method_is_str_enum():
    assert isinstance(HTTPMethod.GET, HTTPMethod)
    assert HTTPMethod.GET == "GET"
    assert HTTPMethod.GET.value == "GET"


def test_http_method_uses_stdlib_on_python_311_plus():
    if sys.version_info >= (3, 11):
        from http import HTTPMethod as StdlibHTTPMethod

        assert HTTPMethod is StdlibHTTPMethod
