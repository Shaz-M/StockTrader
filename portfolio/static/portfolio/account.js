const deposit = document.querySelector('#deposit');
const withdraw = document.querySelector('#withdraw');

const balance = parseFloat($("#accountBal").text().substring(1));


deposit.addEventListener('input', depositEvent);
withdraw.addEventListener('input',withdrawEvent);

function depositEvent(){
    let depositAmt = parseInt(event.target.value);
    let newBal = balance;
    if(!Number.isNaN(depositAmt)){
        newBal+=depositAmt;
    }
    $('#depositBal').text('$'+newBal);
}

function withdrawEvent(){
    let withdrawAmt = parseInt(event.target.value);
    let newBal = balance;
    if(!Number.isNaN(withdrawAmt)){
        newBal-=withdrawAmt;
    }
    $('#withdrawBal').text('$'+newBal);
}

var inputs = $("form#buy-form input");
var inputs2 = $("form#sell-form input");


var validateInputs = function validateInputs(inputs) {
  var validForm = true;
  inputs.each(function(index) {
    var input = $(this);
    if (!input.val() || (input.type === "radio" && !input.is(':checked'))) {
      $("#deposit-button").attr("disabled", "disabled");
      $("#deposit-button").css('background-color','grey');
      validForm = false;
    }
  });
  return validForm;
}

var validateInputs2 = function validateInputs2(inputs) {
    var validForm = true;
    inputs.each(function(index) {
      var input = $(this);
      if (!input.val() || (input.type === "radio" && !input.is(':checked'))) {
        $("#sell-button").attr("disabled", "disabled");
        validForm = false;
      }
    });
    return validForm;
  }

inputs.change(function() {
    if (validateInputs(inputs)) {
      $("#deposit-button").removeAttr("disabled");
      $("#deposit-button").css('background-color','#7eb8f3');
    }
  });

inputs2.change(function() {
  if (validateInputs(inputs2)) {
    $("#sell-button").removeAttr("disabled");
    $("#sell-button").css('background-color','#7eb8f3');
  }
});

$(document).ready(function(){
    $("#deposit-button").attr("disabled", "disabled");
    $("#deposit-button").css('background-color','grey');
    $("#sell-button").attr("disabled", "disabled");
    $("#sell-button").css('background-color','grey');
});