%rebase('base.tpl')
%setdefault('error', '')

<div class="row">
   <div class="col-md-6 col-md-offset-3"><!-- centering the posts in the middle -->

	 <h2 class='text-center'>Confirm Signup</h2>
	 <br />
	 <br />

	<form class="form-horizontal" role="form" method="post">
	  <div class="form-group">
		<label for="emailID" class="col-sm-3 control-label">Email Address</label>
		<div class="col-sm-9">
		  <input type="email" class="form-control" name="emailID" placeholder="Email Address" value="{{emailID}}">
		</div>
	  </div>

	  <div class="form-group">
		<div class="col-sm-offset-3 col-sm-3">
		  <button type="submit" class="btn btn-default text-center">Confirm Signup</button>
		</div>
	  </div>
	</form>

	%if error:
	<div class="alert alert-danger text-center" role="alert">
	  {{error}}
	</div>
	%end

    </div>
</div>