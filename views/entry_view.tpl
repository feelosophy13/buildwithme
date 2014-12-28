%rebase('base.tpl')
%setdefault('mode', 'view')  # there are three modes: 1. "view" for regular viewing, 2. "delete" for confirming post delete, and 3. "feedback_edit" for feedback editing
%setdefault('error', '')
%setdefault('feedbackContent', '')

%if mode == 'view':
%	feedback_action_link = '/insert_feedback'
%elif mode == 'feedback_edit':
%	feedback_action_link = '/edit_feedback'
%end

%if feedbacks:
%	numFeedbacks = len(feedbacks)
%else:
%	numFeedbacks = 0
%end

%if mode == 'delete':
   <div class="row">
	  <div class="col-md-6 col-md-offset-3">
	  <form role="form" method="post">
		  <div class="alert alert-warning" role="alert">
			  Are you sure you want to permanently delete this post? &nbsp;&nbsp;&nbsp;		  
			  <button type="submit" class="btn btn-danger">Delete</button>
			  <a href="/manage_posts" class="noLinkDec"><button type="button" class="btn btn-default">Cancel</button></a>
		  </div>
	  </form>
	  </div>
   </div>
%end

<!-- Portfolio Item Heading -->
<div class="row">
	<div class="col-lg-12">
		<h1 class="page-header">{{post['s']}}
			<small>by <a href="/user/{{post['a']['u']}}">{{post['a']['f']}}</a></small>
		</h1>
	</div>
</div>
<!-- /.row -->

<!-- Portfolio Item Row -->
<div class="row">

	<!-- start of first column -->
	<div class="col-md-7">
		<img class="img-responsive" src="http://placehold.it/750x500" alt="">
		
		<!-- start of feedbacks -->
		<div class="well">
		    %if mode == 'view':
				<div class="text-right">
					<span class="pull-right">{{numFeedbacks}} feedbacks</span>
				</div>
			%end

			<hr>

			%for i in range(0, numFeedbacks):
			<div class="row">
				<div class="col-md-12">
					<a href="/user/{{feedbacks[i]['a']['u']}}">{{feedbacks[i]['a']['f']}}</a> wrote:
					<span class="pull-right">{{feedbacks[i]['t']}}</span>					
					<p>{{feedbacks[i]['b']}}</p>
				</div>
			</div>

			<hr>
			%end
			
			<!-- form to add a feedback -->
			%if mode == 'view' or mode == 'feedback_edit':
				<div class="row">
					<div class="col-md-12">
						%if userID:								
							<p>Give a feedback:</p>
							<form role="form" action="{{feedback_action_link}}" method="POST">
								<div class="form-group">
									<input type="hidden" name="permalink", value="{{post['p']}}">
									<textarea class="form-control" rows="5" placeholder="Got anything to say?" name="feedbackContent" maxlength="1000">{{feedbackContent}}</textarea>
								</div>
								{{error}}
								<button type="submit" class="btn btn-lg btn-danger" value="Submit">Submit</button>
							</form>

						%else:
							You must <a href='/login'>log in</a> to post feedback.
						%end
					</div>
				</div>
			%end
			<!-- form to add a feedback -->
			
		</div>
		<!-- end of feedbacks -->
		
	</div>
	<!-- end of first column -->

	<!-- start of second column -->
	<div class="col-md-5">
		<h3>Summary</h3>
		<p>{{!post['b']['c']}}</p>
		<h3>Problem</h3>
		<p>{{!post['b']['p']}}</p>
		<h3>Solution</h3>
		<p>{{!post['b']['s']}}</p>
		<h3>Monetization</h3>
		<p>{{!post['b']['m']}}</p>
		<h3>Marketing</h3>
		<p>{{!post['b']['a']}}</p>

	</div>
	<!-- end of second column -->

</div>
<!-- end of row -->

<!-- Related Projects Row -->
<!--
<div class="row">

	<div class="col-lg-12">
		<h3 class="page-header">Related Projects</h3>
	</div>

	<div class="col-sm-3 col-xs-6">
		<a href="#">
			<img class="img-responsive portfolio-item" src="http://placehold.it/500x300" alt="">
		</a>
	</div>

	<div class="col-sm-3 col-xs-6">
		<a href="#">
			<img class="img-responsive portfolio-item" src="http://placehold.it/500x300" alt="">
		</a>
	</div>

	<div class="col-sm-3 col-xs-6">
		<a href="#">
			<img class="img-responsive portfolio-item" src="http://placehold.it/500x300" alt="">
		</a>
	</div>

	<div class="col-sm-3 col-xs-6">
		<a href="#">
			<img class="img-responsive portfolio-item" src="http://placehold.it/500x300" alt="">
		</a>
	</div>

</div>
-->

<hr>
        
