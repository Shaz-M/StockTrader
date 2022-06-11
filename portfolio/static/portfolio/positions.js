let stocks = $(".ticker");
let sharesArr = $(".quantity");
let markArr = $(".marks");
let tradePriceArr = $(".tradePrice");
let openArr = $(".plOpen");
let dayArr = $(".plDay");
let netLiqArr = $(".netLiq");
let percentArr = $(".percentReturn");


function fetchdata(stocks){
    let sumPlOpen = 0;
    let sumPlDay = 0;
    let sumNetLiq = 0;
    for(let i = 0; i<stocks.length; i++){
        let ticker = stocks[i].innerText;
        let shares = parseInt(sharesArr[i].innerText);
        let markDom = markArr[i];
        let avgPrice = tradePriceArr[i].innerText;
        avgPrice = parseInt(avgPrice.substring(1));
        let openDom = openArr[i];
        let dayDom = dayArr[i];
        let netLiqDom = netLiqArr[i];
        let percentDom = percentArr[i];
        $.ajax({
        url: 'https://api.tdameritrade.com/v1/marketdata/'+ticker+'/quotes?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B',
        type: 'get',
        async: false,
        dataType: "json",
        success: function(data){
            // Perform operation on return valud
            let stockObj = data[ticker];
            let price = stockObj.regularMarketLastPrice;
            let change = stockObj.regularMarketNetChange;
            let netLiq = price*shares;
            let plOpen = (shares*price)-(shares*avgPrice);
            let plDay = shares*change;
            let percentPL = (plOpen/(shares*avgPrice))*100;
    
            plOpen = plOpen.toFixed(2);
            plDay = plDay.toFixed(2);
            netLiq = netLiq.toFixed(2);
            percentPL = percentPL.toFixed(2);

            sumPlOpen += parseFloat(plOpen);
            sumPlDay += parseFloat(plDay);
            sumNetLiq += parseFloat(netLiq);
            markDom.innerText = price;
            openDom.innerText = "$"+plOpen;
            dayDom.innerText = "$"+plDay;
            netLiqDom.innerText = "$"+netLiq;
            percentDom.innerText = percentPL+"%";
        },
        });
    }

    sumPlOpen = sumPlOpen.toFixed(2);
    sumPlDay = sumPlDay.toFixed(2);
    sumNetLiq = sumNetLiq.toFixed(2);
    $(".totalPlOpen").each(function(){
        $(this).text("$"+sumPlOpen);
    })
    $(".totalPlDay").each(function(){
        $(this).text("$"+sumPlDay);
    })
    $(".totalNetLiq").each(function(){
        $(this).text("$"+sumNetLiq);
    })
    setTimeout(fetchdata,5000,stocks);
}

$(document).ready(function(){
    fetchdata(stocks);
});