%rebase('base.tpl')
%setdefault('message', '')

<div class="row">
  <div class="col-xs-12 col-sm-9">
	<p class="pull-right visible-xs">
	  <button type="button" class="btn btn-primary btn-xs" data-toggle="offcanvas">Toggle nav</button>
	</p>
	<div class="jumbotron">
	  <h2>Welcome to {{queriedUser['f'] + ' ' + queriedUser['l']}}'s page!</h2>

	  %if queriedUser['b']:  # if there is user bio
		  <p>{{queriedUser['b']}}</p>
	  %end
	</div>
	
	%if mode == 'view':
		%include('user_profile_about.tpl')
	%elif mode == 'contact':
		%include('user_profile_contact.tpl')
	%end

	
  </div><!--/.col-xs-12.col-sm-9-->

  <div class="col-xs-6 col-sm-3 sidebar-offcanvas" id="sidebar" role="navigation">
    <!--
	<img src="http://photos4.meetupstatic.com/photos/member/c/5/2/8/highres_170450472.jpeg" alt="..." class="img-thumbnail">
	-->
	<img class="img-thumbnail" src="../static/images/default_profile_image1.png" alt="sad face" width="256px" height="256px" />

	<div class="text-center">
		%if queriedUser['w']['f']:
			<a href="{{queriedUser['w']['f']}}" target="_blank"><img src="../static/images/fb_48.png" alt="facebook" /></a>
		%end
		%if queriedUser['w']['l']:
			<a href="{{queriedUser['w']['l']}}" target="_blank"><img src="../static/images/li_48.png" alt="linkedin" /></a>
		%end
		%if queriedUser['w']['o']:
			<a href="{{queriedUser['w']['o']}}" target="_blank"><img src="../static/images/o_48.png" alt="other" width="46px" height="46px" /></a>
		%end
	</div>


	<div class="list-group">
	  %if mode == 'view':
		  <a href="/user/{{queriedUser['_id']}}" class="list-group-item active text-center">About {{queriedUser['f']}}</a>
		  <a href="/contact_user/{{queriedUser['_id']}}" class="list-group-item text-center">Contact {{queriedUser['f']}}</a>
	  %elif mode == 'contact':
		  <a href="/user/{{queriedUser['_id']}}" class="list-group-item text-center">About {{queriedUser['f']}}</a>
		  <a href="/contact_user/{{queriedUser['_id']}}" class="list-group-item text-center active">Contact {{queriedUser['f']}}</a>
	  %end

	  <a class="list-group-item text-center">Name: {{queriedUser['f'] + ' ' + queriedUser['l']}}</a>	  
	  %if queriedUser['g']: 
	      <a class="list-group-item text-center">Gender: {{queriedUser['g']}}</a>
	  %end
	  %if queriedUser['a']:
    	  <a class="list-group-item text-center">Age: {{queriedUser['a']}}</a>
	  %end
	  %if queriedUser['z']:
    	  <a class="list-group-item text-center">Location: {{queriedUser['z']}}</a>
      %end

	</div>
  </div><!--/.sidebar-offcanvas-->

</div><!--/row-->
      

