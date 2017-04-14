fartscroll();
$(document).ready( () => {
  //$.get( `${window.location.href}results/${title}`, updateResults )
  for(joke of [{title:'Why did the chicken cross the road', selftext:'Your mom'},
              {title:'Knock Knock', selftext:'Your mom'}]){
                $('body').append(flipcard(joke));
              }
  $('.flip').hover(function(){
        $(this).find('.card').toggleClass('flipped');
  });
}
)
