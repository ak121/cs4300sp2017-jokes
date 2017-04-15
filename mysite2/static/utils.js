function jokedisp(joke){
  return (
   `<tr>
    <button data-toggle="collapse" data-target="${joke.id}">${joke.title}
    </button>
    <div id="${joke.id}" class="collapse">
      ${joke.selftext}
    </div>
    </tr>`);
}
