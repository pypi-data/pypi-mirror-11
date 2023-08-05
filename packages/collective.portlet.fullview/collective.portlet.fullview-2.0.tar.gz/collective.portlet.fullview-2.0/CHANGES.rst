Changelog
=========

2.0 (2015-07-15)
----------------

- Remove plone.memoize instance caches to avoid read on writes.
  [thet]

- Cache the rendered portlet for an hour with sensible cache keys (portlet id,
  path, modification date, user).
  [thet]

- Make the content selection field ``content_uid`` required.
  [thet]

- Don't fail if the portlet was added but no content item can be found.
  [thet]

- Add an ``omit_border`` option to render a div instead of the dl/dt/dd
  structure.
  [datakurre]

- Register the ``RelatedItemsFieldWidget`` adapter for this package's browser
  layer to not conflict with the registration provided in ``plone.app.z3cform``
  in Plone 5.
  [thet]

- Skip portlethash check when it's None for minimal support for
  collective.panels.
  [datakurre]

- Add setuptools entrypoint for Plone.
  [datakurre]

- Fix translation of portlet summary.
  [datakurre]

- Add Finnish localization.
  [datakurre]

- Fix path to uninstall profiles.
  [thet]

- Rename methods, make them properties, use memoize for portlethash.
  [thet]

- Don't call the fullview context object unintended in the templates. This had
  the side effect, of the edit-bar not being rendered.
  [thet]

- Move the content's title into the portlet header.
  [thet]

- Allow fullview portlets to be derived while making sure, they don't run into
  an infinite recursion loop. This is done via annotating the request with the
  portlet hash.
  [thet]

- Return the content object's title for the management screen portlet title to
  better distinguish several portlets.
  [thet]

- Use the ``RelatedItemsFieldWidget`` from ``plone.app.widgets`` and switch to
  a ``z3c.form`` based implementation.
  [thet]


1.1 (2015-03-06)
----------------

- Only render the fullview portlet, if it's rendered on a context where it is
  directly assigned. Don't render, if it was derived from a parent context.
  This avoids infinite loops when a fullview portlets renders a childitem.
  [thet]


1.0 (2015-03-04)
----------------

- Initial version.
  [thet]
