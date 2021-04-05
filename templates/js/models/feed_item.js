
class FeedItem{
  constructor(title, content, position){
    this.title = title;
    this.content = content;
    this.position = position;
  }

  static fromJSON(json_string){
    var a = JSON.parse(json_string);
    var title = a.title;
    var content = a.content;
    var position = a.position;
    return new FeedItem(title, content, position);
  }
}

export {FeedItem};
