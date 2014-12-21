%rebase('base.tpl')

<div class="starter-template">
   <div class="row">
	  <div class="col-md-6 col-md-offset-3"><!-- centering the posts in the middle -->

		 <div class="panel panel-default">
		   <div class="panel-heading">
			 <h3 class="panel-title"><b>{{post['s']}}</b></h3>
			 <!--
			 <h3 class="panel-title"><b>{{post['t']}}</b><br></h3>
			 -->
		   </div>
		   <div class="panel-body">
			 <div class='largeFontSize'>
			 {{!post['b']}}<br />
			 </div>
	
			 <br />
			 <a href="#">
			 %if ('f' in post):
			 %numFeedbacks = len(post['f'])
			 %else:
			 %numFeedbacks = 0
			 %end
			 {{numFeedbacks}} feedbacks</a>

			</div>
		 </div>
		 <br />

		 <!-- display feedbacks -->
		 <h4>Feedbacks</h4>

		 %if ('f' in post):
			 %numFeedbacks = len(post['f'])
		 %else:
			 %numFeedbacks = 0
		 %end

		 %for i in range(0, numFeedbacks):
			 <blockquote class="commentBoxes">
			   <p>{{post['f'][i]['b']}}</p>
			   <footer><b>{{post['f'][i]['u']}}</b> on <i>{{post['f'][i]['t']}}</i></footer>
			 </blockquote>
		 %end
		 <!-- display feedbacks -->

		 <br />

		 %if (userID == None):
			 You must <a href='/login'>log in</a> to post feedback.
		 %else:
			 <!-- form to add a feedback -->
			 Give a feedback:
			 <form role="form" action="/newfeedback" method="POST">
				 <div class="form-group">
					 <input type="hidden" name="permalink", value="{{post['p']}}">
					 <textarea class="form-control" rows="5" id="feedbackContent" placeholder="Got anything to say?" name="feedbackContent" maxlength="400">{{newFeedbackContent}}</textarea>
				 </div>
				 <br />
				 {{error}}
				 <br />
				 <button type="submit" class="btn btn-lg btn-danger" value="Submit">Submit</button>
			 </form>
			 <!-- form to add a feedback -->
		 %end


	  </div>
   </div>
</div>
