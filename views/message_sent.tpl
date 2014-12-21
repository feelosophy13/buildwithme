%rebase('base.tpl')
%setdefault('targetUserID', '')

<div class="starter-template">
   <div class="alert alert-success" role="alert">
       <p class="lead">Your message was sent successfully!</p>
   </div>
   
   <a href="/user/{{targetUserID}}">Go back to the user's profile.</a>
</div>

