// The idea behind this class is to abstract away manipulations on
// the dom so that when communicated with the software is talking at the level of messages and elements on the feed
const FIRST = 0;

class FeedHandler{
  constructor(){
    this.lower_sentinel = $("#sentinel_lower");
  }
  feed_item_to_dom(feed_item){
    let template_clone = this.get_template().content.cloneNode(true);
    // Query & update the template content
    template_clone.querySelector("#title").innerHTML = feed_item.title;
    template_clone.querySelector("#content").innerHTML = feed_item.content;
    return template_clone;
  }

  prepend_item(feed_item){
    this.get_scroller()
      .insertBefore(
        this.feed_item_to_dom(feed_item),
        this.get_scroller().childNodes[FIRST]);
  }
  add_more_items(items){
    // Iterate over the items in the response
    for (var i = 0; i < items.length; i++) {
      this.get_scroller()
        .appendChild(
          this.feed_item_to_dom(items[i]));
    }
  }
  get_scroller(){
    return $("#scroller_lower");
  }
  get_template(){
    return $("#post_template");
  }
  get_lower_sentinel(){
    if(this.lower_sentinel){
      return this.lower_sentinel;
    }else{
      this.lower_sentinel = $("#sentinel_lower");
    }
  }
}

class MessageHandler{
  constructor(){
    this.messages = [];
    this.upper_sentinel = $("#sentinel_upper");
  }
  get_upper_sentinel(){
    if(this.upper_sentinel){
      return this.upper_sentinel;
    }else{
      this.upper_sentinel = $("#sentinel_upper");
    }
  }
  setup_loader(message_sender){
    this.message_sender = message_sender;
  }
  add_new_message(message){
  }
  add_older_messages(messages){
  }

  handleSuccessComandSent(response, textStatus, jqXHR) {
    console.log(response);
    $("#omnibar")[FIRST].value = "";
  }
}

class CommandHandler{
  constructor(){
    $("#omnibar")
      .focus(this.scrollToTypePosition)
      .click(this.scrollToTypePosition)
      .keypress(this.handleOmniboxTyping);
  }
  eventIsReturnCarridge(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    return keycode == "13";
  }
  handleOmniboxTyping(event){
    var omnibarValue = $("#omnibar")[FIRST].value;
    if(this.eventIsReturnCarridge(event) && omnibarValue !== ""){
      this.sendCommand(omnibarValue);
    } 
  }
  scrollToTypePosition(){
    /* This function induces the page to scroll so that the
       omnibox is at the bottom of the page.
    */
    window.scroll({
      top: $("#iload").position().top - window.innerHeight+140,
      left: 0,
      behavior: "smooth"});
  }
}

class ScrollHandler{
  constructor(){
    document.addEventListener("scroll", this.scrollHandler);
    // Provide some default top and bottom functions
    this.top_handler = function(){};
    this.bottom_handler = function(){};
  }
  attach_top_handler(top_handler){
    this.top_handler = top_handler;
  }
  attach_bottom_handler(bottom_handler){
    this.bottom_handler = bottom_handler;
  }
  scrollHandler(e){
    const THRESHOLD = 100;
    var inputbox = $(".inputbox");
    var middle_box = $(".display-4").position().top;
    var input_top = window.scrollY - middle_box;
    if(input_top>THRESHOLD){
      inputbox.addClass("fix-search-top");
    }else if(input_top<-window.innerHeight+THRESHOLD){
      inputbox.addClass("fix-search-bottom");
    }else{
      inputbox.removeClass("fix-search-top");
      inputbox.removeClass("fix-search-bottom");
    }
    if(window.scrollY<THRESHOLD){
      //more messages
      this.top_handler();
    }else if(window.scrollY+THRESHOLD>document.body.scrollHeight){
      //more feed
      this.bottom_handler();
    }
  }

}


//Functions to export from module (Used by main)
function get_scroll_handler(server){
  return new Promise(function(resolve, reject){
    $(document).ready(function(){
      resolve(new ScrollHandler());
    });
  });
}
function get_feed_handler(server){
  return new Promise(function(resolve, reject){
    $(document).ready(function(){
      resolve(new FeedHandler());
    });
  });
}
function get_message_handler(server){
  return new Promise(function(resolve, reject){
    $(document).ready(function(){
      resolve(new MessageHandler(server));
    });
  });
}
function get_command_handler(server){
  return new Promise(function(resolve, reject){
    $(document).ready(function(){
      resolve(new CommandHandler(server));
    });
  });
}

export {get_scroll_handler, get_feed_handler, get_message_handler, get_command_handler};
