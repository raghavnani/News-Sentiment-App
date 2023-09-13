import { Component, OnInit, ViewChild } from '@angular/core';
import { UserService } from '../servies/user/user.service';
import { Router } from '@angular/router'; 
import { AppUserAuth } from '../servies/user/user-auth';
import { IonInfiniteScroll } from '@ionic/angular';


@Component({
  selector: 'app-tab4',
  templateUrl: './tab4.page.html',
  styleUrls: ['./tab4.page.scss'],
})
export class Tab4Page implements OnInit {
  // @ViewChild(IonInfiniteScroll) infiniteScroll: IonInfiniteScroll;


  securityObject: AppUserAuth = null;

  constructor(private userService : UserService, private router: Router ) { 
    this.securityObject = 
    userService.securityObject;
  }

  ngOnInit() {
  }

  logout(){
      
    this.userService.logout()

    this.router.navigateByUrl('/tabs/tab1');

  }

}
