import mock
from pyramid import httpexceptions

from cliquet.errors import ERRORS

from .support import BaseWebTest, unittest, authorize


class FormattedErrorMixin(object):

    def assertFormattedError(self, response, code, errno, error,
                             message=None, info=None):
        self.assertEqual(response.headers['Content-Type'],
                         'application/json; charset=UTF-8')
        self.assertEqual(response.json['code'], code)
        self.assertEqual(response.json['errno'], errno)
        self.assertEqual(response.json['error'], error)

        if message is not None:
            self.assertIn(message, response.json['message'])
        else:
            self.assertNotIn('message', response.json)

        if info is not None:
            self.assertIn(info, response.json['info'])
        else:
            self.assertNotIn('info', response.json)


class ErrorViewTest(FormattedErrorMixin, BaseWebTest, unittest.TestCase):

    sample_url = "/mushrooms"

    def assertFormattedError(self, response, code, errno, error,
                             message=None, info=None):
        self.assertEqual(response.headers['Content-Type'],
                         'application/json; charset=UTF-8')
        self.assertEqual(response.json['code'], code)
        self.assertEqual(response.json['errno'], errno)
        self.assertEqual(response.json['error'], error)

        if message is not None:
            self.assertIn(message, response.json['message'])
        else:
            self.assertNotIn('message', response.json)

        if info is not None:
            self.assertIn(info, response.json['info'])
        else:
            self.assertNotIn('info', response.json)

    def test_backoff_headers_is_not_present_if_no_error(self):
        response = self.app.get(self.sample_url,
                                headers=self.headers, status=200)
        self.assertNotIn('Backoff', response.headers)

    def test_backoff_header_is_present_on_error_responses(self):
        with mock.patch.dict(
                self.app.app.registry.settings,
                [('cliquet.backoff', 10)]):
            response = self.app.get(self.sample_url,
                                    headers=self.headers, status=200)
            self.assertIn('Backoff', response.headers)
            self.assertEquals(response.headers['Backoff'],
                              '10'.encode('utf-8'))

    def test_404_is_valid_formatted_error(self):
        response = self.app.get('/unknown', status=404)
        self.assertFormattedError(
            response, 404, ERRORS.MISSING_RESOURCE, "Not Found",
            "The resource your are looking for could not be found.")

    def test_401_is_valid_formatted_error(self):
        response = self.app.get(self.sample_url, status=401)
        self.assertFormattedError(
            response, 401, ERRORS.MISSING_AUTH_TOKEN, "Unauthorized",
            "Please authenticate yourself to use this endpoint.")

    @authorize(False)
    def test_403_is_valid_formatted_error(self):
        response = self.app.get(self.sample_url,
                                headers=self.headers, status=403)
        self.assertFormattedError(
            response, 403, ERRORS.FORBIDDEN, "Forbidden",
            "This user cannot access this resource.")

    def test_405_is_valid_formatted_error(self):
        response = self.app.patch(self.sample_url,
                                  headers=self.headers, status=405)
        self.assertFormattedError(
            response, 405, ERRORS.METHOD_NOT_ALLOWED, "Method Not Allowed",
            "Method not allowed on this endpoint.")

    def test_500_is_valid_formatted_error(self):
        with mock.patch(
                'cliquet.tests.testapp.views.Mushroom._extract_filters',
                side_effect=ValueError):
            response = self.app.get(self.sample_url,
                                    headers=self.headers, status=500)
        self.assertFormattedError(
            response, 500, ERRORS.UNDEFINED, "Internal Server Error",
            "A programmatic error occured, developers have been informed.",
            "https://github.com/mozilla-services/cliquet/issues/")

    def test_503_is_valid_formatted_error(self):
        with mock.patch(
                'cliquet.tests.testapp.views.Mushroom._extract_filters',
                side_effect=httpexceptions.HTTPServiceUnavailable):
            response = self.app.get(self.sample_url,
                                    headers=self.headers, status=503)
        self.assertFormattedError(
            response, 503, ERRORS.BACKEND, "Service Unavailable",
            "Service unavailable due to high load, please retry later.")
        self.assertIn("Retry-After", response.headers)

    def test_500_provides_traceback_on_server(self):
        mock_traceback = mock.patch('logging.traceback.print_exception')
        with mock.patch(
                'cliquet.tests.testapp.views.Mushroom._extract_filters',
                side_effect=ValueError):
            with mock_traceback as mocked_traceback:
                self.app.get(self.sample_url, headers=self.headers, status=500)
                self.assertTrue(mocked_traceback.called)
                self.assertEqual(ValueError,
                                 mocked_traceback.call_args[0][0])


class RedirectViewTest(FormattedErrorMixin, BaseWebTest, unittest.TestCase):
    api_prefix = ''

    def test_do_not_redirect_to_version_if_not_supported_version(self):
        resp = self.app.get('/v1/', status=404)
        self.assertFormattedError(
            resp, 404, ERRORS.VERSION_NOT_AVAILABLE, "Not Found",
            "The requested protocol version is not available "
            "on this server.")

    def test_redirect_to_version(self):
        # GET on the hello view.
        response = self.app.get('/')
        self.assertEqual(response.status_int, 307)
        self.assertEqual(response.location,
                         'http://localhost/v0/')

        # GET on the fields view.
        response = self.app.get('/mushrooms')
        self.assertEqual(response.status_int, 307)
        self.assertEqual(response.location,
                         'http://localhost/v0/mushrooms')

    def test_do_not_redirect_to_version_if_disabled_in_settings(self):
        # GET on the hello view.
        app = self._get_test_app({
            'cliquet.version_prefix_redirect_enabled': False
        })

        app.get('/', status=404)

    def test_querystring_is_preserved_during_redirection(self):
        response = self.app.get('/home/articles?_since=42')
        self.assertEqual(response.location,
                         'http://localhost/v0/home/articles?_since=42')
