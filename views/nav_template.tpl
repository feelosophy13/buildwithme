%setdefault('userID', None)
%setdefault('firstname', None)


<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <div class="container">
	<div class="navbar-header">

	  <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
		<span class="sr-only">Toggle navigation</span>
		<span class="icon-bar"></span>
		<span class="icon-bar"></span>
		<span class="icon-bar"></span>
	  </button>

	  <a class="navbar-brand" href="/">BUILD WITH ME</a>
	</div>
	<div id="navbar" class="collapse navbar-collapse">
	
		%if (userID == None):  # if user not logged in
		<div class="navbar-form navbar-right">
		 <a href="/login" class="noLinkDec"><button type="button" class="btn btn-default navbar-right">Log In</button></a>
		</div>

		<div class="navbar-form navbar-right">
		 <a href="/signup" class="noLinkDec"><button type="button" class="btn btn-info navbar-right">Sign Up</button></a>
		</div>
	  <!--
	  <form class="navbar-form navbar-right" role="form" method="post" action="/login">
		<div class="form-group">
		  <input type="text" placeholder="Email" class="form-control" name="email">
		</div>
		<div class="form-group">
		  <input type="password" placeholder="Password" class="form-control" name="password">
		</div>
		<button type="submit" class="btn btn-warning">Log in</button>
	  </form>
	  -->

		%else:  # if user logged in
		<div class="navbar-form navbar-right">
		 <a href="/newpost" class="noLinkDec"><button type="button" class="btn btn-info navbar-right">+ SUBMIT IDEA</button></a>
		</div>

		<ul class="nav navbar-nav navbar-right">
		  <li class="dropdown">
			 <a href="" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Hello, {{firstname}}! <span class="caret"></span></a>
			 <ul class="dropdown-menu" role="menu">
			   <li><a href="/user/{{userID}}">My Profile</a></li>
			   <li><a href="/edit_profile">Edit Profile</a></li>
			   <li><a href="/liked_ideas">Liked Ideas</a></li>
			   <li class="divider"></li>
			   <!--
			   <li><a href="/help">Help</a></li>
			   -->
			   <li><a href="/logout">Log out</a>
			 </ul>
		  </li>
		</ul>
		%end

		<ul class="nav navbar-nav navbar-right">
		  <li><a href="/how_it_works">How It Works</a></li> 
		</ul>
	  
	</div><!--/.nav-collapse -->
  </div>
</nav>
