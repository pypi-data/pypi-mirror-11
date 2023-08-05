=====================
 Development Roadmap
=====================

.. epigraph::

   Roads?  Where we're going, we don't need roads. 

   -- Dr Emmett Brown, `Back To The Future`__

   __ http://www.imdb.com/title/tt0088763

This section contains a few notes and ideas about the future development of
|PD|.

Compatibility with original Ditz
================================

As of version 0.8, |PD| is pretty much roundtrip-compatible with the
original Ditz.  If the original were still being developed, I guess I'd try
to keep in step with it.  But it's not.  So the question is, what price
compatibility?

I think |PD| being able to read original Ditz databases is important.  I'm
not sure about the other direction: once a database has migrated to |PD|, I
don't see a use-case for going back again.

Extending the file formats
==========================

The original Ditz had hooks to support extra features, such as
issue-claiming and issue priorities.  These added new fields to the issue
files.  I intend to implement these features, but not via plugins.

This raises the problem of how to extend the file formats while maintaining
compatibility with old formats.  One idea that springs to mind is to
extend the :mod:`ditz.objects` classes with different YAML tags.  Then,
when an 'old' object is read, it can be transparently converted to a newer
one.

Adding new commands
===================

There's a case for implementing each existing command as a plugin.  Then
users can simply extend the command set by writing a plugin.  The trick is
to dynamically add :samp:`do_{name}` methods to the :class:`DitzCmd` class
after reading the plugins.
