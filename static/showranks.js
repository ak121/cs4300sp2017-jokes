fartscroll();
$(document).ready( () => {
  //$.get( `${window.location.href}results/`, updateResults )
})

function retrieveJokes(){
  querystr = $('#query').val();
  $.ajax({url:`${window.location.href}results`,
    type: 'POST',
    dataType: 'json',
    processData: false,
    success: updateResults
  });
};

function updateResults(jokedata){
  $('#results-view').html("");
  var i = 0;
  for (joke of jokedata) {
    newrow = $('#results-view')[0].insertRow(i);
    newrow.innerHTML = jokedisp(joke);
    i += 1;
  }
};
