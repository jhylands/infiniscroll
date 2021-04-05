class Message{
  constructor(){
    
  }
  static fromJSON(json_string){
    var a = JSON.parse(json_string);
    return new Message();
  }
}

export {Message};
