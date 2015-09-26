%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
<p>Edit the task with ID = {{no}}</p>
<form action="/edit/{{no}}" method="get">
Text<input type="text" name="Task" value="{{old[0]}}" size="100" maxlength="100">
<br/>
Time<input type="text" name="Time" value="" size="100" maxlength="100">
<br/>
Cost<input type="text" name="Cost" value="" size="100" maxlength="100">
<br/>
Priority<input type="text" name="Priority" value="" size="100" maxlength="100">
<br/>
Status<input type="text" name="Status" value="" size="100" maxlength="100">
<br/>
<input type="submit" name="save" value="save">
</form>