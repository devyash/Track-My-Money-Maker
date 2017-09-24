function toJSDate (dateTime) {
    var dateTime = dateTime.split(" ");
    var date = dateTime[0].split("-");
    var time = date[2].split(":");
    //(year, month, day, hours, minutes, seconds, milliseconds)
    return time[0].substring(3)+":"+time[1];
  }
function drawGraph(coin_base_url,label,elementId){
    let a=[]
    let b=[]
    $.get( coin_base_url, function( data ) {
        let out=data.data.prices
        _.map(out, function(obj){
          a.push(toJSDate(obj.time))
          b.push(obj.price)
        });
        var res={
            labels: a,
            xAxisID:"Time",
            yAxisID:"Price in USD$",

            datasets: [{
                label: label,

                borderColor: 'rgb(51, 204, 255)',
                data: b,
            }],

        };
        var ctx = document.getElementById(elementId).getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data:res,

            // Configuration options go here
            options:{},
            // {
            //   scales: {
            //     xAxes: [{
            //       type: 'time',
            //       distribution: 'series',
            //       ticks: {
            //         source: 'labels',
            //         stepSize: 2
            //       }
            //     }],
            //     yAxes: [{
            //       scaleLabel: {
            //         display: true,
            //         labelString: 'Closing price ($)'
            //       }
            //     }]
            //   }
            // }
          });
        });
  }

function drawPolarChart(obj,elementId){
    // Display the data
    console.log(obj)
    let res = {
      datasets: [{
          data: obj.data,
          backgroundColor: [
                "#F7464A",
                "#46BFBD",
                "#FDB45C"
            ],
   borderColor: "rgba(0, 0, 0, 0.8)"
 }],


      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: obj.label,
  };
  var ctx = document.getElementById(elementId).getContext('2d');
  var chart = new Chart(ctx, {
    data: res,
    type: 'polarArea',
    options: {}});
}

function displayChart(bitcoinDataURL  ,Bitcoindata,elementId){
    new Promise((resolve, reject) => {
        $.ajax({
        url: bitcoinDataURL,
        success: function(data){
             data=data.response
             console.log(data);
            //  TODO: Change the data format here
             drawPolarChart({
               label:["negative","neutral","positive"],
               data:[data.negative.tweets.length, data.neutral.tweets.length, data.positive.tweets.length]
             },elementId)
        },
        timeout: 50000 // sets timeout to 50 seconds
      });
    })
}

$( document ).ready(function() {
  var searchButton = $("#searchButton")
  searchButton.bind('click', function() {
    // TODO: Add search key to url and search
  });

  var coin_base_url="https://www.coinbase.com/api/v2/prices/BTC-USD/historic?period=day"
  var label="Bitcoin"
  var elementId="myChart-1"
  drawGraph(coin_base_url,label,elementId);
  var coin_base_url="https://www.coinbase.com/api/v2/prices/LTC-USD/historic?period=day"
  var label="Litecoin"
  var elementId="myChart-2"
  drawGraph(coin_base_url,label,elementId);

  var coin_base_url="https://www.coinbase.com/api/v2/prices/ETH-USD/historic?period=day"
  var label="Etherum"
  var elementId="myChart-3"
  drawGraph(coin_base_url,label,elementId);

  // First Get Bitcoin data
  // TODO: Added temporary
  let keyWord="mhacks"
  let bitcoinDataURL="http://trackmymoneymaker.appspot.com/query?q="+keyWord;
  var Bitcoindata={}
  elementId="myChart-11"
  displayChart(bitcoinDataURL,Bitcoindata,elementId)
  keyWord="mhacks"
  let LiteCoinUrl="http://trackmymoneymaker.appspot.com/query?q="+keyWord;
  elementId="myChart-21"
  console.log("2nd chart")
  displayChart(LiteCoinUrl,Bitcoindata,elementId)
  keyWord="mhacks"
  let etherumURL="http://trackmymoneymaker.appspot.com/query?q="+keyWord;
  console.log("3rd chart")
  elementId="myChart-31"
  displayChart(etherumURL,Bitcoindata,elementId)
  });
