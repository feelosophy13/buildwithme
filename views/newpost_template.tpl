%rebase('base.tpl')
%setdefault('title', '')
%setdefault('postContent', '')
%setdefault('tags', '')
%setdefault('youtubeLink', '')
%setdefault('error', '')

<div class="row">
   <div class="col-md-6 col-md-offset-3"><!-- centering the posts in the middle -->
   	<h1 class='text-center'>Post Your Idea</h1>
   	<br />

	 %if error:
	   <div class="alert alert-danger text-center" role="alert">
		 {{error}}
	   </div>
	 %end

	  <form class="form-horizontal" role="form" action="/newpost" method="POST">
	  	<div class="form-group">
		  <label for="title" class="col-sm-2 control-label">Idea Title</label>
		  <div class="col-sm-10">
			  <input type="text" class="form-control" id="title" name="title" value="{{title}}" maxlength="120" placeholder="My awesome title">
		  </div>
	  	</div>
	  	
		<div class="form-group">
		  <label for="postContent" class="col-sm-2">Description</label>
		  <div class="col-sm-10">
			<textarea class="form-control" rows="10" id="postContent" placeholder="My next great idea is..." name="postContent" maxlength="2000"
			onKeyDown="limitText(this.form.limitedtextarea, this.form.countdown, 2000);"
			onKeyUp="limitText(this.form.postContent, this.form.countdown, 2000);">{{postContent}}</textarea>
			<br />
			<font size="2">You have <input readonly type="text" name="countdown" class="word_countdown" size="1" value="2000"> characters left.</font>
		  </div>
		</div>

		<div class="form-group">
		  <label for="youtubeLink" class="col-sm-2 control-label">Youtube</label>
		  <div class="col-sm-10">
		  	<input type="url" class="form-control" id="youtubeLink" name="youtubeLink" value="{{youtubeLink}}" placeholder="Please include https:// in the URL. (Optional)">
		  </div>
		</div>

		<div class="form-group">
		  <label for="tags" class="col-sm-2 control-label">Tags</label>
		  <div class="col-sm-10">
		  	<input type="text" class="form-control" id="tags" name="tags" value="{{tags}}" maxlength="120" placeholder="Please limit to 6 tags, separated by commas. (Optional)">
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
				<a href="/newpost" class="noLinkDec"><button type="button" class="btn btn-lg btn-default">Empty</button></a>
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