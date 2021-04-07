var ScrollModel = require("./scroll_model").ScrollModel;
class Feed extends ScrollModel{
  constructor(){
    super(constructor);
    this.current_feed_id=0;
  }
  more(){
    this.communication_handler.get_more_feed_items(this.current_feed_id)
      .then((result)=>{
        this.dom_handler.add_more_items(result);});
  }
}
export {Feed};
