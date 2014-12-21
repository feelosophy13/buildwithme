<!-- posts start -->
%for post in myposts:
%permalink = post['p']
<div class="panel panel-default">
  <div class="panel-heading">
  	<!-- <div class="like"><a class="like" href="#" data-permalink={{permalink}}>Like</a></div> -->
    <h3 class="panel-title"><b>{{post['t']}}</b></h3>
  </div>
      
  <div class="panel-body">
  	<div class='largeFontSize'>
	{{!post['b']}}<br />
	</div>
	<br />
	
	<div class="commentCount">
	<a href="/post/{{post['p']}}">
	%if ('c' in post):
	%numComments = len(post['c'])
	%else:
	%numComments = 0
	%end
	{{numComments}} comments</a>	
	</div>

	</div>
	</div>
<hr />
%end
<!-- posts end -->



<nav>
  <ul class="pager">
    %if (previous_page_exists == True):
    <li class="previous"><a href="/{{previous_page_num}}">&larr; Newer</a></li>
    %end
    %if (next_page_exists == True):
    <li class="next"><a href="/{{next_page_num}}">Older &rarr;</a></li>
    %end
  </ul>
</nav>