var MVPModel = require("./scroll_model").MVPModel;
var Message = require("../models/message").Message;
class Command extends MVPModel{
  attach_dom_handler(handler){
    throw "Can't attach a single dom handler";
  }
  attach_dom_input_handler(handler){
    this.dom_input_handler = handler;
    this.dom_input_handler.attach_message_sender(this.make_new_message_callback());
  }
  attach_dom_output_handler(handler){
    this.dom_output_handler = handler;
  }

  make_new_message_callback(){
    var self = this;
    return function(message_text){
      if(message_text==="logout"){
        window.location.replace("/logout");
      }
      var message = new Message();
      message.message = message_text;
      //self.dom_output_handler.add_new_message(message);
      self.communication_handler.submit_new_message(message)
        .then(function(response){
          if(response!=={}){
            self.dom_output_handler.add_new_message(response);
          }
        });
    };
  }
  
  
}

export {Command};
