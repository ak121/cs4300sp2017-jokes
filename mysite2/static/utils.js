function jokedisp(joke){
  return (
   `<div class="well well-sm" >${joke.title}
    </div>
    <div class="well well-lg">
      ${joke.selftext}
    </div>`);
}
