<h1>Things to Do</h1>
<table>
<tr><th>Task</th><th>Time</th><th>Cost</th><th>Priority</th><th>Status</th></tr>
%for row in rows:
    %print row
    %Task, Time, Cost, Priority, Status, rowid = row
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    <td><a href="/edit/{{rowid}}"> Edit</a></td>
    </tr>
%end
</table>