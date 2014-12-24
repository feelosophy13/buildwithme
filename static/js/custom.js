function limitText(limitField, limitCount, limitNum) {
    if (limitField.value.length > limitNum) {
		limitField.value = limitField.value.substring(0, limitNum);
    } else {
		limitCount.value = limitNum - limitField.value.length;
    }
}


$("a[data-permalink]").click(function(e) {  // when a like/unlike button is clicked for a post
	permalink = $(this).attr("data-permalink")  // get the permalink for the post liked/unliked
	
    if ($(this).html() == "Like Idea") {  // if "like" button was clicked
		$.post('/like_post', {permalink: permalink}, function(data) {  	// send a post request to /like_post with permalink
			if (data == 'success') {  // if like was successfully saved to the database
                $(this).html('Unlike Idea');  // change button from "like" to "unlike"
			} else if (data == 'already liked') {
				alert("js-2")
			    alert("You already liked this idea!");
			} else {   // if like was not successfully saved to the database
				alert('Sorry, an error occurred.');
			}
		});    
    }
    
    else {  // if "unlike" button was clicked
        $.post('/unlike_post', {permalink: permalink}, function(data) {  // send a post request to /unlike_post with permalink
        	if (data == 'success') {  // if unlike was successfully saved to the database
                $(this).html('Like Idea');  // change button from "unlike" to "like"
        	} else if (data == 'already unliked') {
        	    alert("You already unliked this idea!");
        	} else {  // if unlike was not successfully saved to the database
        		alert("Sorry, an error occurred.");
        	}
        });
    }
    
    return false;
});


$("#loadingSpin").hide();


$("#sendMessageBtn").click(function(){
  $("#loadingSpin").show();
});
