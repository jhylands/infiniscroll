var ScrollModel = require("./scroll_model").ScrollModel;
class Messenger extends ScrollModel{
  constructor(){
    super(constructor);
    this.current_message_id=0;
  }
  more(){
    this.communication_handler.get_older_messages(this.current_message_id)
      .then((result)=>{
        this.dom_handler.add_older_messages(result);});
  }
}
export {Messenger};
