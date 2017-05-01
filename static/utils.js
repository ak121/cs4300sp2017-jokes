function jokedisp(joke){
  // return (
  //  `<div class="well well-sm" >${joke.title}
  //   </div>
  //   <div class="well well-lg">
  //     ${joke.selftext}
  //   </div>`);
  var num_comments = joke.metadata.num_comments //'${joke.metadata.num_comments}';
  if(num_comments==undefined) num_comments = "N/A";
  var upvotes = joke.metadata.ups; //'${joke.metadata.ups}';
  if(upvotes==undefined) upvotes = "N/A";
  var downvotes = joke.metadata.downs; //'${joke.metadata.downs}';
  if(downvotes==undefined) downvotes = "N/A";

  return (
   `<div class="well well-lg results">
      <div class="metadata">
        <ul>        
          <li>  &#x1F4AC; ${num_comments} </li>
          <li>  &#x1F44D; ${upvotes} </li>
          <li>  &#x1F44E; ${downvotes} </li>
        </ul>
      </div> <br>
   		<div class="question"><i>Q:</i> ${joke.title}</div>
      <div class="answer" style="display: none;"><i>A:</i> ${joke.selftext}</div>      
    </div>`);
}

$(document).ready( () => {
  $(".container").hide();

  $("#results-view").on("click", ".results", function(){
    if($(this).hasClass("flip")){
      $(this).removeClass("flip");    
      var ques = $(this).find(".question");      
      ques.show();
      var answer = $(this).find(".answer");      
      answer.hide();
    }
    else{
      $(this).addClass("flip");    
      var ques = $(this).find(".question");      
      ques.hide();
      var answer = $(this).find(".answer");      
      answer.show();      
    }
  });  

  $("#query").keyup(function(event){
    if(event.keyCode==13){
      $("#search_button").click();
    }
  });
})
