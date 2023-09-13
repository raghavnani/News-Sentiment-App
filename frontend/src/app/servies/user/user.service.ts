import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, throwError, from, of} from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AppUserAuth } from './user-auth';
import { AppUser } from './app-user';
import { emit } from 'process';

// var passwordHash = require('password-hash');


@Injectable({
  providedIn: 'root'
})
export class UserService {
  private Url = 'http://127.0.0.1:5001/api/';  // URL to web api

  securityObject: AppUserAuth = new AppUserAuth();


  constructor(
    private http: HttpClient) { }


    getAllUsers(): Observable<any[]> { 

      return this.http.get<any[]>(this.Url+'getAllUsers')
            .pipe(
              catchError(this.handleError)
            );
    }

    getUserByEmail(entity:AppUser): Observable<string>{

      return this.http.post<string>(this.Url+'getUserByEmail', entity)
      .pipe(
        catchError(this.handleError)
      );
    }


    resetSecurityObject(): void {
      this.securityObject.userName = "";
      this.securityObject.bearerToken = "";
      this.securityObject.isAuthenticated = false;
      localStorage.removeItem("bearerToken");
    }
    
    login(entity: AppUser): 
           Observable<AppUserAuth> {
          this.resetSecurityObject();

          let username = this.getUserByEmail(entity)

          if (username){

              this.securityObject.userName = username['user_name'],
              this.securityObject.isAuthenticated=true

          }

          if (this.securityObject.userName !== "") {
            localStorage.setItem("bearerToken",
              this.securityObject.bearerToken);
          }
          return of<AppUserAuth>(this.securityObject);
        }

logout(): void {
  this.resetSecurityObject();
}

    
    
    /**
     * Handle Http operation that failed.
     * Let the app continue.
     * @param operation - name of the operation that failed
     * @param result - optional value to return as the observable result
     */
    private handleError(error) {
      
      let errorMessage = '';
            if (error.error instanceof ErrorEvent) {
                // client-side error
                errorMessage = `Error: ${error.error.message}`;
            } else {
                // server-side error
                errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
            }
            console.log(errorMessage);
            return throwError(errorMessage);
        }
    
      }