fartscroll();
var nsfwCheckbox;

$(document).ready( () => {
  //$.get( `${window.location.href}results/`, updateResults )
  // nsfwCheckbox = document.querySelector('input[value="wantNSFW"]');
  // nsfwCheckbox = document.querySelector('input[id="nsfw"]');
})

function retrieveJokes(){
  querystr = $('#query').val();
  var isChecked = false;
  nsfwCheckbox = document.querySelector('input[value="wantNSFW"]'); //This technically shouldn't go here, but okay
  if(nsfwCheckbox.checked) isChecked = true;
  $.ajax({url:`${window.location.href}results/`,
    type: 'POST',
    dataType: 'json',
    processData: false,
    data: JSON.stringify({'query': querystr, 'nsfw' : isChecked}),
    success: updateResults
  });
};

function updateResults(jokedata){
  $('#results-view').html("<b>Click each card to reveal the answer!</b><br>");
  var i = 0;
  for (joke of jokedata) {
    newrow = $('#results-view')[0].insertRow(i);
    newrow.innerHTML = jokedisp(joke);
    i += 1;
  }
};
