

function fetchdata(ticker){
    $.ajax({
    url: 'https://api.tdameritrade.com/v1/marketdata/'+ticker+'/quotes?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B',
    type: 'get',
    dataType: "json",
    success: function(data){
        // Perform operation on return valud
        let price = data[ticker].regularMarketLastPrice;
        let change = data[ticker].regularMarketNetChange;
        let percent = data[ticker].regularMarketPercentChangeInDouble;
        percent = percent.toFixed(2);
        if(change>0){
            let string = '+$'+change+' (+'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","rgba(8, 153, 129, 1)");
        }
        else if(change<0){
            let string = '-$'+change+' (-'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","red");
        }
        else{
            let string = '+$'+change+' (+'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","white");
        }
        $("#price").text('$'+price);
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