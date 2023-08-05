<%inherit file="base.mako"/>
<%namespace name="lib" file="lib.mako"/>

% if logged_in is not None :
  <h2>
        <span class="label label-default">Dashboard</span>

        % if logged_in is not None and request.registry.settings['hg_delivery.default_login'] == request.authenticated_userid:
        <button type="button" style="background-color:transparent;border:none" onclick="$('#new_project_dialog').modal('show');" alt="add new project">
          <span class='glyphicon glyphicon-plus' style="font-size:26px;vertical-align:bottom"></span>
        </button>
        % endif
  </h2>
  %for project in dashboard_list :
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3 class="panel-title"><a
href="${url(route_name='project_edit',id=project.id)}"><b>${project.name}</b></a><i> (revision : ${nodes_description[project.id].get('rev','UNKNOWN')})</i></h3>
      </div>
      <div class="panel-body">
        current branch : <span class="label label-warning"> ${nodes_description[project.id].get('branch','UNKNOWN')}</span
        <br>
        <br>
        current hash : <i>${nodes_description[project.id].get('node','UNKNOWN')}</i>
        <br>
        current comment : <i>${nodes_description[project.id].get('desc','UNKNOWN')}</i>
      </div>
    </div>
  %endfor
  %if not dashboard_list :
      > <i>The dashboard is empty</i>
  %endif

% else :

 <div class="starter-template">
   <h1>Welcome to HgDelivery webapp</h1>
   <p class="lead">The purpose of HgDelivery webapp is to allow people to deliver or manage new release easily</p>
   <br>
   <br>
   <br>
   <br>
   <p class="lead"><b>Please login before proceeding</b></p>
 </div>

% endif

% if logged_in is not None :
   ${lib.publish_project_dialog()}
% endif

<%block name="local_js">
</%block>


