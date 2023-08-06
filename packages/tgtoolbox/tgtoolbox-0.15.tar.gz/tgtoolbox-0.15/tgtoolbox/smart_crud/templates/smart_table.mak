<%def name="row()" >
  <div class="row">
    <div class="col-xs-12">
      ${caller.body()}
    </div>
  </div>
</%def>

<%self:row>
  <div class="btn-toolbar" role="toolbar">
    <div class="btn-group" role="group">
      %if table.can_new:
        <a href="new" class="btn btn-default">
          ${h.icon('plus')}
        </a>
      %endif
    </div>
  </div>
</%self:row>
<hr/>
${tmpl_context.paginators.data.pager() | n}
<%self:row>
  <table class="table table-striped table-hover">
    <thead>
    <tr>
      <th>#</th>
      %for col in table.columns.values():
        <th>${col.render_header() | n}</th>
      %endfor
    </tr>
    </thead>
    <tbody>
      <%
        row_counter = table.page_size * table.page_index
      %>
      %for record in table.query:
        <%
          row_counter += 1
        %>
        <tr>
          <td>${row_counter}</td>
          %for column in table.columns.values():
            <td>${table.format(record, column)}</td>
          %endfor
          <td>
            %if table.can_edit:
              <a href="${record.id}/edit" class="btn btn-default">${h.icon('pencil')}</a>
            %endif
            %if table.can_delete:
              <form method="POST" action="${record.id}?${request.query_string}" style="display: inline">
                <input type="hidden" name="_method" value="DELETE">
                <button type="submit" class="btn btn-default" onclick="return confirm('${_('Are you sure?')}')">
                  ${h.icon('trash')}
                </button>
              </form>
            %endif
          </td>
        </tr>
      %endfor
    </tbody>
  </table>
</%self:row>
<%self:row>
  ${tmpl_context.paginators.data.pager() | n}
</%self:row>

