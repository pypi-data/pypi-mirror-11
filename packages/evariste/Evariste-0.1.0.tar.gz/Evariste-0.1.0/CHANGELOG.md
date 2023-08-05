* Version 0.1.0 (2015-08-17)

  * Licence: Switched from GPL to AGPL.
  * Various setup.py improvements
  * Core
    * Python 3.5 support
    * Implemented multiprocessing
    * Sanitize the way path are handled
    * Many many internal fixes and improvements.
    * Now uses pygit2 version 0.22
  * Plugins
    * Improved management and loading
    * Added hooks
    * Improved selection (enable/disable setup options, default and required plugins, dependencies).
    * Renderers
      * htmllog: Removed draft. Will be addded later.
      * htmlbox: New html renderer, with CSS.
      * html: Various improvements.
      * text: New simple text renderer.
    * VCS
      * Git: Improved support (submodules, files added but not committed, code speed, etc.)
    * Actions
      * LaTeX: Various improvements.
      * Raw: Changed default behavior. By default, everything is rendered.
      * Command
        * Fixed bugs with shell commands (quotes and ampersands are now supported)
        * Merged command and multicommand actions into command
  * Command line
    * Compilation is independent from current working directory
    * Added -j and -B options
    * Default value for arguments can be set in setup file
  * Tests
    * Wrote tests. Will be completed in next version.
  * Documentation
    * Wrote draft
  * evs tools
    * New evs tool
    * New evs-cache tool

    -- Louis Paternault <spalax@gresille.org>

* Version 0.0.0 (2015-03-20)

  * First published version. Works, but with few options, and no documentation.

    -- Louis Paternault <spalax@gresille.org>
