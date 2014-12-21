<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>F*ck My Life @ UNLV</title>

    <!-- Bootstrap core CSS -->
    <link href="../static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="../static/css/starter-template.css" rel="stylesheet">
    <link href="../static/css/custom.css" rel="stylesheet">
    
    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="../static/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">UNLV FML</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">

		  <!--
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Post Your FML</a></li>
          </ul> 
          
          <div class="navbar-form navbar-right">
          <button type="button" class="btn btn-default navbar-right">
				<a href='www.facebook.com'>Sign up</a>
			</button>
			</div>
          -->
          
			%if (username == None or len(username) == 0):
          <div class="navbar-form navbar-right">
     	     <a href="/signup" class="noLinkDec"><button type="button" class="btn btn-default navbar-right">Sign up</button></a>
			</div>

          <form class="navbar-form navbar-right" role="form" method="post" action="/login">
            <div class="form-group">
              <input type="text" placeholder="Email" class="form-control" name="email"">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" class="form-control" name="password">
            </div>
            <button type="submit" class="btn btn-danger">Log in</button>
          </form>
          
			%else:
			<div class="navbar-form navbar-right">
     	     <a href="/logout" class="noLinkDec"><button type="button" class="btn btn-default navbar-right">Log out</button></a>
			</div>

			<div class="navbar-form navbar-right">
     	     <a href="/newpost" class="noLinkDec"><button type="button" class="btn btn-danger navbar-right">Post FML</button></a>
			</div>

			<p id="navbar-greeting">
				Hello, {{username}}!
			</p>
			%end

          
        
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">

      <div class="starter-template">
      	<img src="http://graphics.fansonly.com/schools/unlv/trads/images/unlv-2006-logo.gif" alt="UNLV logo" width="170px" height="140px">
        <h1>F*ck My Life @ UNLV</h1>
        <p class="lead">Slept through an exam? A Justin Bieber fan?<br />
        Whatever it is, <a href = '/newpost'>share your stories</a>!</p>
		<hr />

<div class="row">
  <div class="col-md-6 col-md-offset-3"><!-- centering content in the middle -->



<!-- FML posts start -->
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
<!-- FML posts end -->



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

  </div><!-- centering content in the middle -->
</div>

      </div>
      <footer>
        <p>&copy; FML@UNLV 2014</p>
      </footer>

    </div><!-- /.container -->



    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="../static/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../static/js/ie10-viewport-bug-workaround.js"></script>
    
    <!-- import custom JS functions -->
    <script src="../static/js/custom.js"></script>

  </body>
</html>
