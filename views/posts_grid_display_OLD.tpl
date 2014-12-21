%import math
%rowNum = int(math.ceil(len(posts) / 3.0))
%for i in range(0, rowNum):
	<div class="row">
	%postsPerRow = posts[i*3:i*3+3]
	%for post in postsPerRow:
		<div class="col-sm-4">
			<h3><a href="/post/{{post['p']}}">{{post['s']}}</a></h3>
			<!--
			Posted {{post['t']}}<br />
			-->
			<i>by <a href='/user/{{post['a']['u']}}'>{{post['a']['f']}}</a></i><br />
			{{post['lc']}} likes; <a href="#">Like</a><br />
			{{post['fc']}} feedbacks<br />
			<!-- tags display -->
			%if ('l' in post):
			<em>Tags</em>: 
				%for tag in post['l'][0:1]:
					<a href="/tag/{{tag}}">{{tag}}</a>
					%for tag in post['l'][1:]:
						, <a href="/tag/{{tag}}">{{tag}}</a>
					%end
				%end
			%end
			<!-- tags display -->
			<br /><br />
			<p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>

		</div>
	%end
	</div>
%end