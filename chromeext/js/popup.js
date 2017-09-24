
document.addEventListener('DOMContentLoaded', function() {
  var a=[]
  var b=[]
  var self=this;
  var giphyApiKey="dVlhE2vskvrVHSCoXOxX702d0F4itEna"
  var checkPageButton = document.getElementById('checkPage');
  var shouldIBuy = document.getElementById('shouldIBuy');
  var visualize = document.getElementById('visualize');

  checkPageButton.addEventListener('click', function() {
    chrome.tabs.getSelected(null, function(tab) {
      $.get( "https://api.coinbase.com/v2/prices/BTC-USD/buy", function( data ) {
        $( "#bitcoin" ).html(data.data.amount);
      });
      $.get( "https://api.coinbase.com/v2/prices/LTC-USD/buy", function( data ) {
        $( "#litecoin" ).html(data.data.amount);
      });
      $.get( "https://api.coinbase.com/v2/prices/ETH-USD/buy", function( data ) {
        $( "#etherum" ).html(data.data.amount);
      console.log("clicked update!")
      });

    });
  }, false);
  shouldIBuy.addEventListener('click', function() {
    chrome.tabs.getSelected(null, function(tab) {
      var url="http://api.giphy.com/v1/gifs/random?tag="
      var chosenValue = Math.random() < 0.5 ? "yes" : "no";
      $.get( url+chosenValue+"&api_key="+giphyApiKey, function( data ) {
        window.open(data.data.image_url)
      });
    });
  }, false);
  visualize.addEventListener('click', function() {
    chrome.tabs.getSelected(null, function(tab) {
        var visualizeUrl="http://localhost:8887"
        console.log("Visualize Clicked")
        window.open(visualizeUrl)
    });
  });

}, false);
