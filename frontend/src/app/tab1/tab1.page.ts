import { Component , HostListener, ViewChild} from '@angular/core';
import { NewsService } from '../servies/news.service';
import { News } from '../servies/news';
import { UserService } from '../servies/user/user.service';
import { AppUserAuth } from '../servies/user/user-auth';
import { Router } from '@angular/router'; 
import { IonContent } from '@ionic/angular';


@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {
  @ViewChild('pageTop') pageTop: IonContent;

  news:News[] = [];

  article:News;

  page:number
  condition:string

  securityObject: AppUserAuth = null;


  constructor(private newsService : NewsService, private userService : UserService, private router: Router ) {

    this.securityObject = 
    userService.securityObject;

    this.page = 0

        this.news=[]

   }

  ngOnInit() {

    this.getSelectedNews('Latest')


  }


  saveArticle(article:News){

    if(this.securityObject.isAuthenticated){

      this.newsService.updateSavedNews(article.get_id(), article.get_saved()).subscribe(element =>{


        if (element['saved']== true){
  
          this.ngOnInit()
          
      }
    });  
    }else{

      this.router.navigateByUrl('login');


    }
  }

  getSelectedNews(value:string){

    if (this.pageTop){

      this.pageTop.scrollToTop();

    }

    this.news=[]
    this.page=0
    this.condition = value

    this.newsService.getSelectedNews(this.condition,this.page).subscribe(neutrals =>{

      neutrals.forEach(element => {



        if (element['logits']){

          let article = new News(element['id'],element['news_filter_id'],element['source'],element['title'],
                                  element['content'], element['description'], element['url'], element['image_url'], element['published_at'],
                                      element['text'], element['logits'].split(',').map(x=>+x), element['sentiment'], element['saved']);
            this.news.push(article)
      }
    });  
    })


    }
    

    getMoreData(event){

      this.page = this.page+1

      this.fetchMoreData(event)


}

fetchMoreData(event){

  this.newsService.getSelectedNews(this.condition, this.page).subscribe(latest =>{

    latest.forEach(element => {

      if (element['logits']){

        let article = new News(element['id'],element['news_filter_id'],element['source'],element['title'],
                                element['content'], element['description'], element['url'], element['image_url'], element['published_at'],
                                    element['text'], element['logits'].split(',').map(x=>+x), element['sentiment'], element['saved']);
          this.news.push(article)
    }
  });  

  event.target.complete();

  })
}



}
