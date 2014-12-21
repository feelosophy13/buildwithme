%rebase('base.tpl')
%setdefault('emailID', '')


<div class="row">
   <div class="col-md-6 col-md-offset-3"><!-- centering the posts in the middle -->

	 <h2 class='text-center'>Login</h2>
	 <br />

   <form class="form-horizontal" role="form" method="post">
	 <div class="form-group">
	   <label for="emailID" class="col-sm-3 control-label">Email Address</label>
	   <div class="col-sm-9">
		 <input type="email" class="form-control" name="emailID" placeholder="Email Address" value="{{emailID}}">
	   </div>
	 </div>

	 <div class="form-group">
	   <label for="password" class="col-sm-3 control-label">Password</label>
	   <div class="col-sm-9">
		 <input type="password" class="form-control" id="password" name="password" placeholder="Password">
	   </div>
	 </div>

	 <div class="form-group">
	   <div class="col-sm-offset-5 col-sm-2">
		 <button type="submit" class="btn btn-default text-center">Log In</button>
	   </div>
	 </div>
   </form>
   
   %if error:
   <div class="alert alert-danger text-center" role="alert">
	 {{error}}
   </div>
   %end

   <p class='text-center'>
	   Don't have an account? Hey, it's free! <a href="/signup">Sign up</a>.
   </p>

   <hr />
   </div>
</div>