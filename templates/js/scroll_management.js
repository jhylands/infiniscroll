$(document).ready(function(){
    // Get references to the dom elements
    function omnibarFocus(){
      window.scroll(0, $("#iload").position().top - window.innerHeight+130);
    }
    $("#omnibar").focus(omnibarFocus).click(omnibarFocus);
      
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
    function loadItems(sentinel) {
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
            if(sentinel===sentinels[0]){
              console.log("try add to top")
              scrollers[0].insertBefore(template_clone, scrollers[0].childNodes[0]);
            }else{
              scrollers[1].appendChild(template_clone);
            }
              
            // Increment the counter
            counter += 1;
            // Update the counter in the navbar
            loaded.innerText = `${counter} items loaded`;
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
      loadItems(sentinels[0]);
    });
    var intersectionObserver2 = new IntersectionObserver(entries => {
      // If intersectionRatio is 0, the sentinel is out of view
      // and we don't need to do anything. Exit the function
      if (entries[0].intersectionRatio <= 0) {return;}
      // Call the loadItems function
      loadItems(sentinels[1]);
    });

    // Instruct the IntersectionObserver to watch the sentinel
    intersectionObserver1.observe(sentinels[0]);
    intersectionObserver2.observe(sentinels[1]);
});

document.addEventListener('scroll', function(e) {
  var inputbox = $(".inputbox");
  var middle_box = $(".display-4").position().top;
  var input_top = window.scrollY - middle_box;
  if(input_top>-20){
    inputbox.addClass("fix-search-top");
  }else if(input_top<-window.innerHeight-30){
    inputbox.addClass("fix-search-bottom");
  }else{
    inputbox.removeClass("fix-search-top");
    inputbox.removeClass("fix-search-bottom");
  }
 });
