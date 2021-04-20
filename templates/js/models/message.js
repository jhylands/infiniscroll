class Message{
  constructor(){
    
  }
  static fromJSON(json_string){
    var message_info = JSON.parse(json_string);
    var message = new Message();
    message.message = message_info.message;
    message.status = message_info.status;
    message.timestamp = message_info.timestamp;
    return message;
  }
}

export {Message};
