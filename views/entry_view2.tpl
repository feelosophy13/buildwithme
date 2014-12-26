%rebase('base.tpl')
        <!-- Portfolio Item Heading -->
        <div class="row">
            <div class="col-lg-12">
                <h1 class="page-header">Portfolio Item
                    <small>Item Subheading</small>
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
					<div class="text-right">
						<a class="btn btn-success">Leave a Feedback</a>
					</div>

					<hr>

					<div class="row">
						<div class="col-md-12">
							Anonymous
							<span class="pull-right">10 days ago</span>
							<p>This product was great in terms of quality. I would definitely buy another!</p>
						</div>
					</div>

					<hr>

					<div class="row">
						<div class="col-md-12">
							Anonymous
							<span class="pull-right">12 days ago</span>
							<p>I've alredy ordered another one!</p>
						</div>
					</div>

					<hr>

					<div class="row">
						<div class="col-md-12">
							Anonymous
							<span class="pull-right">15 days ago</span>
							<p>I've seen some better than this, but not at this price. I definitely recommend this item.</p>
						</div>
					</div>
					
					<hr>
					
					<div class="row">
						<div class="col-md-12">
							%if (userID == None):
								You must <a href='/login'>log in</a> to post feedback.
							%else:
								<!-- form to add a feedback -->
								<p>Give a feedback:</p>
								<form role="form" action="/newfeedback" method="POST">
									<div class="form-group">
										<input type="hidden" name="permalink", value="{{post['p']}}">
										<textarea class="form-control" rows="5" placeholder="Got anything to say?" name="feedbackContent" maxlength="1000">{{feedbackContent}}</textarea>
									</div>
									{{error}}
									<button type="submit" class="btn btn-lg btn-danger" value="Submit">Submit</button>
								</form>			 
						</div>
					</div>

			 
			 <!-- form to add a feedback -->
		 %end


				</div>
                <!-- end of feedbacks -->
                
            </div>
            <!-- end of first column -->

            <!-- start of second column -->
            <div class="col-md-5">
                <h3>Project Description</h3>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae. Sed dui lorem, adipiscing in adipiscing et, interdum nec metus. Mauris ultricies, justo eu convallis placerat, felis enim.</p>
                <h3>Project Details</h3>
                <ul>
                    <li>Lorem Ipsum</li>
                    <li>Dolor Sit Amet</li>
                    <li>Consectetur</li>
                    <li>Adipiscing Elit</li>
                </ul>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae. Sed dui lorem, adipiscing in adipiscing et, interdum nec metus. Mauris ultricies, justo eu convallis placerat, felis enim.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae. Sed dui lorem, adipiscing in adipiscing et, interdum nec metus. Mauris ultricies, justo eu convallis placerat, felis enim.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae. Sed dui lorem, adipiscing in adipiscing et, interdum nec metus. Mauris ultricies, justo eu convallis placerat, felis enim.</p>

            </div>
            <!-- end of second column -->

        </div>
        <!-- end of row -->
        
        <p></p>
        


        

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
