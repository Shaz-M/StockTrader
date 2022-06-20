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
    // for each stock in the portfolio add the dyanmic data
    // overall sums are summed during each iteration
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

            plOpen = parseFloat(plOpen);
            plDay = parseFloat(plDay);
            let pl = [plOpen,plDay];
            let selectors = [openDom,dayDom];
            
    
            for(let i = 0; i<selectors.length; i++){
                element = selectors[i];
                let temp = pl[i].toFixed(2);
                if(pl[i] > 0){
                    element.style.color = "rgba(8, 153, 129, 1)";
                    element.innerText = "$"+temp;
                }
                else if(pl[i] < 0){
                    temp = temp.substring(1);
                    element.style.color = "#f1272e";
                    element.innerText = "($"+temp+')';
                }
                else{
                    element.style.color = "white";
                    element.innerText = "$"+temp;
                }
        
            }
            percentPL = parseFloat(percentPL);
            let temp =  percentPL.toFixed(2);
            if(percentPL>0){
                percentDom.style.color = "rgba(8, 153, 129, 1)";
                percentDom.innerText = "$"+temp;
            }
            else if(percentPL<0){
                percentDom.style.color = "#f1272e";
                percentDom.innerText = temp+'%';
            }
            else{
                percentDom.style.color = "white";
                percentDom.innerText = temp+"%";            
            }


            plOpen = plOpen.toFixed(2);
            plDay = plDay.toFixed(2);
            netLiq = netLiq.toFixed(2);
            percentPL = percentPL.toFixed(2);

            sumPlOpen += parseFloat(plOpen);
            sumPlDay += parseFloat(plDay);
            sumNetLiq += parseFloat(netLiq);

            markDom.innerText = price;
            netLiqDom.innerText = "$"+netLiq;
            percentDom.innerText = percentPL+"%";
        },
        });
    }
    //after all stocks added, collect totals and display
    sumPlOpen = sumPlOpen.toFixed(2);
    sumPlOpen = parseFloat(sumPlOpen);
    sumPlDay = sumPlDay.toFixed(2);
    sumPlDay = parseFloat(sumPlDay);
    sumNetLiq = sumNetLiq.toFixed(2);
    sumNetLiq = parseFloat(sumNetLiq);
    let sums = [sumPlDay,sumPlOpen,sumNetLiq];
    let selectors = ['.totalPlDay','.totalPlOpen','.totalNetLiq'];

    for(let i = 0; i<selectors.length; i++){
        $(selectors[i]).each(function(){
            temp = sums[i].toFixed(2);
            if(sums[i] > 0){
                $(this).css("color","rgba(8, 153, 129, 1)");
                $(this).text("$"+temp);
            }
            else if(sums[i] < 0){
                temp = temp.substring(1);
                $(this).css("color","#f1272e");
                $(this).text("($"+temp+")");
            }
            else{
                $(this).css("color","white");
                $(this).text("$"+temp);
            }
        })

    }
    //repeat function every interval
    setTimeout(fetchdata,5000,stocks);
}

$(document).ready(function(){
    fetchdata(stocks);
});