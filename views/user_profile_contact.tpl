%setdefault('error', '')
%if userID:
	%state = ''
%else:
	%state = 'disabled'
%end

<h2 class='text-center'>Contact {{queriedUser['f']}}</h2>

<br />

<div class="row">
 <form class="form-horizontal" role="form" method="POST">
   %if error:
	 <div class="form-group">
	   <div class="col-sm-10 col-sm-offset-1">
		   <div class="alert alert-danger text-center" role="alert">
			 {{error}}
		   </div>
	   </div>
	 </div>
   %end
   
   %if userID is None:
   <div class="form-group">
	 <div class="col-sm-10 col-sm-offset-1">
	 	<div class="alert alert-warning text-center" role="alert">
	 		Please <a href="/login">log in</a> to contact {{queriedUser['f']}}.
	 	</div>
	 </div>
   </div>
   %else:
   <div class="form-group">
	 <div class="col-sm-10 col-sm-offset-1">
		<textarea class="form-control" rows="7" id="message" placeholder="Say something nice." name="message" maxlength="2000"
		onKeyDown="limitText(this.form.limitedtextarea, this.form.countdown, 2000);"
		onKeyUp="limitText(this.form.message, this.form.countdown, 2000);">{{message}}</textarea>
	 </div>
   </div>

   <div class="form-group text-center">
  	<img id="loadingSpin" src="../static/images/loading_spin.gif" />
   </div>
					   
   <div class="form-group text-center">
	<font size="2">You have <input readonly type="text" name="countdown" class="word_countdown" size="1" value="2000"> characters left.</font>
   </div>

   <div class="form-group">
	 <div class="col-sm-offset-5 col-sm-2">
		<button type="submit" class="btn btn-default" id="sendMessageBtn">Send Message</button>		
	 </div>
   </div>
   %end
 </form>
 


</div>