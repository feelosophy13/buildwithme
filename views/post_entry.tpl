%rebase('base.tpl')
%setdefault('error', '')
%setdefault('permalink', '')


<div class="row">
   <div class="col-md-8 col-md-offset-2"><!-- centering the posts in the middle -->
   	<h1 class='text-center'>Post Your Idea</h1>
   	<br />

	 %if error:
	   <div class="alert alert-danger text-center" role="alert">
		 {{error}}
	   </div>
	 %end
	 

	  <form class="form-horizontal" role="form" method="POST">
	  	<div class="form-group">
		  <label for="title" class="col-sm-2 control-label">Idea Title</label>
		  <div class="col-sm-10">
			  <input type="text" class="form-control" name="title" value="{{post['s']}}" maxlength="120" placeholder="My awesome, descriptive title">
		  </div>
	  	</div>
	  	
		<div class="form-group">
		  <label for="bodySummary" class="col-sm-2 control-label">Summary</label>
		  <div class="col-sm-10">
			<textarea class="form-control" rows="3" placeholder="My next great idea is..." name="bodySummary" maxlength="200">{{post['b']['c']}}</textarea>
		  </div>
		</div>

		<div class="form-group">
		  <label for="bodyProblem" class="col-sm-2 control-label">The Problem</label>
		  <div class="col-sm-10">
			<textarea class="form-control" rows="4" placeholder="What problem are you trying to solve?" name="bodyProblem" maxlength="500">{{post['b']['p']}}</textarea>
		  </div>
		</div>

		<div class="form-group">
		  <label for="bodySolution" class="col-sm-2 control-label">The Solution</label>
		  <div class="col-sm-10">
			<textarea class="form-control" rows="4" placeholder="What's your solution?" name="bodySolution" maxlength="500">{{post['b']['s']}}</textarea>
		  </div>
		</div>

		<div class="form-group">
		  <label for="bodyMonetize" class="col-sm-2 control-label">Monetization</label>
		  <div class="col-sm-10">
			<textarea class="form-control" rows="4" placeholder="How do you plan to make money?" name="bodyMonetize" maxlength="500">{{post['b']['m']}}</textarea>
		  </div>
		</div>

		<div class="form-group">
		  <label for="bodyAdvertise" class="col-sm-2 control-label">Marketing</label>
		  <div class="col-sm-10">
			<textarea class="form-control" rows="4" placeholder="How will you bring people to your service/product?" name="bodyAdvertise" maxlength="500">{{post['b']['a']}}</textarea>
		  </div>
		</div>

		<div class="form-group">
		  <label for="youtubeLink" class="col-sm-2 control-label">Youtube</label>
		  <div class="col-sm-10">
		  	<input type="url" class="form-control" name="youtubeLink" value="{{post['y']}}" placeholder="Please include https:// in the URL. (Optional)">
		  </div>
		</div>

		<div class="form-group">
		  <label for="tags" class="col-sm-2 control-label">Tags</label>
		  <div class="col-sm-10">
		  	<input type="text" class="form-control" name="tags" value="{{post['l']}}" maxlength="120" placeholder="Please limit to 6 tags, separated by commas. (Optional)">
		  </div>
		</div>
		
		<!--
		<div class="form-group">
		  <label for="exampleInputFile">File input</label>
		  <input type="file" id="exampleInputFile">
		  <p class="help-block">Example block-level help text here.</p>
		</div>
		-->
		
		<div class="form-group">
			<div class="col-sm-6 col-sm-offset-5">
				<button type="submit" class="btn btn-lg btn-success" value="Submit">Submit</button>
				<a href="/newpost" class="noLinkDec"><button type="button" class="btn btn-lg btn-danger">Empty</button></a>
			</div>
		</div>		
	  </form>


<!--
<form role="form">
  <div class="form-group">
    <label for="exampleInputEmail1">Email address</label>
    <input type="email" class="form-control" id="exampleInputEmail1" placeholder="Enter email">
  </div>
  <div class="form-group">
    <label for="exampleInputPassword1">Password</label>
    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
  </div>
  <div class="form-group">
    <label for="exampleInputFile">File input</label>
    <input type="file" id="exampleInputFile">
    <p class="help-block">Example block-level help text here.</p>
  </div>
  <div class="checkbox">
    <label>
      <input type="checkbox"> Check me out
    </label>
  </div>
  <button type="submit" class="btn btn-default">Submit</button>
</form>
-->


   </div>
</div>