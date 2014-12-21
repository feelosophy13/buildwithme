%rebase('base.tpl')

<div class="row">
   <div class="col-sm-6 col-sm-offset-3">
	 <h2 class="text-center">Edit Profile Information</h2>
	 <br />
	 <form class="form-horizontal" role="form" method="POST">
	   <div class="form-group">
		 <label for="emailID" class="col-sm-3 control-label">Email Address</label>
		 <div class="col-sm-9">
		   <input disabled type="email" class="form-control" id="emailID" name="emailID" placeholder="Email Address" value="{{user['e']}}">
		 </div>
	   </div>

	   <div class="form-group">
		 <label for="firstname" class="col-sm-3 control-label">First Name</label>
		 <div class="col-sm-9">
		   <input type="text" class="form-control" id="firstname" name="firstname" placeholder="John" value="{{user['f']}}">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="lastname" class="col-sm-3 control-label">Last Name</label>
		 <div class="col-sm-9">
		   <input type="lastname" class="form-control" id="lastname" name="lastname" placeholder="Doe" value="{{user['l']}}">
		 </div>
	   </div>
	   
	   <div class="form-group">
		 <label for="bio" class="col-sm-3 control-label">Brief Bio</label>
		 <div class="col-sm-9">
			<textarea class="form-control" rows="5" id="bio" placeholder="Where's your awesome intro?" name="bio" maxlength="800"
			onKeyDown="limitText(this.form.limitedtextarea, this.form.countdown, 800);"
			onKeyUp="limitText(this.form.bio, this.form.countdown, 800);">{{user['b']}}</textarea>
		 </div>
	   </div>
	   <div class="form-group text-center">
	   	<font size="2">You have <input readonly type="text" name="countdown" class="word_countdown" size="1" value="800"> characters left.</font>
	   </div>

	   <div class="form-group">
		 <label for="birthYear" class="col-sm-3 control-label">Birth Year</label>
		 <div class="col-sm-9">
		   <input type="text" class="form-control" id="birthYear" name="birthYear" placeholder="e.g. 1985" value="{{user['y']}}">
		 </div>
	   </div>
 
	   <div class="form-group">
		 <label for="" class="col-sm-3 control-label">URLs</label>
		 <div class="col-sm-9">
		   <input type="url" class="form-control" id="facebookURL" name="facebookURL" placeholder="Facebook URL including https://" value="{{user['w']['f']}}">
		 </div>
	   </div>	   
	   <div class="form-group">
		 <label for="" class="col-sm-3 control-label"></label>
		 <div class="col-sm-9">
		   <input type="url" class="form-control" id="linkedInURL" name="linkedInURL" placeholder="LinkedIn URL including https://" value="{{user['w']['l']}}">
		 </div>
	   </div>
	   <div class="form-group">
		 <label for="" class="col-sm-3 control-label"></label>
		 <div class="col-sm-9">
		   <input type="url" class="form-control" id="otherURL" name="otherURL" placeholder="Other URL including http://" value="{{user['w']['o']}}">
		   <small>Make sure to include <strong>http://</strong> or <strong>https://</strong> in your URLs!</small>
		 </div>
	   </div>
	   
	   <div class="form-group">
		 <label for="zip" class="col-sm-3 control-label">Postal ZIP</label>
		 <div class="col-sm-9">
		   <input type="text" class="form-control" id="zip" name="zip" placeholder="e.g. 89119" value="{{user['z']}}">
		 </div>
	   </div>
	   
	   
	   <div class="form-group">
	       <label for="gender" class="col-sm-3 control-label">Gender</label>
	       <div class="col-sm-9">
	          %if user['g'] == '':
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="m"> Male
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="f"> Female
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="o"> Other
				 </label>	       
	          %elif user['g'] == 'male':
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="m" checked> Male
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="f"> Female
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="o"> Other
				 </label>
			  %elif user['g'] == 'female':
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="m"> Male
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="f" checked> Female
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="o"> Other
				 </label>
			  %else:
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="m"> Male
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="f"> Female
				 </label>
				 <label class="radio-inline">
				   <input type="radio" name="gender" value="o" checked> Other
				 </label>
			  %end
			  
			  
			  
			</div>
	   </div>

	   <div class="form-group">
	     <div class="col-sm-offset-3 col-sm-6">
		     <a href="/change_password">Change my password.</a>
		 </div>
	   </div>	   
	   
	   <div class="form-group">
	     <div class="col-sm-offset-5 col-sm-2">
	       <button type="submit" class="btn btn-default">Update Profile</button>
	     </div>
	   </div>
	 </form>

	 %if error:
	   <div class="alert alert-danger text-center" role="alert">
         {{error}}
	   </div>
	 %end

	 <br />
	 <hr />
	 
  </div>
</div>
	 