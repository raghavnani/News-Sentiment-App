import { Component, OnInit } from '@angular/core';
import { AppUser } from '../servies/user/app-user';
import { AppUserAuth } from '../servies/user/user-auth';
import { UserService } from '../servies/user/user.service';
import { Router } from '@angular/router'; 

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  constructor(private userService : UserService, private router: Router ) { }

 

  user: AppUser = new AppUser();
  securityObject: AppUserAuth = null;
 
  ngOnInit() {
  }
  
  login() {
    this.userService.login(this.user)
      .subscribe(resp => {
        this.securityObject = resp;

        if(this.securityObject){

          this.router.navigateByUrl('/tabs/tab3');
        }
      });

      }  

}
