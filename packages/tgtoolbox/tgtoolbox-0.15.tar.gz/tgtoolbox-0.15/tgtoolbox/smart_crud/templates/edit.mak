<%inherit file="local:templates.admin.master"/>
<%def name="title()">${tmpl_context.title} - ${model}</%def>
<%include file="local:apps.root.views.partial.flash" />
<div class="row">
  <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-3 col-md-offset-0">
    <h2>Edit ${model}</h2>
  </div>
</div>
<hr/>
<div class="row">
  <div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-3 col-md-offset-0">
    ${tmpl_context.widget(value=value, action='./') | n}
  </div>
</div>

