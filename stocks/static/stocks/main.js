

function fetchdata(ticker){
    $.ajax({
    url: 'https://api.tdameritrade.com/v1/marketdata/'+ticker+'/quotes?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B',
    type: 'get',
    dataType: "json",
    success: function(data){
        // Perform operation on return valud
        let stockObj = data[ticker];
        let price = stockObj.regularMarketLastPrice;
        let change = stockObj.regularMarketNetChange;
        let percent = stockObj.regularMarketPercentChangeInDouble;
        let bidPrice = stockObj.bidPrice;
        let askPrice = stockObj.askPrice;
        let high = stockObj.highPrice;
        let low = stockObj.lowPrice;
        let low52 = stockObj['52WkLow'];
        let high52 = stockObj['52WkHigh'];
        high = high.toFixed(2);
        low = low.toFixed(2);
        low52 = low52.toFixed(2);
        high52 = high52.toFixed(2);
        percent = percent.toFixed(2);
        if(change>0){
            let string = '+$'+change+' (+'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","rgba(8, 153, 129, 1)");
        }
        else if(change<0){
            let string = '-$'+change+' (-'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","#f1272e");
        }
        else{
            let string = '+$'+change+' (+'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","white");
        }
        $(".currPrice").each(function(){
            $(this).text("$"+price);
        });
        $("#bidPrice").text("$"+bidPrice);
        $("#askPrice").text("$"+askPrice);
        $("#low").text("$"+low);
        $("#high").text("$"+high);
        $("#52low").text("$"+low52);
        $("#52high").text("$"+high52);
    },
    complete:function(data){
        setTimeout(fetchdata,5000,ticker);
    }
    });
    }

$(document).ready(function(){
    let ticker = $('#ticker').text();
    ticker = ticker.toUpperCase();
    fetchdata(ticker);
});