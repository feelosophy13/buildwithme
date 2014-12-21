%rebase('base.tpl')
%setdefault("error", "")


<div class="row">
   <div class="col-sm-6 col-sm-offset-3">

	 <h2>Update Password</h2>
	 <br />
	 <form class="form-horizontal" role="form" method="POST">
	   <div class="form-group">
		 <label for="current_password" class="col-sm-4 control-label">Current Password</label>
		 <div class="col-sm-8">
		   <input type="password" class="form-control" id="current_password" name="current_password" placeholder="Current Password" value="" maxlength="30">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="new_password" class="col-sm-4 control-label">New Password</label>
		 <div class="col-sm-8">
		   <input type="password" class="form-control" id="new_password" name="new_password" placeholder="New Password" value="" maxlength="30">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="new_password2" class="col-sm-4 control-label">Verify Password</label>
		 <div class="col-sm-8">
		   <input type="password" class="form-control" id="new_password2" name="new_password2" placeholder="New Password" value="" maxlength="30">
		 </div>
	   </div>
	   <div class="form-group">
	     <div class="col-sm-offset-5 col-sm-2">
	       <button type="submit" class="btn btn-default">Update Password</button>
	     </div>
	     <!--
		 <div class="col-sm-offset-2 col-sm-10">
		   <button type="submit" class="btn btn-default">Sign in</button>
		 </div>
		 -->
	   </div>
	 </form>
	 <br />

	 %if error:
	   <div class="alert alert-danger text-center" role="alert">
		 {{error}}
	   </div>
	 %end

	 <hr />
	 
  </div>
</div>
	 