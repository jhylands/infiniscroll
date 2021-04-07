//I guess this is the entry point and imports most things
// What we could do to make this the highest level of the dependency tree is have this import the document load function, inject a main function from here into it to gather the information required.
//That would make this module dependent on those without creating a circular dependency
var dom = require("../dom_manipulation/dom");
var get_scroll_handler = dom.get_scroll_handler;
var get_feed_handler = dom.get_feed_handler;
var get_message_handler = dom.get_message_handler;
var get_command_handler = dom.get_command_handler;
var Server = require("../server_coms/send_recive");
var MessageComs = Server.MessageComs;
var FeedComs = Server.FeedComs;

var Feed = require("../models/feed").Feed;
var Messenger = require("../models/messenger").Messenger;
var Command = require("../models/command").Command;

// I don't really want these to be global but they need to be defined after the promises have come back...
// Not that those two things are conflicting but
var feed;
var messenger;

function main(){
  var dom_getters = [get_scroll_handler, get_feed_handler, get_message_handler, get_command_handler];
  Promise.all(dom_getters.map(f=>f()))
    .then(function(results){
      var scroll_handler = results[0];
      var feed_handler = results[1];
      var message_handler = results[2];
      var command_handler = results[3];

      // If we have the server passed into the dom handlers
      // then these controlers are superflous.
      // might be a good use case for one of books.
      feed = new Feed();
      feed.attach_dom_handler(feed_handler);
      feed.attach_communication_handler(new FeedComs());
      messenger = new Messenger();
      messenger.attach_dom_handler(message_handler);
      var message_coms = new MessageComs();
      messenger.attach_communication_handler(message_coms);

      //perhaps it should be here that we setup the requests
      scroll_handler.attach_top_handler(
        function(){messenger.more();});
      scroll_handler.attach_bottom_handler(
        function(){feed.more();});
      messenger.more();
      feed.more();

      var commander = new Command();
      commander.attach_communication_handler(message_coms);
      commander.attach_dom_input_handler(command_handler);
      commander.attach_dom_output_handler(message_handler);
      
    });
}

main();
