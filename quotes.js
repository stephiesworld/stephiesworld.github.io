var quotes = [
  { text: "No one can build you the bridge on which you, and only you, must cross the river of life.", author: "Nietzsche" },
  { text: "To live is the rarest thing in the world. Most people just exist.", author: "Oscar Wilde" },
  { text: "We are all just walking each other home.", author: "Ram Dass" },
  { text: "What is done out of love always takes place beyond good and evil.", author: "Nietzsche" },
  { text: "Memory is the diary we all carry about with us.", author: "Oscar Wilde" },
  { text: "Look for what you notice but no one else sees.", author: "Rick Rubin" },
  { text: "All that matters is that you are making something you love, to the best of your ability, here and now.", author: "Rick Rubin" },
  { text: "Perhaps all the dragons in our lives are princesses who are only waiting to see us act, just once, with beauty and courage.", author: "Rilke" },
  { text: "The only journey is the one within.", author: "Rilke" }
];

function setRandomQuote() {
  var el = document.getElementById('footerQuote');
  if (el) {
    var q = quotes[Math.floor(Math.random() * quotes.length)];
    el.innerHTML = '\u201c' + q.text + '\u201d \u2014 ' + q.author;
  }
}
