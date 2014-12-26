%rebase("base.tpl")

<h1>Manage Your Ideas</h1>
<hr />

%if summaries:
	<table class="table table-striped">
		<tr>
			<th>Date</th>
			<th>Title</th>
			<th>Action</th>
		</tr>
		%for summary in summaries:			
			<tr>
				<td>{{summary['t']}}</td>
				<td><a href="/post/{{summary['p']}}">{{summary['s']}}</a></td>
				<td><a href="/edit_post/{{summary['p']}}">Edit</a> | <a href="/delete_post/{{summary['p']}}">Delete</a></td>
			</tr>
		%end
	</table>
%end

<hr />


<h3>Option 1</h3>
<table class="table table-hover">
	<tr class="active">
		<td>
			HELLO
		</td>
		<td>
			MUCH
		</td>
	</tr>
	<tr class="success">
		<td>
			Hello
		</td>
		<td>
			Much
		</td>
	</tr>
	<tr class="warning">
		<td>
			Hello
		</td>
		<td>
			Much
		</td>
	</tr>
	<tr class="danger">
		<td>
			Hello
		</td>
		<td>
			Much
		</td>
	</tr>
	<tr class="info">
		<td>
			Hello
		</td>
		<td>
			Much
		</td>
	</tr>
</table>


