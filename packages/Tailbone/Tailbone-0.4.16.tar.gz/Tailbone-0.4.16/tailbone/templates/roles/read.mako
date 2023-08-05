## -*- coding: utf-8 -*-
<%inherit file="/roles/crud.mako" />

${parent.body()}

<h2>Users</h2>

% if role is guest_role:

    <p>The guest role is implied for all users.</p>

% elif role.users:

        <p>The following users are assigned to this role:</p>
        <br />
        <div class="grid clickable">
          <table>
            <thead>
              <th>Username</th>
              <th>Full Name</th>
            </thead>
            <tbody>
              % for i, user in enumerate(role.users, 1):
                  <tr class="${'odd' if i % 2 else 'even'}" url="${url('user.read', uuid=user.uuid)}">
                    <td>${user.username}
                    <td>${user.display_name}</td>
                  </tr>
              % endfor
            </tbody>
          </table>
        </div>

% else:

    <p>There are no users assigned to this role.</p>

% endif
