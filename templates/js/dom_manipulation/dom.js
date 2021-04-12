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
    return $("#scroller_lower")[FIRST];
  }
  get_template(){
    return $("#post_template")[FIRST];
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
    this.get_scroller()
      .appendChild(
        this.message_to_dom(message));
  }
  add_older_messages(items){
    // Iterate over the items in the response
    for (var i = 0; i < items.length; i++) {
      //Not sure this is the right direction
      this.get_scroller()
        .prepend(
          this.message_to_dom(items[i]));
    }
  }
  message_to_dom(message){
    let template_clone = this.get_template().content.cloneNode(true);
    // Query & update the template content
    template_clone.querySelector("#user").innerHTML = message.id;
    template_clone.querySelector("#content").innerHTML = message.message;
    template_clone.querySelector("#datetime").innerHTML = message.timestamp;
    return template_clone;
  }
  get_scroller(){
    return $("#scroller_upper")[FIRST];
  }
  get_template(){
    return $("#message_template")[FIRST];
  }

  handleSuccessComandSent(response, textStatus, jqXHR) {
    console.log(response);
    $("#omnibar")[FIRST].value = "";
  }
}

class CommandHandler{
  constructor(){
    this.sendCommand = function(){console.log("sendCommand needs setting");};
    $("#omnibar")
      .focus(this.scrollToTypePosition)
      .click(this.scrollToTypePosition)
      .keypress(this.make_handle());

  }
  eventIsReturnCarridge(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    return keycode == "13";
  }
  attach_message_sender(sendCommand){
    this.sendCommand = sendCommand;
  }

  make_handle(){
    var self = this;
    return function handleOmniboxTyping(event){
      var omnibarValue = self.get_box().value;
      if(self.eventIsReturnCarridge(event) && omnibarValue !== ""){
        self.get_box().value = "";
        self.sendCommand(omnibarValue);
      } 
    };
  }
  get_box(){
    return $("#omnibar")[FIRST];
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
    document.addEventListener("scroll", this.make_scroll_handler());
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
  make_scroll_handler(){
    var self = this;
    return function scrollHandler(e){
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
        self.top_handler();
      }else if(window.scrollY+window.innerHeight>document.body.scrollHeight){
        //more feed
        self.bottom_handler();
      }
    };
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
