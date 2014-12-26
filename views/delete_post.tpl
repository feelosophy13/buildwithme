%rebase('base.tpl')

<div class="starter-template">
   <div class="row">
	  <div class="col-md-8 col-md-offset-2">

	  <form role="form" method="post">
		  <div class="alert alert-warning" role="alert">
			  Are you sure you want to permanently delete this post? &nbsp;&nbsp;&nbsp;		  
			  <button type="submit" class="btn btn-danger">Delete</button>
			  <a href="/manage_posts" class="noLinkDec"><button type="button" class="btn btn-default">Cancel</button></a>
		  </div>
	  </form>

		 <div class="panel panel-default">
		   <div class="panel-heading">
			 <h3 class="panel-title"><b>{{post['s']}}</b></h3>
		   </div>
		   <div class="panel-body">
			 <div class='largeFontSize'>
			 {{!post['b']}}<br />
			 </div>	
			</div>
		 </div>
		 <br />

	  </div>
   </div>
</div>
