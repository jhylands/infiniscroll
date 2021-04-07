var Message = require("../models/message").Message;
var FeedItem = require("../models/feed_item").FeedItem;
function webRequestExceptionHander(jqXHR, textStatus, errorThrown) {
  // A catch all and log
  console.log(jqXHR);
  console.log(textStatus);
  console.log(errorThrown);
}

class Server{
  constructor(user_token){
    this.user_token = user_token;
  }
  postJSON(url, data, success){
    // Maybe put a check that the data isn't a string already here
    // Also potentially an optional exception handler, even though this has a good default
    //maybe this should return a promise
    var formData = JSON.stringify(data); //Array 
    $.ajax({
      url : url,
      type: "POST", 
      dataType: "json",
      contentType: "application/json",
      data : formData, // data in json format
      async : false,
      success: success,
      error: webRequestExceptionHander});
  }
    
}
class FeedComs extends Server{
  get_more_feed_items(){
    var self = this;
    //should return a promise of more items
    return new Promise(function(resolve, reject){
      var data = {};
      var url = "/load";
      self.postJSON(url, data, resolve);
    });
  }
  make_feed_items(response){
    response.json().then((data) => {
      // If empty JSON, exit the function
      if (!data.length) {
        // Replace the spinner with "No more posts"
        return [];
      }else{
        return data.forEach(feed_item => FeedItem.fromJSON(feed_item));
      }
    });
  }
}

class MessageComs extends Server{
  get_older_messages(current_message_id){
    //should return a promise of more messages
    var self = this;
    return new Promise(function(resolve, reject){
      var data = {};
      var url;
      if(current_message_id!==0){
        url = "/previous_messages/" + current_message_id;
      }else{
        url = "/previous_messages/";
      }
      self.postJSON(url, data, resolve);
    });
  }
  submit_new_message(message){
    var self = this;
    //should return a promise of more messages
    return new Promise(function(resolve, reject){
      var data = {message:message.message};
      var url = "/store_message";
      self.postJSON(url, data, resolve);
    });
  }
  // Function to request new items and render to the dom
  make_messages(response){
    response.json().then((data) => {
      // If empty JSON, exit the function
      if (!data.length) {
        // Replace the spinner with "No more posts"
        return [];
      }else{
        return data.forEach(message => Message.fromJSON(message));
      }
    });
  }
}

export {MessageComs, FeedComs};
