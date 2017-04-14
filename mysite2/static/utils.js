function flipcard(joke){
  return `<div class="col-sm-3">
            <div class="flip">
              <div class="card">
                <div class="face front">
                  <h3>${joke.title}</h3>
                </div>
                <div class="face back">
                  <h3>${joke.selftext}</h3>
                </div>
              </div>
            </div>
          </div>`;
}
