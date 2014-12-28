%rebase("base.tpl")

<h1>Manage Posts</h1>
<hr />

%if post_summaries:
	<h3>My Ideas</h3>
	<table class="table table-striped">
		<tr>
			<th width="250px">Date</th>
			<th>Title</th>
			<th width="200px">Action</th>
		</tr>
		%for summary in post_summaries:			
			<tr>
				<td>{{summary['t']}}</td>
				<td><a href="/post/{{summary['p']}}">{{summary['s']}}</a></td>
				<td><a href="/edit_post/{{summary['p']}}">Edit</a> | <a href="/delete_post/{{summary['p']}}">Delete</a></td>
			</tr>
		%end
	</table>
	<hr />
%end

%if feedback_summaries:
	<h3>My Feedbacks</h3>
	<table class="table table-striped">
		<tr>
			<th width="250px">Date</th>
			<th>Post Link</th>
			<th width="200px">Action</th>
		</tr>
		%for summary in feedback_summaries:
			<tr>
				<td>{{summary['t']}}</td>
				<td><a href="/post/{{summary['p']}}">{{summary['p']}}</a></td>
				<td><a href="/edit_feedback/{{summary['_id']}}">Edit</a> | <a href="/delete_feedback/{{summary['_id']}}">Delete</a></td>
			</tr>
		%end
	</table>
%end
