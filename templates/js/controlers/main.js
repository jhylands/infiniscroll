//I guess this is the entry point and imports most things
// What we could do to make this the highest level of the dependency tree is have this import the document load function, inject a main function from here into it to gather the information required.
//That would make this module dependent on those without creating a circular dependency
var dom = require("./dom_manipulation/dom");
var get_scroll_handler = dom.get_scroll_handler;
var get_feed_handler = dom.get_feed_handler;
var get_message_handler = dom.get_message_handler;
var get_command_handler = dom.get_command_handler;

function sendCommand(command){
  postJSON(
    "/store",
    {message: command},
    handleSuccessComandSent);
}

function main(){
  var dom_getters = [get_scroll_handler, get_feed_handler, get_message_handler, get_command_handler];
  Promise.all(dom_getters.forEach(f=>f())).then(function(scroll_handler, feed_handler, message_handler, command_handler){
    //perhaps it should be here that we setup the requests

  });
}
