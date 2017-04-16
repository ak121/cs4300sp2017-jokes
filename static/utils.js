function jokedisp(joke){
  // return (
  //  `<div class="well well-sm" >${joke.title}
  //   </div>
  //   <div class="well well-lg">
  //     ${joke.selftext}
  //   </div>`);
  return (
   `<div class="well well-lg">
   		<h3>${joke.title}</h3>
      	${joke.selftext}
    </div>`);
}
