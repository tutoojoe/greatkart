// imageZoom("myimage", "myresult");
// function imageZoom(imgID, resultID) {
//   var img, lens, result, cx, cy;
//   img = document.getElementById(imgID);
//   result = document.getElementById(resultID);
//   /*create lens:*/
//   lens = document.createElement("DIV");
//   lens.setAttribute("class", "img-zoom-lens");
//   /*insert lens:*/
//   img.parentElement.insertBefore(lens, img);
//   /*calculate the ratio between result DIV and lens:*/
//   console.log("result.offsetWidth  >>>>>", result.offsetWidth ,"lens.offsetWidth>>>>>>>>>>>",lens.offsetWidth);
//   cx = 300 / lens.offsetWidth;
//   console.log("result.offsetHeight>>>>>",result.offsetHeight ,"llens.offsetHeighth>>>>>>>>>>>",lens.offsetHeight);
//   cy = 300 / lens.offsetHeight;
//   /*set background properties for the result DIV:*/
//   result.style.backgroundImage = "url('" + img.srcset + "')";
//   result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
//   /*execute a function when someone moves the cursor over the image, or the lens:*/
//   lens.addEventListener("mousemove", moveLens);
//   img.addEventListener("mousemove", moveLens);
//   /*and also for touch screens:*/
//   lens.addEventListener("touchmove", moveLens);
//   img.addEventListener("touchmove", moveLens);
//  // img.addEventListener("mouseenter", bigImg);  
 
  
  
// function bigImg(x) {
//   console.log("onmouseenter >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
// }

// function normalImg(x) {
// //result.style.display ="none";
//      console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>onmousLEAVE");
// }


  
// function moveLens(e) {
//   var pos, x, y;
//   /*prevent any other actions that may occur when moving over the image:*/
//   e.preventDefault();
//   /*get the cursor's x and y positions:*/
//   pos = getCursorPos(e);
//   /*calculate the position of the lens:*/
//   x = pos.x - (lens.offsetWidth / 2);
//   y = pos.y - (lens.offsetHeight / 2);
// // console.log("x" , x , "and Y " , y); 
//   /*prevent the lens from being positioned outside the image:*/
//   if (x > img.width - lens.offsetWidth) {x = img.width - lens.offsetWidth;  } //else{img.addEventListener("mouseenter", bigImg);  }
//   if (x < 0) {x = 0;}
//   if (y > img.height - lens.offsetHeight) {y = img.height - lens.offsetHeight; img.addEventListener("mouseleave",  normalImg);}//else{img.addEventListener("mouseenter", bigImg);  }
//   if (y < 0) {y = 0;}
//   /*set the position of the lens:*/
//   lens.style.left = x + "px";
//   lens.style.top = y + "px";
//   /*display what the lens "sees":*/
//   result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
// }
// function getCursorPos(e) {
//   var a, x = 0, y = 0;
//   e = e || window.event;
//   /*get the x and y positions of the image:*/
//   a = img.getBoundingClientRect();
//   //console.log("------------------A  left" ,  a ); 
//   /*calculate the cursor's x and y coordinates, relative to the image:*/
//   x = e.pageX - a.left;
//   y = e.pageY - a.top;
//   /*consider any page scrolling:*/
//   x = x - window.pageXOffset;
//   y = y - window.pageYOffset;
//   return {x : x, y : y};
// }

// }

// function hideme(x) {
//     //x.style.display = "none";
   
// }
// function showme(x) {
//     //x.style.display = "block";
   
// }


document.getElementById('img-container').addEventListener('mouseover', function(){
  console.log("mouse over");
  imageZoom('featured')
  
})

function imageZoom(imgID){
  console.log("njan vannea");
  let img = document.getElementById(imgID)
  let lens = document.getElementById('lens')

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
    let pos = getCursor()
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