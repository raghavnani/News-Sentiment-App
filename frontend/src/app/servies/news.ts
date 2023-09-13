export class News{

    constructor(

        // _id, , source, title, content, description, url, image_url, published_at, text,
        // logits, sentiment

    private _id:number,
    private news_filter_id: string,
    private source:string,
    private title:string,
    private content: string,
    private description:string,
    private url:string,
    private imageUrl : string,
    private publishedAt:string,
    private text:string,
    private logits:number[],
    private sentiment:string,
    private saved:number
    )
    {}    
    
    public get_id(): number{
        return this._id;
    }


    public get_news_filter_id(): string{
        return this.news_filter_id;
    }

    public get_source(): string{
        return this.source;
    }


    public get_title(): string{
        return this.title;
    }

    public get_content(): string{
        return this.content;
    }

    public get_description(): string{
        return this.description;
    }

    public get_text(): string{
        return this.text;
    }
    public get_logits(): number[]{
        return this.logits;
    }
    public get_sentiment(): string{
        return this.sentiment;
    }

    public get_url(): string{
        return this.url;
    }

    public get_image_url(): string{
        return this.imageUrl;
    }

    public get_published_at(): string{
        return this.publishedAt;
    }

    public get_saved(): number{
        return this.saved;
    }

    public set_saved(saved: number){
        return this.saved = saved
    }



}
