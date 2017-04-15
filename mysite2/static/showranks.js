fartscroll();
$(document).ready( () => {
  //$.get( `${window.location.href}results/`, updateResults )
})

function retrieveJokes(){
  querystr = $('#query').val();
  $.ajax({url:`${window.location.href}results/${encodeURI(JSON.stringify({'query':querystr}))}`,
    type: 'GET',
    dataType: 'json',
    processData: false
  }).done(updateResults);
};

function updateResults(jokedata){
  console.log(jokedata)
  $('#results-view').empty();
  for (joke in jokedata.responseJSON) {
    $('#results-view').innerHTML += (jokedisp(joke));
  }
};
