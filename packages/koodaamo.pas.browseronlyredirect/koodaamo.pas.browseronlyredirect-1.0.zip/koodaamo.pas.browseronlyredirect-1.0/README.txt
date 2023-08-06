Introduction
------------

This is a modified Cookie Auth Plugin that only redirects if the UA is a browser.
The main envisioned use case is for scenarios that require an API to be built for
an existing client (that we have no control over) that does not expect redirects
to login form upon authentication.

The detection is done by comparing the request User-Agent header against some of
the most common browser user agent strings, ie. "Mozilla", "Webkit", "Opera", and
for the terminal users out there, "Lynx".

Basic installation and use:

1. Go to Zope root acl_users folder via ZMI
2. Add a "Browser-only-redirecting Cookie Auth Helper".
3. Go to "plugins" folder
4. Click "Challenge Plugins" to get to the plugin registry
5. Disable "credentials_cookie_auth" plugin
6. Add in its place the plugin (helper) you added in 2.

Make sure the plugin/helper you added is at the top so it's given a chance to
run first.

Then, try authenticating with wrong credentials. You should get a proper 401
Unauthorized response rather than the usual 302 Moved Temporarily (typically causing
redirect).
