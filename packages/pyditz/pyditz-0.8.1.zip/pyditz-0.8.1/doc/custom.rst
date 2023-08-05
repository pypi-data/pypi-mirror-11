===============
 Customization
===============

There are several ways to customize the way |PD| operates.  The most basic
is to adjust the settings in your :doc:`guide/config`.  But you can also
change the look and feel of the exported issue database, and add your own
export formats.  This section tells you how to do these things.

Customizing exported data
=========================

|PD| uses two types of file when exporting its data: *static* files, and
*template* files.  Static files are copied verbatim from where they're
found into the destination directory, whereas template files are modified
by inserting content into them at various points (and typically reference
the static files).  The engine used to insert template content is Jinja2_.

Static and template files for the builtin export formats are found by
default in |PD|\'s installed package directory.  But other places are
searched first, and this is where you can put customized files to override
things.  The search path for files is (in order of searching):

#. The directory where issues are stored for the project
#. |RCPATH|
#. |PD|\'s installed package directory

When exporting issues in a given format, |PD| looks in each of these
directories for subdirectories:

:samp:`{DIR}/static/{FORMAT}`
    Static files for the export format

:samp:`{DIR}/templates/{FORMAT}`
    Template files for the export format

Modifying static files
----------------------

So, for example, if you wanted to modify the stylesheet for the HTML output
for a particular |PD| project, you could do the following:

#. Generate HTML normally.

#. Copy the ``style.css`` file from the generated output to
   :samp:`{ISSUEDIR}/static/html/style.css`.

#. Modify ``style.css`` as required, putting any extra static files (e.g.,
   images referenced by the style sheet) in the same directory.

If you wanted to modify the stylesheet for *all* |PD| projects, you'd copy
the files into subdirectories of |RCPATH| instead.

Modifying template files
------------------------

If you want to modify a template, the same procedure applies: copy the
appropriate template file from the |PD| installation directory to the
corresponding place below either the project issue directory or |RCPATH|,
and modify it.  This involves knowing how Jinja2_ templating works (which I
will summarize here when I get around to it |GRIN|).

Builtin export formats
----------------------

At the moment, there's only one builtin export format: HTML.  It has these
static files:

    ``style.css``: The HTML style sheet.

    ``sorttable.js``: Some JavaScript to enable sorting of HTML tables.
    Referenced by the style sheet.

    ``*.png``: The small images used to illustrate issue status, next to
    their titles, in the output.

and these template files:

    ``base.html``: The base HTML page template all the others are derived
    from.

    ``index.html``: Template for the main index page.

    ``issue.html``: Template for a single issue page.

    ``component.html``: Template for a component page.

    ``release.html``: Template for a release summary page.

    ``unassigned.html``: Template for the page of issues unassigned to any
    release.

    ``macros.html``: Comon Jinja macros used by the other templates.

.. _export-plugins:

Creating new export formats
===========================

You can write your own |PD| export formats by writing a :doc:`plugin
<plugin>` which subclasses the :class:`Exporter` class.  An exporter has a
bunch of class attributes which you should set appropriately:

.. autoattribute:: ditz.exporter.Exporter.name
.. autoattribute:: ditz.exporter.Exporter.description
.. autoattribute:: ditz.exporter.Exporter.suffix
.. autoattribute:: ditz.exporter.Exporter.static_dir
.. autoattribute:: ditz.exporter.Exporter.template_dir

What happens during export
--------------------------

Here's an outline of what happens on export:

#. The :func:`setup` method is called, to initialise Jinja filters and
   export configuration variables.  Here's where you can define filters
   (via :func:`add_filter`) or configuration variables (via
   :func:`add_config`).  The exporter :attr:`db` attribute is the Ditz
   issue database being exported, which you can use to set up the filters.

   .. automethod:: ditz.exporter.Exporter.setup
   .. automethod:: ditz.exporter.Exporter.add_filter
   .. automethod:: ditz.exporter.Exporter.add_config

#. The :func:`write` method is called to do the actual exporting.  If using
   templates, this should use the :func:`render` method to render them.

   The :func:`export_filename` method is available to create a standard
   filename for each issue database item, using the exporter suffix.  Or,
   you can generate your own.

   .. automethod:: ditz.exporter.Exporter.write
   .. automethod:: ditz.exporter.Exporter.render
   .. automethod:: ditz.exporter.Exporter.export_filename

The exporter has several attribute objects which can be used during setup
and export:

* The :attr:`db` attribute is a :class:`DitzDB` object---see the next
  section for details.

* The :attr:`config` attribute is a :class:`ConfigSection` object which
  allows you to access those settings of the user configuration file which
  control the export:

  .. automethod:: ditz.config.ConfigSection.get
  .. automethod:: ditz.config.ConfigSection.getint
  .. automethod:: ditz.config.ConfigSection.getfloat
  .. automethod:: ditz.config.ConfigSection.getboolean

Structure of a |PD| database
============================

.. warning::

   This API may change incompatibly before |PD| 1.0.

.. _ditzdb:

The top-level :class:`DitzDB` object
------------------------------------

.. autoattribute:: ditz.database.DitzDB.project
.. autoattribute:: ditz.database.DitzDB.issues
.. autoattribute:: ditz.database.DitzDB.issue_events
.. automethod:: ditz.database.DitzDB.convert_to_name

The :class:`Project` object
---------------------------

.. autoattribute:: ditz.objects.Project.name
.. autoattribute:: ditz.objects.Project.components
.. autoattribute:: ditz.objects.Project.releases

The :class:`Component` objects
------------------------------

.. autoattribute:: ditz.objects.Component.name

The :class:`Release` objects
----------------------------

.. autoattribute:: ditz.objects.Release.name
.. autoattribute:: ditz.objects.Release.released

The :class:`Issue` objects
--------------------------

.. autoattribute:: ditz.objects.Issue.attributes
.. autoattribute:: ditz.objects.Issue.name
.. autoattribute:: ditz.objects.Issue.closed
.. autoattribute:: ditz.objects.Issue.progresstime
.. autoattribute:: ditz.objects.Issue.references
.. autoattribute:: ditz.objects.Issue.log_events
