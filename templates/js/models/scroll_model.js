class ScrollModel{
  attach_communication_handler(handler){
    this.communication_handler = handler;
  }
  attach_dom_handler(handler){
    this.dom_handler = handler;
  }
  more(){
    //abstract
    //function to load more be it messages or feed items
    
  }
}
export {ScrollModel};
