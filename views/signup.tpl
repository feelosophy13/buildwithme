%rebase('base.tpl')
%setdefault('error', '')

<div class="row">
   <div class="col-sm-6 col-sm-offset-3">

	 <h1 class="text-center">Signup</h1>
	 <br />
	 
	 <form class="form-horizontal" role="form" method="POST">
	   <div class="form-group">
		 <label for="firstname" class="col-sm-4 control-label">First Name</label>
		 <div class="col-sm-8">
		   <input type="text" class="form-control" id="firstname" name="firstname" placeholder="First Name" value="{{user_signup['f']}}" maxlength="30">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="lastname" class="col-sm-4 control-label">Last Name</label>
		 <div class="col-sm-8">
		   <input type="lastname" class="form-control" id="lastname" name="lastname" placeholder="Last Name" value="{{user_signup['l']}}" maxlength="30">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="emailID" class="col-sm-4 control-label">Email Address</label>
		 <div class="col-sm-8">
		   <input type="email" class="form-control" id="emailID" name="emailID" placeholder="Email Address" value="{{user_signup['e']}}">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="password1" class="col-sm-4 control-label">Password</label>
		 <div class="col-sm-8">
		   <input type="password" class="form-control" id="password" name="password" placeholder="Password" value="" maxlength="30">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="password2" class="col-sm-4 control-label">Confirm Password</label>
		 <div class="col-sm-8">
		   <input type="password" class="form-control" id="password2" name="password2" placeholder="Password" value="" maxlength="30">
		 </div>
	   </div>
	   <div class="form-group">
		 <div class="col-sm-offset-5 col-sm-2">
		   <button type="submit" class="btn btn-default">Sign Up</button>
		 </div>
	   </div>
	 </form>

	 %if error:
	   <div class="alert alert-danger text-center" role="alert">
		 {{error}}
	   </div>
	 %end

	 <p class='text-center'>
	 	Already a user? <a href="/login">Log in</a>.
	 </p>
	 
	 <hr />
	 
  </div>
</div>
	 