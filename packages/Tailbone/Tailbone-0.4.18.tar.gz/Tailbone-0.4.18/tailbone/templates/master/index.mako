## -*- coding: utf-8 -*-
## ##############################################################################
## 
## Default master 'index' template.  Features a prominent data table and
## exposes a way to filter and sort the data, etc.
## 
## ##############################################################################
<%inherit file="/base.mako" />

<%def name="title()">${grid.model_title_plural}</%def>

<%def name="context_menu_items()">
  % if request.has_perm('{0}.create'.format(grid.permission_prefix)):
      <li>${h.link_to("Create a new {0}".format(grid.model_title), url('{0}.create'.format(grid.route_prefix)))}</li>
  % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

${grid.render_complete()|n}
