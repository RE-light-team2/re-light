

$('.humberger').on('click',function(){
    if($('#slideL').hasClass('off')){
      $('#slideL').removeClass('off');
      $('#slideL').animate({'marginLeft':'0px'},500).addClass('on');
    }else{
      $('#slideL').addClass('off');
      $('#slideL').animate({'marginLeft':'-400px'},500);
    }
  });

  
$('.hum2').on('click',function(){
  if($('#slideL').hasClass('off')){
    $('#slideL').removeClass('off');
    $('#slideL').animate({'marginLeft':'400px'},500).addClass('on');
  }else{
    $('#slideL').addClass('off');
    $('#slideL').animate({'marginLeft':'0px'},500);
  }
});

$(function(){
  $('.btn').on('click', function(event){
      event.preventDefault();
      $(this).toggleClass('active');
  });
});
/*
$(function() {

    var dis = 250;

    $("button") .click(function() {   

        $("body") .children() 
                         .animate ({
                           "margin-left" : "+=" + dis + "px"
                         }, 200); 

        dis *= -1;

    }) ;

}) ;
*/
