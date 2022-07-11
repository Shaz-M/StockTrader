const selectElement = document.querySelector('#quantity');
let cash = parseFloat($("#cashBal").text().substring(1));


selectElement.addEventListener('input', inputEvent);
selectElement.addEventListener('change',inputEvent);


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
    $("#tradeCost").text("$"+cost);
    $('#resBal').text('$'+resBal);
}

function wcqib_refresh_quantity_increments() {
    jQuery("div.quantity:not(.buttons_added), td.quantity:not(.buttons_added)").each(function(a, b) {
        var c = jQuery(b);
        c.addClass("buttons_added"), c.children().first().before('<input type="button" value="-" class="minus" />'), c.children().last().after('<input type="button" value="+" class="plus" />')
    })
}
String.prototype.getDecimals || (String.prototype.getDecimals = function() {
    var a = this,
        b = ("" + a).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
    return b ? Math.max(0, (b[1] ? b[1].length : 0) - (b[2] ? +b[2] : 0)) : 0
}), jQuery(document).ready(function() {
    wcqib_refresh_quantity_increments()
}), jQuery(document).on("updated_wc_div", function() {
    wcqib_refresh_quantity_increments()
}), jQuery(document).on("click", ".plus, .minus", function() {
    var a = jQuery(this).closest(".quantity").find(".qty"),
        b = parseFloat(a.val()),
        c = parseFloat(a.attr("max")),
        d = parseFloat(a.attr("min")),
        e = a.attr("step");
    b && "" !== b && "NaN" !== b || (b = 0), "" !== c && "NaN" !== c || (c = ""), "" !== d && "NaN" !== d || (d = 0), "any" !== e && "" !== e && void 0 !== e && "NaN" !== parseFloat(e) || (e = 1), jQuery(this).is(".plus") ? c && b >= c ? a.val(c) : a.val((b + parseFloat(e)).toFixed(e.getDecimals())) : d && b <= d ? a.val(d) : b > 0 && a.val((b - parseFloat(e)).toFixed(e.getDecimals())), a.trigger("change")
});

let shares =  parseInt($("#shares").text())
let avgPrice = parseFloat($("#avgPrice").text().substring(1));
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
        let netLiq = price*shares;
        let plOpen = (shares*price)-(shares*avgPrice);
        let plDay = shares*change


        plOpen = plOpen.toFixed(2);
        netLiq = netLiq.toFixed(2);
        high = high.toFixed(2);
        low = low.toFixed(2);
        low52 = low52.toFixed(2);
        high52 = high52.toFixed(2);
        percent = percent.toFixed(2);
        askPrice = askPrice.toFixed(2);
        bidPrice = bidPrice.toFixed(2);

        
        if(change>0){
            let string = '+$'+change+' (+'+percent+'%)';
            $("#change").text(string);
            $(".priceDiv").css("color","rgba(8, 153, 129, 1)");
            $("#plDay").css("color","rgba(8, 153, 129, 1)");
            $("#plDay").text("$"+plDay);
        }
        else if(change<0){
            let string = '-$'+change+' (-'+percent+'%)';
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
        setTimeout(fetchdata,5000,ticker);
    }
    });
    }

$(document).ready(function(){
    let ticker = $('#ticker').text();
    ticker = ticker.toUpperCase();
    fetchdata(ticker);
});