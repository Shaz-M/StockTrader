const selectElement = document.querySelector('#quantity');
const sellQuantity = document.querySelector('#sell-quantity');

let cash = parseFloat($("#cashBal").text().substring(1));


selectElement.addEventListener('input', inputEvent);
sellQuantity.addEventListener('input',inputEvent);

function inputEvent(){
    let shares = parseInt(event.target.value);
    let cost = 0;
    if(!Number.isNaN(shares)){
        let currPrice = parseFloat($("#price").text().substring(1));
        cost = currPrice*shares;
        cost = cost.toFixed(2);
        cost = parseFloat(cost);
    }

    let resBal = cash-cost;
    resBal = resBal.toFixed(2);
    if(cost==0){cost="0.00";}
    $(".tradeCost").text(function(){
        return "$"+cost
    });
    $('#resBal').text('$'+resBal);
}


let shares =  parseInt($("#shares").text());
let avgPrice = parseFloat($("#avgPrice").text().substring(1));
function fetchdata(ticker,prevPrice){
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
        let netLiq = price*shares;
        let plOpen = (shares*price)-(shares*avgPrice);
        let plDay = shares*change


        plOpen = plOpen.toFixed(2);
        plDay = plDay.toFixed(2);
        netLiq = netLiq.toFixed(2);
        high = high.toFixed(2);
        low = low.toFixed(2);
        low52 = low52.toFixed(2);
        high52 = high52.toFixed(2);
        percent = percent.toFixed(2);
        askPrice = askPrice.toFixed(2);
        bidPrice = bidPrice.toFixed(2);
        price = price.toFixed(2);
        change = change.toFixed(2);

        
        if(change>0){
            let string = '+$'+change+' (+'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","rgba(8, 153, 129, 1)");
            $("#plDay").css("color","rgba(8, 153, 129, 1)");
            $("#plDay").text("$"+plDay);
        }
        else if(change<0){
            let string = '-$'+Math.abs(change)+' (-'+Math.abs(percent)+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","#f1272e");
            $("#plDay").css("color","#f1272e");
            $("#plDay").text("($"+plDay+")");
        }
        else{
            let string = '+$'+change+' (+'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","white");
            $("#plDay").css("color","white");
            $("#plDay").text("$"+plDay);
        }
        $(".currPrice").each(function(){
            $(this).text("$"+price);
        });

        //dynamic price color change based on prev price
        if(prevPrice != 0){
            if(price>prevPrice){
                $('#price').css('color','rgba(8, 153, 129, 1)');
            }
            else if(price<prevPrice){
                $('#price').css('color','#f1272e');
            }
            else{
                $('#price').css('color','white');
            }
        }
        prevPrice = price;
        $("#bidPrice").text("$"+bidPrice);
        $("#askPrice").text("$"+askPrice);
        $("#low").text("$"+low);
        $("#high").text("$"+high);
        $("#52low").text("$"+low52);
        $("#52high").text("$"+high52);
        $("#netLiq").text("$"+netLiq);

        if(plOpen > 0){
            $("#plOpen").css("color","rgba(8, 153, 129, 1)");
            $("#plOpen").text("$"+plOpen);
        }
        else if(plOpen < 0){
            let temp = plOpen.substring(1);
            $("#plOpen").css("color","#f1272e");
            $("#plOpen").text("($"+temp+")");
        }
        else{
            $("#plOpen").css("color","white");
            $("#plOpen").text("$"+plOpen);
        }
    },
    complete:function(data){
        setTimeout(fetchdata,5000,ticker,prevPrice);
    }
    });
    }

$(document).ready(function(){
    let dt = new Date();
    let hour = dt.getHours();
    let minute = dt.getMinutes();
    if(hour >= 15 || (hour<8 && minute<30)){
        $('#buy-tab').css('pointer-events','none');
        $('#buy-tab').css('background-color','rgba(8, 153, 129, 0.5)');
        $('#buy-tab').css('color','grey');
        $('#sell-tab').css('pointer-events','none');
        $('#sell-tab').css('background-color','rgba(241, 39, 46, 0.5)');
        $('#sell-tab').css('color','grey');
    }

    let ticker = $('#ticker').text();
    ticker = ticker.toUpperCase();
    fetchdata(ticker,0);
});