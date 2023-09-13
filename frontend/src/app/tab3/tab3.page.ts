import { Component } from '@angular/core';
import { News } from '../servies/news';
import { NewsService } from '../servies/news.service';
import { AppUserAuth } from '../servies/user/user-auth';
import { UserService } from '../servies/user/user.service';

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page {

  news:News[] = [];

  article:News;

  users:any[]

  target:any

  securityObject: AppUserAuth = null;


  folder:any
  sentimentSelected:string

  constructor(private newsService : NewsService , private userService : UserService) { 

    this.securityObject = 
     userService.securityObject;
  }



  ngOnInit() {

    // this.getSelectedNews("Positive")

    this.getAllUsers()

  }


  getAllUsers(){
    this.newsService.getAllUsers().subscribe(users =>{

      console.log(users)

      this.users = users
    })
  }



  // getSelectedNews(condition:string){

  //   this.news=[]

  //   this.newsService.getSelectedNews(condition).subscribe(neutrals =>{

  //     neutrals.forEach(element => {



  //       if (element['logits']){

  //         let article = new News(element['id'],element['news_filter_id'],element['source'],element['title'],
  //                                 element['content'], element['description'], element['url'], element['image_url'], element['published_at'],
  //                                     element['text'], element['logits'].split(',').map(x=>+x), element['sentiment'], element['saved']);
  //           this.news.push(article)
  //     }
  //   });  
  //   })
  //   }



}
