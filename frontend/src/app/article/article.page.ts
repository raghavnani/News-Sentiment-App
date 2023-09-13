import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { News } from '../servies/news';
import { element } from 'protractor';


@Component({
  selector: 'app-article',
  templateUrl: './article.page.html',
  styleUrls: ['./article.page.scss'],
})
export class ArticlePage implements OnInit {

  article:News;

  constructor(private location:Location){
  }

  ngOnInit() {

    let element = this.location.getState();

    this.article = new News(element['_id'],element['news_filter_id'],element['source'],element['title'],
                                  element['content'], element['description'], element['url'], element['imageUrl'], element['publishedAt'],
                                      element['text'], element['logits'], element['sentiment'], element['saved']);
            

    console.log(this.article)

  }


}
