%for post in posts:
	<div class="col-sm-3">
		<h3><a href="/post/{{post['p']}}">{{post['s']}}</a></h3>
		<p>{{post['pd']}}</p>
		on {{post['t']}}<br />
		by <a href='/user/{{post['a']['u']}}'>{{post['a']['f']}}</a>
		<br />
		<br />
		{{post['lc']}} likes;
		{{post['fc']}} feedbacks
		
		<br />
		<br />

		<!-- tags display -->
		%if ('l' in post and len(post['l']) > 0):
		Tags: 
			%for tag in post['l'][0:1]:
				<a href="/tag/{{tag}}">{{tag}}</a>
				%for tag in post['l'][1:]:
					, <a href="/tag/{{tag}}">{{tag}}</a>
				%end
			%end
		%end
		<!-- tags display -->		

		<br />
		
		%if str(userID) in post['i']:
			<div class="like"><a class="like" href="#" data-permalink={{post['p']}}>Unlike Idea</a></div>
		%else:
			<div class="like"><a class="like" href="#" data-permalink={{post['p']}}>Like Idea</a></div>
		%end
		
		<p><a class="btn btn-default" href="/post/{{post['p']}}" role="button">View details &raquo;</a></p>
	</div>
%end