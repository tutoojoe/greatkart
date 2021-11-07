// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if


/*

    document.getElementById('img-container').addEventListener('mouseover', function(){
        console.log("mouse over");
        imageZoom('featured')
        
      })
      
      function imageZoom(imgID){
        console.log("njan vannea");
        let img = document.getElementById(imgID)
        let lens = document.getElementById('lens')
      console.log(lens);
        lens.style.backgroundImage = `url( ${img.src} )`
      
        let ratio = 3
      
        lens.style.backgroundSize = (img.width * ratio) + 'px ' + (img.height * ratio) + 'px';
      
        img.addEventListener("mousemove", moveLens)
        lens.addEventListener("mousemove", moveLens)
        img.addEventListener("touchmove", moveLens)
        console.log("njan mousemove");
      
        function moveLens(){
          /*
              Function sets sets position of lens over image and background image of lens
              1 - Get cursor position
              2 - Set top and left position using cursor position - lens width & height / 2
              3 - Set lens top/left positions based on cursor results
              4 - Set lens background position & invert
              5 - Set lens bounds
          
              */
      
              //1
     /*     let pos = getCursor()
          //console.log('pos:', pos)
      
          //2
          let positionLeft = pos.x - (lens.offsetWidth / 2)
          let positionTop = pos.y - (lens.offsetHeight / 2)
      
          //5
          if(positionLeft < 0 ){
            positionLeft = 0
          }
      
          if(positionTop < 0 ){
            positionTop = 0
          }
      
          if(positionLeft > img.width - lens.offsetWidth /3 ){
            positionLeft = img.width - lens.offsetWidth /3
          }
      
          if(positionTop > img.height - lens.offsetHeight /3 ){
            positionTop = img.height - lens.offsetHeight /3
          }
      
      
          //3
          lens.style.left = positionLeft + 'px';
          lens.style.top = positionTop + 'px';
      
          //4
          lens.style.backgroundPosition = "-" + (pos.x * ratio) + 'px -' +  (pos.y * ratio) + 'px'
        }
      
        function getCursor(){
          /* Function gets position of mouse in dom and bounds
              of image to know where mouse is over image when moved
              
              1 - set "e" to window events
              2 - Get bounds of image
              3 - set x to position of mouse on image using pageX/pageY - bounds.left/bounds.top
              4- Return x and y coordinates for mouse position on image
              
              */
     /* 
              let e = window.event
              let bounds = img.getBoundingClientRect()
      
              //console.log('e:', e)
              //console.log('bounds:', bounds)
              let x = e.pageX - bounds.left
              let y = e.pageY - bounds.top
              x = x - window.pageXOffset;
              y = y - window.pageYOffset;
          
          return {'x':x, 'y':y}
        }
      
        }
      
      imageZoom('featured')


    */
}); 
// jquery end

