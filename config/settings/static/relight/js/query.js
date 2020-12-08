

$('.humberger').on('click',function(){
    if($('#slideL').hasClass('off')){
      $('#slideL').removeClass('off');
      $('#slideL').animate({'marginLeft':'0px'},500).addClass('on');
    }else{
      $('#slideL').addClass('off');
      $('#slideL').animate({'marginLeft':'-400px'},500);
    }
  });

  