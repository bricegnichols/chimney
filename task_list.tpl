<h1>Things to Do</h1>
<table>
<tr><th>Task</th><th>Time</th><th>Cost</th><th>Priority</th><th>Status</th></tr>
%for row in rows:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>