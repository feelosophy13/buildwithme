%setdefault('colNum', 4)
%if colNum == 4:
	%colDivCap = '<div class="col-md-3 col-sm-6 hero-feature">'
%elif colNum == 3:
	%colDivCap = '<div class="col-sm-4 hero-feature">'
%end

%import math
%rowNum = int(math.ceil(len(posts) / float(colNum)))


%for i in range(0, rowNum):
	<div class="row text-center">
	%postsPerRow = posts[i*colNum:i*colNum+colNum]
	%for post in postsPerRow:
		<!--
		<div class="col-md-3 col-sm-6 hero-feature">
		-->
		{{!colDivCap}}
			<div class="thumbnail">			
				<img src="http://placehold.it/800x500" alt="">
				<div class="caption">
					<h3><a href="/post/{{post['p']}}">{{post['s']}}</a></h3>
					<p>
						by <a href='/user/{{post['a']['u']}}'>{{post['a']['f']}}</a>
					</p>
					
					<p>{{post['pd']}}</p>

					<p>
						<a href="#" class="btn btn-warning">Feedback</a> 

						%if str(userID) in post['i']:
							<a href="/post/{{post['p']}}#feedback" class="btn btn-success" data-permalink="{{post['p']}}">Unlike Idea</a>
						%else:
							<a href="#" class="btn btn-success" data-permalink="{{post['p']}}">Like Idea</a>
						%end

					</p>
					
					<p>
					{{post['lc']}} likes; {{post['fc']}} feedbacks<br />
					</p>

					<!-- tags display -->
					%if ('l' in post and len(post['l']) > 0):
					<em>Tags</em>: 
						%for tag in post['l'][0:1]:
							<a href="/tag/{{tag}}">{{tag}}</a>
							%for tag in post['l'][1:]:
								, <a href="/tag/{{tag}}">{{tag}}</a>
							%end
						%end
					%end
					<!-- tags display -->
				</div>
			</div>
		</div>
	%end
	</div>
%end

