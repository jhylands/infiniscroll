var ScrollModel = require("./scroll_model").ScrollModel;
class Messenger extends ScrollModel{
  constructor(){
    super(constructor);
    this.current_message_id=0;
  }

  update_message_id(messages){
    var id_list = messages.map(message=>message.id);
    if (id_list.length!==0){
      this.current_message_id = Math.min(...id_list);
    }
  }
  more(){
    this.communication_handler.get_older_messages(this.current_message_id)
      .then((result)=>{
        this.update_message_id(result);
        this.dom_handler.add_older_messages(result);});
  }
}
export {Messenger};
