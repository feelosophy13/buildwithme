%rebase('base.tpl')

%if userID:  # if user is logged in
<div class="starter-template">
   <h1>Welcome to Build With Me!</h1>
   <p class="lead">A place to bring ideas into reality.</p>
</div>
%else:  # if user is not logged in
<header class="jumbotron hero-spacer">
	<h1>Welcome to Build With Me!</h1>
	<p>A place to bring ideas into reality.</p>
	<p><a href="/signup" class="btn btn-primary btn-large">Sign Up Now!</a>
	</p>
</header>
%end

<hr>

<div class="row">
	%include('posts_grid_display.tpl')
</div>

