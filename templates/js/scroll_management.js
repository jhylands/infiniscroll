var firstOmni = true;
$(document).ready(function(){
    function send_message(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13') {
      if($("#omnibar").value !== ""){
        var formData = JSON.stringify({message:$("#omnibar")[0].value}); //Array 
      
        $.ajax({
            url : "/store", // Url of backend (can be python, php, etc..)
            type: "POST", // data type (can be get, post, put, delete)
            dataType: 'json',
            contentType: 'application/json',
            data : formData, // data in json format
            async : false, // enable or disable async (optional, but suggested as false if you need to populate data afterwards)
            success: function(response, textStatus, jqXHR) {
              console.log(response);
              $("#omnibar")[0].value = "";
              load_messages(document.querySelector('#sentinel_upper'));
            },
            error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
        });
       } 
    }
    }
    // Get references to the dom elements
    function omnibarFocus(){
      window.scroll({top: $("#iload").position().top - window.innerHeight+140, left:0, behavior: "smooth"});
    }

    $("#omnibar").focus(omnibarFocus).click(omnibarFocus).keypress(send_message);
      
    var scrollers = [
      document.querySelector("#scroller_upper"),
      document.querySelector("#scroller_lower")];
    var template = document.querySelector('#post_template');
    var loaded = document.querySelector("#loaded");

    var sentinels = [
      document.querySelector('#sentinel_upper'),
      document.querySelector('#sentinel_lower')];

    // Set a counter to count the items loaded
    var counter = 0;

    // Function to request new items and render to the dom
    function load_messages(sentinel){
      fetch(`last/5`).then((response) => {
        // Convert the response data to JSON
        response.json().then((data) => {
          // If empty JSON, exit the function
          if (!data.length) {
            // Replace the spinner with "No more posts"
            sentinel.innerHTML = "No more posts";
            console.log("limit reached");
            return;
          }
          // Iterate over the items in the response
          for (var i = 0; i < data.length; i++) {
            // Clone the HTML template
            let template_clone = template.content.cloneNode(true);
            // Query & update the template content
            template_clone.querySelector("#title").innerHTML = `${data[i].id}: ${data[i].message}`;
            template_clone.querySelector("#content").innerHTML = data[i].message;
            // Append template to dom
              scrollers[0].insertBefore(template_clone, scrollers[0].childNodes[0]);
            // Increment the counter
            counter += 1;
            // Update the counter in the navbar
            loaded.innerText = `${counter} items loaded`;
          }
          if(firstOmni){
            omnibarFocus();
            firstOmni = false;
          }
        })
      })
    }
    function load_feed(sentinel) {
      // Use fetch to request data and pass the counter value in the QS
      fetch(`/load?c=${counter}`).then((response) => {
        // Convert the response data to JSON
        response.json().then((data) => {
          // If empty JSON, exit the function
          if (!data.length) {
            // Replace the spinner with "No more posts"
            sentinel.innerHTML = "No more posts";
            console.log("limit reached");
            return;
          }
          // Iterate over the items in the response
          for (var i = 0; i < data.length; i++) {
            // Clone the HTML template
            let template_clone = template.content.cloneNode(true);
            // Query & update the template content
            template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
            template_clone.querySelector("#content").innerHTML = data[i][2];
            // Append template to dom
            scrollers[1].appendChild(template_clone);
              
            // Increment the counter
            counter += 1;
            // Update the counter in the navbar
            loaded.innerText = `${counter} items loaded`;
          }
          if(firstOmni){
            omnibarFocus();
            firstOmni = false;
          }
        })
      })
    }

    // Create a new IntersectionObserver instance
    var intersectionObserver1 = new IntersectionObserver(entries => {
      // If intersectionRatio is 0, the sentinel is out of view
      // and we don't need to do anything. Exit the function
      if (entries[0].intersectionRatio <= 0) {return;}
      // Call the loadItems function
      load_messages(sentinels[0]);
    });
    var intersectionObserver2 = new IntersectionObserver(entries => {
      // If intersectionRatio is 0, the sentinel is out of view
      // and we don't need to do anything. Exit the function
      if (entries[0].intersectionRatio <= 0) {return;}
      // Call the loadItems function
      load_feed(sentinels[1]);
    });

    // Instruct the IntersectionObserver to watch the sentinel
    intersectionObserver1.observe(sentinels[0]);
    intersectionObserver2.observe(sentinels[1]);
});

document.addEventListener('scroll', function(e) {
  var inputbox = $(".inputbox");
  var middle_box = $(".display-4").position().top;
  var input_top = window.scrollY - middle_box;
  if(input_top>100){
    inputbox.addClass("fix-search-top");
  }else if(input_top<-window.innerHeight+100){
    inputbox.addClass("fix-search-bottom");
  }else{
    inputbox.removeClass("fix-search-top");
    inputbox.removeClass("fix-search-bottom");
  }
 });
