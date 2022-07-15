document.addEventListener("DOMContentLoaded",() => {
    const rows = document.querySelectorAll("tr[data-href]");
    
    rows.forEach(row => {
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href
        });
    });
});

let totalReturn = $("#totalReturn")
let dayReturn = $("#dailyReturn")

var returns = [totalReturn,dayReturn];

$(document).ready(function(){

    for(let i = 0; i<returns.length; i++){
        let selector = returns[i];
        let value = parseFloat(returns[i].text().substring(1));
        if(value>0){
            selector.css('color',"rgba(8, 153, 129, 1)");
        }
        else if(value<0){
            selector.css('color',"#f1272e");
        }
        else{
            selector.css('color',"white");
        }
        
    }
});
