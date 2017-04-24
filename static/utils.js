function jokedisp(joke){
  // return (
  //  `<div class="well well-sm" >${joke.title}
  //   </div>
  //   <div class="well well-lg">
  //     ${joke.selftext}
  //   </div>`);
  return (
   `<div class="well well-lg results">
   		<div class="question">${joke.title}</div>
      <div class="answer" style="display: none;">${joke.selftext}</div>
    </div>`);
}

$(document).ready( () => {
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
